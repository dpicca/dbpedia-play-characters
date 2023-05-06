# !/usr/local/bin/python
# -*- coding: utf-8 -*-
"""Contains the Abstract TextRepository Class."""

from abc import ABCMeta, abstractmethod

class TextRepository(metaclass=ABCMeta):
    """
    Abstract TextRepository Class.

    This class should be used as parent class for the text repositories of subclasses.
    """

    def __init__(self, repository_uri):
        """
        Init function of the repository class.

        :param str repository_uri: This uri can be of a directory
            (preceded by file: ) or of a remote localtion (http:)
        """
        self._repository_uri = repository_uri

    @abstractmethod
    def get_original_text(self, book):
        """
        Return the original text of the book.

        :param dhtk.common.book.Book book:
        :return str:
        """
        NotImplementedError(
            "Class %s doesn't implement get_original_text()" % self.__class__.__name__
        )

    @abstractmethod
    def get_clean_text(self, book):
        """
        Return a clean version of the text. Remove headers, footers, notes, and annotations.

        :param dhtk.common.book.Book book:
        :return str: Text of the book
        """
        NotImplementedError(
            "Class %s doesn't implement get_clean_text()" % self.__class__.__name__
        )

    @abstractmethod
    def save_clean_text_file_to(self, book, destination):
        """
        Save a clean version of the text to destination.

        Remove headers, footers, notes, and annotations.

        :param dhtk.common.book.Book book:
        :param str destination: Path of the directory or
        filename where to save the text of the book
        :return str: The path of the saved file
        """
        NotImplementedError(
            "Class %s doesn't implement save_clean_text_file_to()" % self.__class__.__name__
        )
