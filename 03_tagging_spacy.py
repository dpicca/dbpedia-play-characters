import pickle
import csv
import os
import re

import spacy

from dhtk.catalogs.gutenberg.search_triplet_store import GutenbergSearchTripletStore
from collections import Counter
from segmenter.segmenter import TextSegmenter
gs = GutenbergSearchTripletStore()


# Corpora and out file paths
csv_file_path = os.path.expanduser("~/Desktop/data_table.csv")
lang_file_path = os.path.expanduser("~/Desktop/languages.txt")
corpus_base = os.path.expanduser("~/Desktop/")
corpora = [
    os.path.expanduser("~/Desktop/playcorpus.p"),
    os.path.expanduser("~/Desktop/fictioncorpus.p")
]


segmenter = TextSegmenter()

for corpus in corpora:
    corpus = pickle.load(open(corpus, "rb"))
    for book in corpus:
        language = book.get_language()

        if not language:
            next

        text = corpus.get_book_text(book)
        if not text:
            next

        out_file_path = os.path.join(os.path.expanduser("~/Desktop/Analyse"), book.get_book_id_number() + ".p")

        if os.path.exists(out_file_path):
            next

        text_blocks_indices, newline_blocks_indices, text_parts_indices = segmenter.get_text_parts(text)

        try:
            nlp = spacy.load(book.get_language())
        except:
            next

        data = list()

        for i in range(int(len(text_blocks_indices))):
            b, e = text_blocks_indices[i]
            doc = nlp(text[b:e])
            data.append({
                "p": str(i),
                "b": str(b),
                "e": str(e),
                "v": doc
            })
        with open(out_file_path, "wb") as file_path:
            pickle.dump(data, file_path)
