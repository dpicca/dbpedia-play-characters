import re
import pandas as pd
from pprint import pprint
from numpy import cumsum
from itertools import groupby
from dhtk.catalogs.gutenberg.search_triplet_store import GutenbergSearchTripletStore


def get_separations(text):
    space_text = text.replace("\r", "\n")
    space_text = re.sub(r"[^\n]", "a", space_text)
    space_text = re.sub("a[\n]a", lambda m: "a" * len(m.group()), space_text, flags=re.MULTILINE)

    paragraphs = [(i, len(list(g))) for i, g in groupby("".join(space_text))]
    end_indexes = list(cumsum([d for _, d in paragraphs]))
    begin_indexes = end_indexes[:-1]
    begin_indexes.insert(0, 0)
    return list(zip(begin_indexes, end_indexes))




gs = GutenbergSearchTripletStore(sparql_endpoint="http://dhtk.unil.ch:3030/gutenberg")
books_found = gs.search_by_author("Charles")
for book in books_found:
    book = gs.book_from_book_id(book['bookid'])
    if book:
        title = book.get_title()
        raw_text = book.get_repository().get_original_text(book)

        if raw_text:
            df = pd.DataFrame(
                columns=[
                    'title',
                    'part_n',
                    'text',
                    'size',
                    'n_newlines',
                    'n_newlines_before',
                    'n_newlines_after',
                    'n_spaces_at_start',
                    'proportion_of_upper',
                    'proportion_of_text',
                    'numbers'
                ]
            )
            separations = list(get_separations(raw_text))[:]
            print("iterate")
            i = 0
            p_num = 0
            for b, e in separations[1:-1]:
                i += 1
                b_before, _ = separations[i-1]
                _, e_after = separations[i+1]
                text_part_before = raw_text[b_before:b]
                text_current = raw_text[b:e]
                text_part_after = raw_text[e:e_after]
                delta = e - b
                n_letters = sum(1 for letter in text_current if letter.isalpha())
                n_spaces_beginning = re.search("^[ ]+", text_current)
                if n_spaces_beginning:
                    n_spaces_beginning = n_spaces_beginning.end()
                else:
                    n_spaces_beginning = 0
                n_stars_beginning = re.search("^[*]+", text_current)
                if n_stars_beginning:
                    n_stars_beginning = n_stars_beginning.end()
                else:
                    n_stars_beginning = 0

                if len(text_current) != text_current.count("\n"):
                    p_num += 1
                    df1 = pd.DataFrame.from_dict({
                        'title': [title],
                        'part_n': p_num,
                        'text': [text_current],
                        'size': delta,
                        'n_newlines': text_current.count("\n")/delta,
                        'n_newlines_before': text_part_before.count("\n"),
                        'n_newlines_after': text_part_after.count("\n"),
                        'n_spaces_at_start': n_spaces_beginning,
                        'n_stars_at_start': n_stars_beginning,
                        'proportion_of_upper': n_letters and sum([1 for letter in text_current if letter.isupper()])/n_letters,
                        'proportion_of_text': n_letters/delta,
                        'numbers': bool(re.search(
                            r"(?:(?=[MDCLXVI])M*(C[MD]|D?C{0,3})(X[CL]|L?X{0,3})(I[XV]|V?I{0,3})?![ 'a-z][a-z])|([1-9]+)",
                        text_current)),
                    })
                    pprint(text_current)
                    df = pd.concat([df, df1])
            filename = "/home/megloff1/Desktop/dhtk/" + title + ".csv"
            df.to_csv(filename)


S