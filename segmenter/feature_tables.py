
import re
from glob import glob
import pandas as pd
from pprint import pprint
from numpy import cumsum
from itertools import groupby
import zipfile
from .segmenter import TextSegmenter
from .utils import unarchive_book

data_path = "../devided_texts/"
save_path = "../feauture-selection/"

# all_books = sorted(glob("/home/megloff1/Documents/aleph.gutenberg.org/*/*/*/*/*.zip"))
# books_done = [filename.rsplit("/", 1)[1].replace(".csv", ".zip") for filename in glob(save_path +"*.csv")]
# books_found = [path for path in all_books if path.rsplit("/", 1)[1] not in books_done]

for csv_file in glob(data_path + "*.csv"):
    df = pd.read_csv(csv_file)
    for i, row in df.iterrows():
        if i == 0:
            continue
        # TODO: add features to df and save df




        # if raw_text:
        #     df = pd.DataFrame(
        #         columns=[
        #             'title',
        #             'part_n',
        #             'text',
        #             'size',
        #             'n_newlines',
        #             'n_newlines_before',
        #             'n_newlines_after',
        #             'n_spaces_at_start',
        #             'proportion_of_upper',
        #             'proportion_of_text',
        #             'numbers'
        #         ]
        #     )
        #     separations = list(get_separations(raw_text))[:]
        #     print("iterate")
        #     i = 0
        #     p_num = 0
        #
        #     for b, e in separations[1:-1]:
        #         i += 1
        #
        #         b_before, _ = separations[i-1]
        #         _, e_after = separations[i+1]
        #
        #         text_part_before = raw_text[b_before:b]
        #         text_current = raw_text[b:e]
        #         text_part_after = raw_text[e:e_after]
        #
        #         delta = e - b
        #         n_letters = sum(1 for letter in text_current if letter.isalpha())
        #         n_spaces_beginning = re.search("^[ ]+", text_current)
        #         if n_spaces_beginning:
        #             n_spaces_beginning = n_spaces_beginning.end()
        #         else:
        #             n_spaces_beginning = 0
        #         n_stars_beginning = re.search("^[*]+", text_current)
        #         if n_stars_beginning:
        #             n_stars_beginning = n_stars_beginning.end()
        #         else:
        #             n_stars_beginning = 0
        #
        #
        #         number_of_quotes = 0
        #         quotes = re.match('[\'"]')
        #         # detect numbers
        #         numbers_count = 0
        #         begins_with_n_number = 0
        #         ends_with_n_number = 0
        #
        #         roman_numbers_upper = re.match(
        #             r"(?:(?=[MDCLXVI])M*(C[MD]|D?C{0,3})(X[CL]|L?X{0,3})(I[XV]|V?I{0,3})?![ 'a-z][a-z])", text_current)
        #         roman_numbers_lower = re.match(
        #             r"(?:(?=[mdclxvi])m*(c[md]|d?c{0,3})(x[cl]|l?x{0,3})(i[xv]|v?i{0,3})?![ 'a-z][a-z])", text_current)
        #         numeric = re.match("[1-9'`´.,]+", text_current)
        #         if roman_numbers_lower or roman_numbers_upper or numeric:
        #
        #
        #
        #         if len(text_current) != text_current.count("\n") + text_current.count("\r"):
        #             p_num += 1
        #             df1 = pd.DataFrame.from_dict({
        #                 'title': [title],
        #                 'part_n': p_num,
        #                 'text': [text_current],
        #                 'size': delta,
        #                 'n_spaces_at_start': n_spaces_beginning,
        #                 'n_stars_at_start': n_stars_beginning,
        #                 'n_numbers_at_start': begins_with_n_number,
        #                 'n_numbers_at_end': ends_with_n_number,
        #                 '%_of_upper': n_letters and sum([1 for letter in text_current if letter.isupper()])/n_letters,
        #                 '%_of_text': n_letters/delta,
        #                 '%_numbers':    numbers_count/delta,
        #                 'n_of_newlines': text_current.count("\n"),
        #                 '%_newlines': text_current.count("\n") / delta,
        #                 '%_newlines_before': text_part_before.count("\n") / len(text_part_before),
        #                 '%_newlines_after': text_part_after.count("\n") / len(text_part_after),
        #             })
        #             # pprint(text_current)
        #             df = pd.concat([df, df1])
        #     filename = "/home/megloff1/Documents/book_parts/" + title + ".csv"
        #     df.to_csv(filename)