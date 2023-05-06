import os
import re
import pickle
import numpy as np
import pandas as pd
from rdflib import Graph, URIRef

def levenshtein(seq1, seq2):
    size_x = len(seq1) + 1
    size_y = len(seq2) + 1
    matrix = np.zeros ((size_x, size_y))
    for x in range(size_x):
        matrix[x, 0] = x
    for y in range(size_y):
        matrix[0, y] = y

    for x in range(1, size_x):
        for y in range(1, size_y):
            if seq1[x-1] == seq2[y-1]:
                matrix [x, y] = min(
                    matrix[x-1, y] + 1,
                    matrix[x-1, y-1],
                    matrix[x, y-1] + 1
                )
            else:
                matrix[x, y] = min(
                    matrix[x-1, y] + 1,
                    matrix[x-1, y-1] + 1,
                    matrix[x, y-1] + 1
                )
    return matrix[size_x - 1, size_y - 1]


g = Graph()
g.parse("sameas.rdf")

wikidata = pd.read_csv(os.path.expanduser("~/Desktop/wikidata_book_author_character.csv"))
dbpedia = pd.read_csv(os.path.expanduser("~/Desktop/dbpedia_authors_and_writtenworks_characters.csv")) # 15025




dbpedia["author_wikidata_id"] = dbpedia["author_wikidata"].apply(lambda x: str(x).replace("http://wikidata.dbpedia.org/resource/", "http://www.wikidata.org/entity/"))
dbpedia["book_wikidata_id"] = dbpedia["book_wikidata"].apply(lambda x: str(x).replace("http://wikidata.dbpedia.org/resource/", "http://www.wikidata.org/entity/"))

wikidata_in_dbpedia = pd.concat([wikidata.loc[(wikidata["author_id"] == str(row[1]["author_wikidata_id"])) & (wikidata["book_id"] == str(row[1]["book_wikidata_id"]))] for row in dbpedia.iterrows()]) #12260 / 35000


corpora = [
    os.path.expanduser("~/Desktop/playcorpus.p"),
    os.path.expanduser("~/Desktop/fictioncorpus.p")
]

found = list()
author_found = list()
not_found = list()
for corpus in corpora:
    corpus = pickle.load(open(corpus, "rb"))
    for book in corpus:
        book_id = book.get_book_id()
        book_id_num = book.get_book_id_number()
        title = book.get_title()
        author = book.get_author()
        author_name = author.get_full_name()
        author_id = author.get_gutenberg_id()
        language = book.get_language()

        dbpedia_author_id = ""
        try:
            dbpedia_author_id = str(list(g.objects(subject=URIRef(author_id), predicate=None))[0])
        except:
            pass

        if not dbpedia_author_id:
            try:
                dbpedia_author_id = dbpedia.loc[dbpedia["author"] == author_name]["author_id"].array[0]
            except:
                pass

        wikidata_author_id = ""
        if dbpedia_author_id:
            try:
                wikidata_author_id = dbpedia.loc[dbpedia["author_id"] == dbpedia_author_id]["author_wikidata_id"].array[0]
            except:
                pass

        if not wikidata_author_id:
            try:
                wikidata_author_id = wikidata.loc[wikidata["author"] == author_name]["author_id"].array[0]
            except:
                pass

        dbpedia_book_id = ""
        try:
            dbpedia_book_id = str(list(g.objects(subject=URIRef(book_id), predicate=None))[0])
        except:
            pass

        wikidata_book_id = ""
        if not dbpedia_book_id:
            try:
                dbpedia_book_id = dbpedia.loc[dbpedia["book"] == title]["book_id"].array[0]
            except:
                pass

        if dbpedia_book_id:
            try:
                wikidata_book_id = dbpedia.loc[dbpedia["book_id"] == dbpedia_book_id]["book_wikidata_id"].array[0]
            except:
                pass

        if not wikidata_book_id:
            try:
                wikidata_book_id = wikidata.loc[wikidata["book"] == title]["book_id"].array[0]
            except:
                pass

        if dbpedia_book_id or wikidata_book_id:
            found.append(
                {
                    "gutenberg_id_num": book_id_num,
                    "author": author_name,
                    "title": title,
                    "gutenberg_book_id": book_id,
                    "gutenberg_author_id": author_id,
                    "dbpedia_author": dbpedia_author_id,
                    "dbpedia_book": dbpedia_book_id,
                    "wikidata_author": wikidata_author_id,
                    "wikidata_book": wikidata_book_id,
                    "book_lang": language,
                }

            )
        elif dbpedia_author_id or wikidata_author_id:
            author_found.append(
                {
                    "gutenberg_id_num": book_id_num,
                    "author": author_name,
                    "title": title,
                    "gutenberg_book_id": book_id,
                    "gutenberg_author_id": author_id,
                    "dbpedia_author": dbpedia_author_id,
                    "dbpedia_book": dbpedia_book_id,
                    "wikidata_author": wikidata_author_id,
                    "wikidata_book": wikidata_book_id,
                    "book_lang": language,
                }

            )

        else:
            not_found.append(
                {
                    "gutenberg_id_num": book_id_num,
                    "author": author_name,
                    "title": title,
                    "gutenberg_book_id": book_id,
                    "gutenberg_author_id": author_id,
                    "dbpedia_author": dbpedia_author_id,
                    "dbpedia_book": dbpedia_book_id,
                    "wikidata_author": wikidata_author_id,
                    "wikidata_book": wikidata_book_id,
                    "book_lang": language,
                }

            )

columns = [
    "gutenberg_id_num",
    "author",
    "title",
    "book_lang",
    "gutenberg_book_id",
    "dbpedia_book",
    "wikidata_book",
    "gutenberg_author_id",
    "wikidata_author",
    "dbpedia_author"
]
pd.DataFrame(found).to_csv(
    os.path.expanduser("~/Desktop/found.csv"),
    header=True,
    columns=columns
)

pd.DataFrame(author_found).to_csv(
    os.path.expanduser("~/Desktop/author_found.csv"),
    header=True,
    columns=columns
)
pd.DataFrame(not_found).to_csv(
    os.path.expanduser("~/Desktop/not_found.csv"),
    header=True,
    columns=columns
)

detected_characters = pd.read_csv(os.path.expanduser("~/Desktop/data_table.csv"),header=None).dropna(axis=0, how="any") # 1782
detected_characters_nlp = pd.read_csv(os.path.expanduser("~/Desktop/data_table_nlp.csv"),header=None).dropna(axis=0, how="any") # 2101 rows


eg = [(i in detected_characters[0]) for i in detected_characters_nlp[0]]
detected_characters_nlp[eg] # 17 in common
eg = [(i in detected_characters_nlp[0]) for i in detected_characters[0]]
detected_characters[eg] # 95 in common
# ner not so useful for theatre.