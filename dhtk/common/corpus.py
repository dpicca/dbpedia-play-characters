# !/usr/local/bin/python
# -*- coding: utf-8 -*-
"""Contains the class for creating a book corpus."""


import os.path

from dhtk import LOGGER


class Corpus:
    """Create a corpus form books of type dhtk.common.Book."""

    def __init__(self, name, description="", corpora_path=None, book_list=None):
        """
        Init of the Corpus class.

        :param str name: name of the corpus
        :param str description: description of the corpus
        :param [dhtk.common.Book] book_list:
        :param str corpora_path: folder path to download/save corpus
        """
        self._name = name
        self._description = description
        if book_list:
            self._book_list = [book for book in book_list if book]
        else:
            self._book_list = set()

        try:
            if not corpora_path:
                corpora_path = input("Choose a directory path to save your corpora:")
            if not os.path.exists(corpora_path):
                os.mkdir(corpora_path)
            self._corpora_path = corpora_path
        except Exception:
            raise OSError("Can not find or create corpora path")

    def get_corpus_path(self):
        """
        Return the path containing the text files of the books in the corpus.

        :return:
        """
        return os.path.join(self._corpora_path, self._name)

    def get_name(self):
        """
        Return the name of the corpus.

        :return str:
        """
        return self._name

    def get_description(self):
        """
        Return the description of the corpus.

        :return str:
        """
        return self._description

    def get_book_list(self):
        """
        Return the list of books in the corpus.

        :return set:
        """
        return self._book_list

    def print_book_list(self):
        """
        Print list of books in the corpus.

        :return None:
        """
        for index, book in enumerate(self._book_list):
            author = book.get_author()
            author_full_name = author.get_full_name()
            book_title = book.get_title()
            print("{} {} {}".format(index, author_full_name, book_title))

    def add_book(self, book):
        """
        Add a book to the corpus.

        :param .book.Book book:
        :return: None
        """
        if book:
            self._book_list.add(book)
        else:
            LOGGER.error("This is not a book.")

    def add_books(self, book_list):
        """
        Add a list of books to the corpus.

        :param [.book.Book] book_list:
        :return: None
        """
        for book in book_list:
            self.add_book(book)

    @staticmethod
    def get_book_file_name(book):
        """
        Return a good filename for a book.

        :param .book.Book book:
        :return str:
        """
        return book.get_book_file_name()

    def remove_book(self, book):
        """
        Delete a book form the corpus.

        :param book: position of the book in the book_list
        :return: None
        """
        self._book_list.remove(book)
        file_path = os.path.join(self.get_corpus_path(), self.get_book_file_name(book))
        os.remove(file_path)

    def clear(self):
        """
        Delete all files and books in the corpus.

        :return: None
        """
        folder = self.get_corpus_path()
        for book_file in os.listdir(folder):
            os.remove(book_file)
        os.removedirs(folder)
        self._book_list.clear()

    def download_book(self, book):
        """
        Download a single book.

        :param .book.Book book:
        :return: None
        """
        corpus_path = self.get_corpus_path()
        if not os.path.exists(corpus_path):
            os.makedirs(corpus_path)

        filename = book.get_book_file_name()

        if not os.path.exists(os.path.join(corpus_path, filename)):
            book.get_repository().save_clean_text_file_to(
                book,
                corpus_path
            )
        else:
            LOGGER.info("File %s already exists in %s.", filename, corpus_path)

    def download_book_corpus(self):
        """
        Download the full corpus.

        :return: None
        """
        corpus_path = self.get_corpus_path()
        if not os.path.exists(corpus_path):
            os.mkdir(corpus_path)

        for book in self._book_list:
            repo = book.get_repository()
            # TODO: save clean text when cleaning works.
            repo.save_original_text_file_to(book, corpus_path)

    def get_book_file_name(self):
        """
        Return a good filename for a book.

        :return str:
        """
        file_name = self.get_author().get_full_name() + "-" + self.get_title() + ".txt"
        return file_name.replace(" ", "_")

    def get_book_text_file_path(self, book):
        """
        Return the text file path for a book in the corpus

        :param book:
        :return:
        """
        return os.path.join(self.get_corpus_path(), book.get_book_id_number() + ".txt")

    def get_book_text(self, book):
        """
        Return the text file path for a book in the corpus

        :param book:
        :return:
        """
        book_file_path = self.get_book_text_file_path(book)
        print(book_file_path)
        if not os.path.exists(book_file_path):
            self.download_book(book)
        text = ""
        with open(book_file_path, "r") as text_file:
            text = text_file.read()
        return text


    def __iter__(self):
        """
        Add capability to iterate over books in corpus.

        :return:
        """
        for book in self._book_list:
            yield book

    def __len__(self):
        """List length"""
        return len(self._book_list)

    def __str__(self):
        """Returns book_list in string format."""
        max_author_name_len = max([
            len(book.get_author().get_full_name()) for book in self._book_list
        ]) + 4
        format_string = "{}\t{:" + str(max_author_name_len) + "}\t{}"
        return "\n".join([
            format_string.format(
                i, book.get_author().get_full_name(), book.get_title()
            ) for i, book in enumerate(self._book_list)
        ])
