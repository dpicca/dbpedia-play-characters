import pickle
import csv
import os
import re
from segmenter.segmenter import TextSegmenter
from dhtk.catalogs.gutenberg.search_triplet_store import GutenbergSearchTripletStore
from collections import Counter

gs = GutenbergSearchTripletStore()

# config stanford dowload
confirm_if_exists = False
resource_dir = os.path.expanduser("~/stanfordnlp_resources")



# Corpora and out file paths
csv_file_path = os.path.expanduser("~/Desktop/data_table.csv")
lang_file_path = os.path.expanduser("~/Desktop/languages.txt")
corpus_base = os.path.expanduser("~/Desktop/")
corpora = [
    os.path.expanduser("~/Desktop/playcorpus.p"),
    os.path.expanduser("~/Desktop/fictioncorpus.p")
]


regex = r"(?:(?:(?:^|^\s+)((?:\d\. ){0,1}(?:[A-Z]+. |[A-Z]+ ){0,2}(?:[A-Z]+))(?=(?:_\(.+\)_){0,1}\.(?: |:|-|—|--)?(?= )))|(?:(?:^[ ]*)_(\w+|\s){1,4}_$)|(?:^((?:[A-Z]+ ){0,3}[A-Z]+)(?=:|\.|$))|(?:^(?:\s*)(?:_|=|\*)?([A-Za-z'’ ]+)(?::_|\._|\.=|\.\*|:)(?:$| ))|(?:^\s+([A-Za-z]+)(?=\.|$))|(?:^_(\w+)_\. .{10,})|(?:^([A-Z][a-z]\.$))|(?:([A-Z ]+)(?:--))|(?:^_)([A-Za-z]+)(?:_\.--)|(?:(?:^\()([A-Za-z ]+)(?:.\)))|(?:\s+([A-Z]+)\:))"

regex = re.compile(
    regex,
    re.M | re.U
)

segmenter = TextSegmenter()
languages = set()
if not os.path.exists(csv_file_path):
    for corpus in corpora:
        corpus = pickle.load(open(corpus, "rb"))
        for book in corpus:
            language = book.get_language()

            if not language:
                next

            languages.add(language)

            text = corpus.get_book_text(book)
            if not text:
                next

            lines = len(re.findall(r"[\r\n]+", text))
            if lines == 0:
                next

            characters = regex.findall(text)
            characters = Counter(["".join(c) for c in characters])
            characters = set((c, n) for c, n in characters.items() if n >= 10)
            parts, _, _ = segmenter.get_text_parts(text)
            caracteristics = {
                "name": book.get_book_id_number(),
                "type": corpus.get_name(),
                "lang": book.get_language(),
                "n_parts": len(parts),
                "txt_len": len(text),
                "n_characters": len(characters),
                "characters": "; ".join([" : ".join((t, str(n))) for t, n in characters])
            }

            with open(csv_file_path, 'a') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=caracteristics.keys())
                writer.writerow(caracteristics)

    with open(lang_file_path, "w") as f:
        f.write("\n".join(list(languages)))
