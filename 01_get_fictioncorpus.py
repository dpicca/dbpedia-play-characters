# pylint: disable=invalid-name
"""
Example illustrating how to get plays from Gutenberg.
"""

import os.path
import pickle
from dhtk.common.corpus import Corpus
from dhtk.catalogs.gutenberg.search_triplet_store import GutenbergSearchTripletStore

gs = GutenbergSearchTripletStore()

"""
prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
prefix owl: <http://www.w3.org/2002/07/owl#>
prefix dbr: <http://dbpedia.org/resource/>
prefix pgterms: <http://www.gutenberg.org/2009/pgterms/>
prefix dcterms: <http://purl.org/dc/terms/>
prefix dcam: <http://purl.org/dc/dcam/>

SELECT DISTINCT ?bookshelf
WHERE 
{
?book_id pgterms:bookshelf [rdf:value ?bookshelf].
FILTER regex(str(?bookshelf), "School Stories", "i")   
}
ORDER BY ?bookshelf
"""

bookshelves = [
    "Fiction",
    "Adventure",
    "Horror",
    "Humor",
    "Western",
    "School Stories",
    "Fantasy",
    "FR Littérature",
    "FR Nouvelles",
    "DE Prosa",
    "IT Letteratura",
    "IT Romanzi",
]
subjects = [
    "Horror tales",
    "Adventure stories",
    "Fiction",
    "literature",

]

book_ids = list()
for bookshelve in bookshelves:
    book_ids.extend([item['book_id'] for item in gs.search_by_bookshelf(bookshelve)])

for subject in subjects:
    book_ids.extend([item['book_id'] for item in gs.search_by_subject(subject)])


books = set()
for book_id in set(book_ids):
    books.add(gs.book_from_book_id(book_id))

book_list = list()

if books:
    corpus = Corpus(
        "Fiction",
        description="books",
        corpora_path=os.path.expanduser("~/Desktop/"),
        book_list=books
    )
    corpus.download_book_corpus()


pickle.dump(corpus, open(os.path.expanduser("~/Desktop/fictioncorpus.p"), "wb"))
