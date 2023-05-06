# pylint: disable=invalid-name
"""
Example illustrating how to get plays from Gutenberg.
"""

import os.path
import pickle
from dhtk.common.corpus import Corpus
from dhtk.catalogs.gutenberg.search_triplet_store import GutenbergSearchTripletStore

gs = GutenbergSearchTripletStore()



bookshelves = [
    "Plays",
    "DE Drama",
    "IT Teatro dialettale",
    "IT Teatro in prosa",
    "IT Teatro in versi",
    "FR Théâtre",
    "PT Teatro",
]
subjects = [
    "Plays",
    "Tragedies",
    "Drama",
    "Comedies",
    "Comedy"
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
        "Plays",
        description="books",
        corpora_path=os.path.expanduser("~/Desktop/"),
        book_list=books
    )
    corpus.download_book_corpus()


pickle.dump(corpus, open(os.path.expanduser("~/Desktop/playcorpus.p"), "wb"))
