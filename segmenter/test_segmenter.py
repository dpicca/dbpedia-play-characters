from glob import glob
from pprint import pprint
from random import shuffle

from scripts.segmenter import TextSegmenter
from scripts.utils import unarchive_book


books_found = sorted(glob("/home/megloff1/Documents/aleph.gutenberg.org/*/*/*/*/*.zip"))
books_done = [filename.rsplit("/", 1)[1].replace(".csv", ".zip") for filename in glob("/home/megloff1/Documents/book_parts/*.csv")]
books_found = [path for path in books_found if path.rsplit("/", 1)[1] not in books_done]

segmenter = TextSegmenter()

shuffle(books_found)

for book in books_found[0:10]:
    if book:
        raw_text = unarchive_book(book)
        title = book.rsplit("/", 1)[1].replace(".zip", "")
        if raw_text:
            print()
            text_blocks_indices, newline_blocks_indices, text_parts_indices = segmenter.get_text_parts(raw_text)
            for i in range(int(len(text_blocks_indices))):
                b, e = text_blocks_indices[i]
                pprint(raw_text[b:e])
                for m in segmenter.get_roman_numbers(raw_text[b:e]):
                    mb, me, n = m
                    pprint(raw_text[b+mb:b+me])
                for m in segmenter.get_numbers(raw_text[b:e]):
                    mb, me, n = m
                    pprint(raw_text[b+mb:b+me])
                for m in segmenter.get_nonalpha_sequences(raw_text[b:e]):
                    mb, me, n = m
                    pprint(raw_text[b+mb:b+me])
                for m in segmenter.get_parentesis(raw_text[b:e]):
                    mb, me, n = m
                    pprint(raw_text[b+mb:b+me])
                for m in segmenter.get_quoted(raw_text[b:e]):
                    mb, me, n = m
                    pprint(raw_text[b+mb:b+me])
                for m in segmenter.get_upper_sequences(raw_text[b:e]):
                    mb, me, n = m
                    pprint(raw_text[b+mb:b+me])
                print()
        try:
            input("Press enter to continue")
        except SyntaxError:
            pass

