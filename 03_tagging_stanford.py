

for download_label in [
    "el",
    "fi",
    "sl",
    "cs",
    "pl",
    "sv",
    "pt",
    "nl",
    "ja",
    "no",
    "et",
    "ca",
    "en",
    "es",
    "la",
    "sr",
    "de",
    "da",
    "zh",
    "tl",
    "it",
    "eo",
    "nap",
    "hu",
    "fr",
]:
    try:
        if download_label in conll_shorthands:
            download_ud_model(download_label, resource_dir=resource_dir, confirm_if_exists=confirm_if_exists)
        elif download_label in default_treebanks:
            download_ud_model(default_treebanks[download_label], resource_dir=resource_dir, confirm_if_exists=confirm_if_exists)
    except:
        pass
import pickle
import csv
import os
import re
import stanfordnlp
from stanfordnlp.utils.resources import download_ud_model, conll_shorthands, default_treebanks
from segmenter.segmenter import TextSegmenter

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

        nlp = stanfordnlp.Pipeline(lang=book.get_language(), use_gpu=False )

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
