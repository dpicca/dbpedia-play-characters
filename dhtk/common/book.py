# !/usr/local/bin/python
# -*- coding: utf-8 -*-
"""Contains the class describing a dhtk book."""

import pickle
from dhtk import LOGGER
from dhtk.common.author import Author


class Book:
    """
    The general book class of dhtk.

    Books implemented in submodules of dhtk should have this class as parent.
    """
    metadata = dict()
    get_repository = None

    def __init__(
            self,
            title,
            language,
            author=None,
            metadata=None,
            **kwargs
    ):
        """
        Init function of a Book.

        :param .author.Author author:
        :param str title:
        :param str editor:
        :param str publisher:
        :param str first_edition_date:
        :param int number_of_pages:
        :param dict metadata:
        :param set title_aliases:
        """
        LOGGER.debug("Book init args %s", (title, author, metadata, kwargs))
        if author:
            self._author = author
        else:
            self._author = Author("Anonymous")

        if isinstance(metadata, dict):
            self.metadata = metadata
        else:
            self.metadata = dict()

        if language:
            self._language = language
        else:
            LOGGER.error("A book needs a language!")
            raise ValueError("A book needs a language.")

        if title:
            self._title = title
        else:
            LOGGER.error("A book needs a title!")
            raise ValueError("A book needs a title.")

        # get data from kwargs
        if kwargs is not None:
            for key, value in kwargs.items():
                self.metadata[key] = value

    def get_author(self):
        """
        Return the book's author.

        :return .author.Author:
        """
        return self._author

    def get_title(self):
        """
        Return the book's title.

        :return str:
        """
        return self._title

    def get_language(self):
        """
        Return the book's title.

        :return str:
        """
        return self._language

    def get_editor(self):
        """
        Return the book's editor.

        :return str:
        """
        return self.metadata.get("editor", "")

    def get_publisher(self):
        """
        Return the book's publisher.

        :return str:
        """
        return self.metadata.get("publisher", "")

    def get_first_date(self):
        """
        Return the first edition date of the book.

        :return date:
        """
        return self.metadata.get("first_edition_date", "")

    def get_number_of_pages(self):
        """
        Return the number of pages of the book.

        :return int:
        """
        return self.metadata.get("number_of_pages", -1)

    def update_metadata(self, metadata):
        """
        Merge old metadata with new metadata.

        :param metadata:
        :return:
        """
        self.metadata.update(metadata)

    def get_metadata(self):
        """
        Return gathered medatata.

        :return dict:
        """
        return self.metadata

    def print_book_information(self):
        """
        Print information about the book.

        :return:
        """
        print("{:12}: {}".format("Title", self._title))
        print("{:12}: {}".format("Author", self._author.get_full_name()))
        print("{:12}:".format("Metadata"))
        for key, value in self.metadata.items():
            if isinstance(value, str):
                print(4 * " " + "- {:12}: {:>12}".format(key, value))
            elif isinstance(value, dict):
                print(4 * " " + "- {:12}:".format(key))
                for entry in value.values():
                    print(12 * " " + "- {}".format(entry))
            else:
                print(4 * " " + "- {:12}:".format(key))
                for entry in value:
                    print(12 * " " + "- {}".format(entry))

    def to_dict(self):
        """
        Return this object as a dictionary.

        :return:
        """
        return {
            "title": self._title,
            "author": self._author.to_dict(),
            "metadata": self.get_metadata()
        }

    def get_book_file_name(self):
        """
        Return a good filename for a book.

        :return str:
        """
        file_name = self.get_author().get_full_name() + "-" + self.get_title() + ".txt"
        return file_name.replace(" ", "_")

    def pickeled(self):
        """
        Return a pickled version of the book.

        :return:
        """
        return pickle.dumps(self, -1)

    def __eq__(self, other):
        """
        Equality function.

        :param Book other:
        :return bool:
        """
        return self._author == other.get_author() and self._title == other.get_title()

    def __ne__(self, other):
        """
        Inequality function.

        :param Book other:
        :return bool:
        """
        return not self.__eq__(other)

    def __hash__(self):
        """Return book hash."""
        return hash((self._author, self._title, self.get_first_date()))
