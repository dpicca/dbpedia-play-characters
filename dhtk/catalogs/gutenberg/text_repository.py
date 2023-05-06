# !/usr/local/bin/python
# -*- coding: utf-8 -*-
"""
Contains GutenbergTextRepository Class.

The cleaning of the texts was adapted from: https://github.com/okfn/gutenizer
"""

import os
import re
import shutil
from tempfile import mkdtemp

from dhtk import LOGGER
from dhtk.catalogs.text_repository import TextRepository
from dhtk.utils import download_file, url_exists, unarchive_book


class GutenbergTextRepository(TextRepository):
    """
    Clean up Gutenberg texts by removing all the header and footer bumpf.

    Usage: init and then run _extract_text.

    TODO: deal with 'Produced by ' which occurs in both header and footer (and
        so cannot be dealt with by the usual methods).
    TODO: Could probably be improved by:
        https://raw.githubusercontent.com/c-w/gutenberg/master/gutenberg/_domain_model/text.py
    TODO: Regex for formatting:
        part tiles:
            r"((?:(?:PART)|(?:Part))[ ][IVLX]+)[:.\s]"
        book titles:
            r"((?:(?:BOOK)|(?:Book))[ ][IVLX]+)[:.\s]"
        chapter titles:
            r"((?:(?:CHAPTER)|(?:Chapter))[ ][IVLX]+)[:.\s]+([\s\S+]*?\s{2})"
    TODO: chapter separation :
        Suggestion 1 (need to add a list of verbs in the negative lookahead parenthesis):
        r"(?<!\w| |,|\.|:|;|!|\?)((?:(?:CHAPTER)|(?:Chapter)|(?:Scene)|(?:SCENE))?[ ]?[IVLX1234567890]+[-:—\.\s]+?)(?=[\s\S+]*?\n{2})(?!(was|have|am|will|do))"
        Suggestion 1 (Compact):
        r"(?<![\w ,\.:;!\?])((?:(?:CHAPTER)|(?:Chapter)|(?:Scene)|(?:SCENE))?[ ]?[IVLX0-9]+[-:—\.\s]+?)(?=[\s\S+]*?\n{2})(?!(was|have|am|will|do))"

        Suggestion 2:
        r"(?<!\w|[ ]|,|\.|:|;|!|\?)((?:(?:CHAPTER)|(?:Chapter)|(?:Scene)|(?:SCENE))?[ ]?[IVLX1234567890]+[-:—\.\s]+?)(?=[\s\S+]*?\n{2})(?<! )(.+)"
        Suggestion 2 (compact):
        r"(?<![\w ,\.:;!\?])((?:(?:CHAPTER)|(?:Chapter)|(?:Scene)|(?:SCENE))?[ ]?[IVLX0-9]+[-:—\.\s]+?)(?=[\s\S+]*?\n{2})(?<! )(.+)"

        Suggestion 3: r"^[\n\r]{2,}[ 	]*(((?:(?:(CHAPTER|Chapter)[ ]?))?[IVXL\d]+[.: ]?[\n\r]*?.+)|([A-Z]+[A-Z '"-.,;:]*[A-Z:]))[\n\r]{2,}(?!(CHAPTER|Chapter))\w+"

    TODO: Footnotes:
        In-text footnotes:
        r"(\[(?:(?:FOOTNOTE)|(?:Footnote)|(?:footnote)|(?:FOOTNOTES)|(?:Footnotes)|(?:footnotes))[-:\.\n]+.+\])"
        End of text footnotes (add re.MULTILINE so that "^" will be considered as beginning of line, (re.compile(r"my_regex", re.MULTILINE))):
        r"(^(?:(?:FOOTNOTE)|(?:Footnote)|(?:footnote)|(?:FOOTNOTES)|(?:Footnotes)|(?:footnotes))(?:\s.*)+?)(?=\s\*)"
    TODO: Parts:
        Suggestion 1: r"((?:(?:PART)|(?:Part)|(?:part)|(?:ACT)|(?:Act)|(?:act))\s+[IVLX]+)[:.\s]"
    """

    _notes_end = ""
    _header_end = ""
    _footer_start = ""
    _original_text = ""
    _clean_text = ""
    _url = ""


    header_end_phrases = [
        "Project Gutenberg's Etext of",
        'This gutenberg_book was prepared by',
        'THE SMALL PRINT',
        'START OF THIS PROJECT GUTENBERG',
        'START OF THE PROJECT GUTENBERG EBOOK',
        'START OF THIS PROJECT GUTENBERG EBOOK',
    ]
    notes_start_phrases = ["Executive Director's Notes:"]
    notes_end_phrases = ['David Reed']
    footer_start_phrases = [
        'End of Project Gutenberg',
        'END OF THE PROJECT GUTENBERG EBOOK',
        'End of The Project Gutenberg',
        'END OF THIS PROJECT GUTENBERG EBOOK',
        'End of the Project Gutenberg EBook of',
    ]

    def __init__(self, repository_uri='file:///home/megloff1/Documents/aleph.gutenberg.org'):
        """
        Init function of the GutenbergTextRepository.

        Check repository_uri and create a temporary directory for file operations.

        :param str repository_uri:
        """
        if not repository_uri:
            raise ValueError("Please set the URI of a 'local' gutenberg text repository.")
        elif "http://www.gutenberg.org/files" in repository_uri:
            raise ValueError(
                """
                Please create a local repository. More information on:
                https://www.gutenberg.org/wiki/Gutenberg:Information_About_Robot_Access_to_our_Pages
                """
            )
        self._temporary_dir = mkdtemp(prefix="dhtk-")
        super().__init__(repository_uri)

    def get_original_text(self, book):
        """
        Return original text.

        :param book:
        :return:
        """
        found_url = False
        url = ""
        if self._original_text:
            return self._original_text

        base_url = self._repository_uri + "/" + book.get_file_uri()
        for extension in ("-0.txt", "-8.txt", "-8.txt", "-0.zip", "-8.zip", ".zip"):
            url = base_url + extension
            found_url = url_exists(url)
            if found_url:
                break


        # TODO: once search does not find audio editions anymore uncomment this:
        # if not found_url:
        #     raise Warning(
        #        "Could not find the text file for {} {}.".format(
        #           book.get_author(),
        #           book.get_title()
        #       )
        #    )
        # TODO: once search does not find audio anymore editions remove this:
        if not found_url:
            return None

        try:
            raw_file_path = download_file(url, os.path.join(
                self._temporary_dir,
                book.get_book_file_name()
            ))
            if raw_file_path.endswith(".zip"):
                self._original_text = unarchive_book(raw_file_path)
            else:
                with open(raw_file_path, "r", encoding="utf8", errors='ignore') as book_text_file:
                    self._original_text = book_text_file.read()
        except Exception as ex:
            raise ex
        return self._original_text

    def get_clean_text(self, book):
        """
        Return text whitoutj header, footer, notes or annotations.

        :param book:
        :return:
        """
        if not self._original_text:
            self.get_original_text(book)

        if not self._clean_text:
            self._clean()

        return self._clean_text

    def save_original_text_file_to(self, book, destination):
        """
        Save the clean text to a text-file in or at destination.

        :param book:
        :param destination:
        :return:
        """
        filename = book.get_book_file_name()
        filename = os.path.join(destination, filename)
        if os.path.exists(filename) and os.path.getsize(filename) == 0:
            return filename

        self.get_original_text(book)

        if not os.path.exists(os.path.dirname(destination)):
            raise FileNotFoundError("Verify your path! " + destination)

        if not os.path.isdir(destination):
            os.makedirs(destination)

        try:
            with open(filename, "w") as file_writer:
                file_writer.write(self._original_text)
        except IOError:
            LOGGER.warning("File %s could not be created.", filename)
        return filename

    def save_clean_text_file_to(self, book, destination):
        """
        Save the clean text to a text-file in or at destination.

        :param book:
        :param destination:
        :return:
        """
        self.get_original_text(book)

        self.get_clean_text(book)

        if not os.path.exists(os.path.dirname(destination)):
            raise FileNotFoundError("Verify your path! " + destination)

        if not os.path.isdir(destination):
            os.makedirs(destination)

        filename = book.get_book_file_name()

        filename = os.path.join(destination, filename)
        if not os.path.exists(filename) or os.path.getsize(filename) == 0:
            with open(filename, "w") as file_writer:
                file_writer.write(self._clean_text)

        return filename

    def _clean(self):
        """
        Remove header, footer, notes and annotations.

        :return:
        """
        # TODO: improve cleaning
        encoded_text = self._original_text
        # normalize the line endings to save us grief later
        encoded_text = encoded_text.replace('\r\n', '\n')
        self._clean_text = self._extract_text(encoded_text)

    @staticmethod
    def _make_re_from_phrase(phrase):
        """
        Make a regular expression that matches a phrase and its surrounding paragraph.

         i.e. that look like:
            ... phrase ....
            more _original_text
            [blank]
            [blank]+
        """
        paragraph_text = r'(^.+\w.+\n)*'  # need \S to ensure not just whitespace

        # TODO: check slowdown due to inclusion of '^.*' at start
        tmp = '^.*' + re.escape(phrase) + r'.*\n' + paragraph_text + r'\s+'
        return re.compile(tmp, re.I | re.M)  # make it case insensitive

    def _find_max(self, phrase, string):
        """
        Find farthest occurrence of string in phrase.

        :param phrase:
        :param string:
        :return:
        """
        max_index = 0
        regex = self._make_re_from_phrase(phrase)
        matches = regex.finditer(string)
        for match in matches:
            max_index = max(match.end(), max_index)
        return max_index

    def _find_min(self, phrase, string):
        """
        Find nearest occurrence of string in phrase.

        :param phrase:
        :param string:
        :return:
        """
        min_index = len(string)
        regex = self._make_re_from_phrase(phrase)
        matches = regex.finditer(string)
        for match in matches:
            min_index = min(match.start(), min_index)
        return min_index

    def _extract_text(self, encoded_text):
        """
        Extract the core _original_text.

        :param encoded_text:
        :return:
        """
        self._notes_end = self._get_notes_end(encoded_text)
        self._header_end = self._get_header_end(encoded_text)
        self._footer_start = self._get_footer_start(encoded_text)
        start_index = self._header_end
        if self._notes_end > 0:
            start_index = self._notes_end
        return str(encoded_text[start_index: self._footer_start].rstrip())

    def _get_notes_end(self, encoded_text):
        """
        Return 0 if no notes.

        :param encoded_text:
        :return:
        """
        indices = [self._find_max(phrase, encoded_text) for phrase in self.notes_end_phrases]
        index = max(indices)
        return index

    def _get_header_end(self, encoded_text):
        """
        Find the index of the end of the header.

        :param encoded_text:
        :return:
        """
        indices = [self._find_max(phrase, encoded_text) for phrase in self.header_end_phrases]
        return max(indices)

    def _get_footer_start(self, encoded_text):
        """
        Return the index of the beginnning of the footer.

        :param encoded_text:
        :return:
        """
        indices = [self._find_min(phrase, encoded_text) for phrase in self.footer_start_phrases]
        return min(indices)

    def __del__(self):
        """Remove temporary directory if instance is deleted."""
        shutil.rmtree(self._temporary_dir)

