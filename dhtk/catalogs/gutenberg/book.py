# !/usr/local/bin/python
# -*- coding: utf-8 -*-
"""Contains the GutenbergBook Class."""

import re

from dhtk import LOGGER
from dhtk.common.book import Book
from dhtk.catalogs.gutenberg.text_repository import GutenbergTextRepository


class GutenbergBook(Book):
    """Extends the Book class for Project Gutenberg books."""

    # Reference to own repository
    get_repository = GutenbergTextRepository

    def __init__(
            self,
            gutenberg_id,
            title,
            author,
            language,
            **kwargs
    ):
        """
        Init function of the GutenbergBook Class.

        :param gutenberg_id: has to start with "http://www.gutenberg.org/ebooks/"
        :param author: class of type Author
        :param title: title of the book
        :param metadata: dictionary of dbpedia e.g. {publisher: "book's publisher",
        editor:"book's editor"}
        """
        id_format = re.compile(r"http://www.gutenberg.org/ebooks/\d+$")
        if not id_format.fullmatch(gutenberg_id):
            LOGGER.error("This gutenberg id is not valid! %s", gutenberg_id)
            raise ReferenceError("This gutenberg id is not valid! %s" % gutenberg_id)

        title = re.sub(r"\s+", " ", title)
        super().__init__(title=title, author=author, gutenberg_id=gutenberg_id, language=language, metadata=kwargs)

    def get_book_id(self):
        """
        Return the gutenberg id uri of the book.

        :return:
        """
        return self.metadata.get("gutenberg_id", "")

    def get_book_id_number(self):
        """
        Return Gutenberg ID without full url.
        :return:
        """
        return self.metadata.get("gutenberg_id", "/").rsplit("/", 1)[1]

    def get_file_uri(self):
        """
        Return the suffix of the uri of the book in a gutenberg text repository.

        :return:
        """
        LOGGER.debug("id: %s", self.metadata.get("gutenberg_id", ""))
        gutenberg_id_num = self.get_book_id_number()
        if int(gutenberg_id_num) < 10:
            subdir = "0/{0}/{0}".format(gutenberg_id_num)
        elif int(gutenberg_id_num) < 100:
            subdir = "{0}/{1}/{1}".format(gutenberg_id_num[0], gutenberg_id_num)
        elif int(gutenberg_id_num) < 1000:
            subdir = "{0}/{1}/{2}/{2}".format(
                gutenberg_id_num[0],
                gutenberg_id_num[1],
                gutenberg_id_num
            )
        else:
            gutenberg_id_string = str(gutenberg_id_num).zfill(2)
            all_but_last_digit = list(gutenberg_id_string[:-1])
            subdir_part = "/".join(all_but_last_digit)
            subdir = "{0}/{1}/{1}".format(subdir_part, gutenberg_id_num)
        return subdir

    def get_book_file_name(self):
        """
        Return a good filename for a book.

        :return str:
        """
        return self.get_book_id_number() + ".txt"

    def __eq__(self, other):
        """
        Equality function.

        :param other:
        :return:
        """
        if isinstance(other, GutenbergBook):
            equals = self.get_book_id() == other.get_book_id()
        else:
            equals = super().__eq__(other)
        return equals

    def __hash__(self):
        """Return book hash."""
        return hash((self._author, self._title, self.get_first_date()))
