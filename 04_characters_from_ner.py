import os
import csv
import spacy
import pickle
from collections import Counter

tagged_files = os.listdir(os.path.expanduser("~/Desktop/Analyse"))

nlp = spacy.load('en')

csv_file_path = os.path.expanduser("~/Desktop/data_table_nlp.csv")

corpora = [
    os.path.expanduser("~/Desktop/playcorpus.p"),
    os.path.expanduser("~/Desktop/fictioncorpus.p")
]
types = ["play", "prose"]

for i, corpus in enumerate(corpora):
    with open(corpus, "rb") as corpus_file:
        corpus = pickle.load(corpus_file)

    tagged_file = tagged_files[1]
    for book in corpus:
        if book.get_book_id_number() + ".p" in tagged_files:
            tagged_file = book.get_book_id_number() + ".p"
        else:
            continue

        file_name = os.path.join(os.path.expanduser("~/Desktop/Analyse"), tagged_file)

        with open(file_name, "rb") as f:
            book_data = pickle.load(f)
        if not book_data:
            continue
        characters = list()

        book.print_book_information()
        for part in book_data:
            doc = part["v"]
            for ent in doc.ents:
                if ent.label_ == "PER":
                    characters.append(str(ent))
        characters = Counter(["".join(c) for c in characters])
        characters = set((c, n) for c, n in characters.items() if n >= 10)
        caracteristics = {
            "name": book.get_book_id_number(),
            "n_characters": len(characters),
            "type": types[i],
            "characters": "; ".join([" : ".join((t, str(n))) for t, n in characters])

        }
        print(characters)
        with open(csv_file_path, 'a') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=caracteristics.keys())
            writer.writerow(caracteristics)

