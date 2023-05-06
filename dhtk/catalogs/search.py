# !/usr/local/bin/python
# -*- coding: utf-8 -*-
"""Contains the Abstract Class Search."""

from abc import ABCMeta, abstractmethod


class Search(metaclass=ABCMeta):
    """
    Abstract method for search classes of the different catalog modules.

    This class should be used as parent for the classes implementing the search
    functions in submodules.
    """

    @abstractmethod
    def search_by_author(self, author_name, author_last_name):
        """
        Search book by author.

        :param str author_name:
        :param str author_last_name:
        :return [dhtk.common.book.Book]:
        """
        NotImplementedError(
            "Class %s doesn't implement search_by_author()" % self.__class__.__name__
        )

    @abstractmethod
    def search_by_title(self, title):
        """
        Search book by title.

        :param str title:
        :return [dhtk.common.book.Book]:
        """
        NotImplementedError(
            "Class %s doesn't implement search_by_author()" % self.__class__.__name__
        )

    @abstractmethod
    def search_by_title_and_author(self, title, auhtor_name, author_last_name):
        """
        Search by title and by author.

        :param str title:
        :param str auhtor_name:
        :param str author_last_name:
        :return:
        """
        NotImplementedError(
            "Class %s doesn't implement search_by_author()" % self.__class__.__name__
        )

    @abstractmethod
    def get_metadata(self, book):
        """
        Search and return metadata of a book in the catalog.

        :param dhtk.common.book.Book book:
        :return dict:
        """
        NotImplementedError(
            "Class %s doesn't implement search_by_author()" % self.__class__.__name__
        )
