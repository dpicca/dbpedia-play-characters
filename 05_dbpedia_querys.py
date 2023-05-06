import re
import os
import pickle
from SPARQLWrapper import SPARQLWrapper, JSON
from time import sleep
import pandas as pd

def query_dbpedia( query):
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    query = re.sub(r"\s+", " ", query.replace("\n", " "))
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    query_results = sparql.queryAndConvert()

    results = list()
    for entry in query_results["results"]["bindings"]:
        formatted_entry = dict()
        for key, value in entry.items():
            formatted_entry[key] = value["value"]
        results.append(formatted_entry)
    return results



# GET CHARACTERS

query = """
PREFIX dbc: <http://dbpedia.org/resource/Category:>
PREFIX dbo: <http://dbpedia.org/ontology/>
SELECT DISTINCT ?c (?n as count(?b))
WHERE { 
     ?c a dbo:FictionalCharacter.
     ?c ?p ?b.
     ?b a dbo:WrittenWork
}
 LIMIT 10000
 group by ?c
"""

dbpedia_characters = query_dbpedia(query)



offset = 0
while len(dbpedia_characters) % 10000 == 0:
    offset += 10000
    query_1 = query + """
    OFFSET %s
    """ % offset
    dbpedia_characters += query_dbpedia(query_1)

characters = {i["c"] for i in dbpedia_characters}



query = """
PREFIX dbc: <http://dbpedia.org/resource/Category:>
PREFIX dbo: <http://dbpedia.org/ontology/>
SELECT DISTINCT ?c 
WHERE { 
	 ?c a dbo:Person
	  ; dbo:creator []
}
"""

dbpedia_characters = query_dbpedia(query)
characters = characters.union({i["c"] for i in dbpedia_characters})


query = """
PREFIX dbc: <http://dbpedia.org/resource/Category:>
PREFIX dbo: <http://dbpedia.org/ontology/>
SELECT DISTINCT ?c 
WHERE { 
    ?c <http://purl.org/linguistics/gold/hypernym> dbr:Character.
}
LIMIT 10000
"""
dbpedia_characters = query_dbpedia(query)

offset = 0
while len(dbpedia_characters) % 10000 == 0:
    offset += 10000
    query_1 = query + """
    OFFSET %s
    """ % offset
    dbpedia_characters += query_dbpedia(query_1)

characters = characters.union({i["c"] for i in dbpedia_characters})
with open(os.path.expanduser("~/Desktop/characters_dbpedia.p"), "wb") as file:
    pickle.dump(characters, file)


# GET ALL CreativeWorks and Authors and wikidata links

query = """
PREFIX dbc: <http://dbpedia.org/resource/Category:>
PREFIX dbo: <http://dbpedia.org/ontology/>
SELECT DISTINCT ?work ?author ?workwikidata ?authorwikidata
WHERE { 
    ?work a schema:CreativeWork.
     OPTIONAL{
      ?work owl:sameAs ?workwikidata.
      FILTER( strstarts(STR(?workwikidata), "http://wikidata.dbpedia.org/resource/"))
      }
   OPTIONAL{
     ?work dbo:author ?author

     OPTIONAL{
      ?author owl:sameAs ?authorwikidata.
      FILTER( strstarts(STR(?authorwikidata), "http://wikidata.dbpedia.org/resource/"))
      }
}
}
LIMIT 10000
"""
dbpedia_authors_books = query_dbpedia(query)

offset = 0
while len(dbpedia_authors_books) % 10000 == 0:
    offset += 10000
    query_1 = query + """
    OFFSET %s
    """ % offset
    dbpedia_authors_books += query_dbpedia(query_1)

with open(os.path.expanduser("~/Desktop/dbpedia_authors_and_works.p"), "wb") as file:
    pickle.dump(dbpedia_authors_books, file)



# CREATE CHARACTER-PROPERTIES MATRIX
query = """
PREFIX dbc: <http://dbpedia.org/resource/Category:>
PREFIX dbo: <http://dbpedia.org/ontology/>
SELECT DISTINCT ?p
WHERE { 
    <%s> ?p ?o
}
LIMIT 10000

"""
propreties = list()
for character in characters:
    query_1 = query % character
    print(query_1)
    propreties.append({"character": character, "propreties": query_dbpedia(query_1)})

with open(os.path.expanduser("~/Desktop/dbpedia_properties_x_character.p"), "wb") as f:
    pickle.dump(propreties, f)

properties_set = list({p["p"] for item in propreties for p in item["propreties"]})
p_matrix = list()
for item in propreties:
    props = [p["p"] for p in item["propreties"]]
    row = {"character": item["character"]}
    row.update({el: el in props for el in properties_set})
    p_matrix.append(row)
pd.DataFrame(p_matrix).to_csv(os.path.expanduser("~/Desktop/dbpedia_character_properties_matrix.csv"))


wikidata_propreties_x_character = pd.read_csv(os.path.expanduser("~/Desktop/wikidata_propreties_x_character.csv"))
characters_set = list(set(wikidata_propreties_x_character["x"]))
properties_set = list(set(wikidata_propreties_x_character["p"]))
p_matrix = list()
for character in characters_set:
    row = {"character": character}
    props = wikidata_propreties_x_character.loc[wikidata_propreties_x_character["x"] == character]["p"].values.tolist()
    row.update({el: el in props for el in properties_set})
    p_matrix.append(row)
pd.DataFrame(p_matrix).to_csv(os.path.expanduser("~/Desktop/wikidata_character_properties_matrix.csv"))




# get authors books and characters
query ="""
SELECT DISTINCT *
WHERE {
?book_id a dbo:WrittenWork .
?book_id rdfs:label ?book .
OPTIONAL {
      ?book_id owl:sameAs ?book_wikidata.
      FILTER( strstarts(STR(?book_wikidata), "http://wikidata.dbpedia.org/resource/"))
}
?book_id dbo:author ?author_id .
?author_id rdfs:label ?author .
OPTIONAL {
      ?author_id owl:sameAs ?author_wikidata.
      FILTER( strstarts(STR(?author_wikidata), "http://wikidata.dbpedia.org/resource/"))
}
?character_id ?p ?book_id .
OPTIONAL {
      ?character_id owl:sameAs ?character_wikidata.
      FILTER( strstarts(STR(?character_wikidata), "http://wikidata.dbpedia.org/resource/"))
}
?character_id a dbo:FictionalCharacter .
?character_id rdfs:label ?character .
FILTER (lang(?book) = "" || langMatches(lang(?book), "en")) 
FILTER (lang(?author) = "" || langMatches(lang(?author), "en"))
FILTER (lang(?character) = "" || langMatches(lang(?character), "en")) .
}
LIMIT 10000
"""
dbpedia_authors_books_characters = query_dbpedia(query)

offset = 0
while len(dbpedia_authors_books_characters) % 10000 == 0:
    offset += 10000
    query_1 = query + """
    OFFSET %s
    """ % offset
    dbpedia_authors_books_characters += query_dbpedia(query_1)

with open(os.path.expanduser("~/Desktop/dbpedia_authors_and_writtenworks_characters.p"), "wb") as file:
    pickle.dump(dbpedia_authors_books_characters, file)
