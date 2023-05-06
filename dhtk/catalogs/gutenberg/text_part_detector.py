"""
Text Part Detection

Detect all parts of a text, pars, books, chapters, index, notes

# TODO: detect index
# TODO: detect transcriber's notes


"""

import re

from dhtk import LOGGER

class TextPartDetector:
    """
    Should detect text parts of gutenberg books.
    """
    __raw_text = ""
    _header_indexes = None
    _text_indexes = None
    _footer_indexes = None
    _chapters_indexes = list()
    _notes_indexes = dict()
    _index_indexes = None
    _preface_indexes = None
    _cover_indexes = None

    def __init__(self, raw_text):
        if not raw_text or not isinstance(raw_text, str):
            raise TypeError

        self.__raw_text = raw_text

    def get_header_text_footer(self):
        """
        Return the indexes of the book, its header and its footer separately

        Focuses on the sets of ***[...]*** that often mark header/footer

        Example - Input:
        [Gutenberg's header]
        *** START OF THIS PROJECT GUTENBERG EBOOK DRACULA ***
        [Text of Dracula]
        *** END OF THIS PROJECT GUTENBERG EBOOK DRACULA ***
        [Gutenberg's footer]
        *** START: FULL LICENSE ***
        [License]

        Output:
        [Header including ***[START OF...]***]
        [Text of Dracula]
        [Footer including ***[END OF...]*** and ***[START: FULL LICENSE]***]

        :return: (header, texte_propre, footer)
        :rtype: (str, str, str)

        """

        text_len = len(self.__raw_text)
        regex = r"(^[*]{3,6}(?:[ ]|(?:[ ]{0,1}START)|(?:END)).+?[*]{3,6})" + \
                r"|(^[*](?:END).*[*](?:END)[*])"

        # TODO: Check for book_id < 10000 *END*THE SMALL PRINT...

        matches = list(re.finditer(regex, self.__raw_text, re.MULTILINE))
        one_third = text_len / 3
        if not matches:
            LOGGER.info("No text borders found.")
        elif len(matches) == 1:
            # The position of the match defines whether it is part of footer or header
            if matches[0].end(0) < one_third:
                self._header_indexes = (0, matches[0].end(0))
                self._text_indexes = (matches[0].end(0), -1)
            else:
                self._text_indexes = (0, matches[0].start(0))
                self._footer_indexes = (matches[0].start(0), -1)
        elif len(matches) == 2:
            # The book's text is between the two matches
            if matches[1].end(0) - matches[0].end(0) < text_len / 10:
                self._header_indexes = (0, matches[1].end(0))
                self._text_indexes = (matches[1].end(0), text_len)
            else:
                self._header_indexes = (0, matches[0].end(0))
                self._text_indexes = (matches[0].end(0), matches[1].start(0))
                self._footer_indexes = (matches[1].start(0), text_len)
        elif len(matches) == 3:
            # Second match's position define what is header and what is footer
            if matches[1].end(0) < one_third:
                self._header_indexes = (0, matches[1].end(0))
                self._text_indexes = (matches[1].end(0), matches[2].start(0))
                self._footer_indexes = (matches[2].start(0), text_len)
            else:
                self._header_indexes = (0, matches[0].end(0))
                self._text_indexes = (matches[0].end(0), matches[1].start(0))
                self._footer_indexes = (matches[1].start(0), text_len)
        elif len(matches) > 4:
            LOGGER.debug(
                "Too Many Matches:\n %s", (
                    str(match.start()) + " " + str(match.end()) + " " + match.group(0)
                    for match in matches
                )
            )

        return self._header_indexes, self._text_indexes, self._footer_indexes

    def get_chapters(self):
        """
        This function gets the chapters of a book previously downloaded.

        It returns a list containing n-tuple with
        the chapter title, its number and its content

        Example:

        self.__raw_text= "Produced by Daniel Lazarus, Jonesey, and David Widger
        MOBY-DICK;

        or, THE WHALE.

        By Herman Melville



        CONTENTS

        ETYMOLOGY.

        EXTRACTS (Supplied by a Sub-Sub-Librarian).

        CHAPTER 1. Loomings.
        CHAPTER 2. The Carpet-Bag.

        ....
        ...
        CHAPTER 2. The Carpet-Bag.

        I stuffed a shirt or two into my old carpet-bag, tucked it under my
        arm, and started for Cape Horn and the Pacific."


        output = get_chapters(self, self.__raw_text):
        print(output)
        [...,('CHAPTER 2. The Carpet-Bag.\n\n', '2', 'CHAPTER 2. The Carpet-Bag.

        I stuffed a shirt or two into my old carpet-bag, tucked it under my
        arm, and started for Cape Horn and the Pacific.",...),...]

        :return: list(tuple(title, chapter n°, content)) :
        Title --> the text of the title,
        Chapter n ---> the number of the chapter,
        Content --> Raw text of the content

        TODO: Find a list of verbs at the first person singular, to replace those at in line 28
        """

        # Initializations
        chapter_indices = list()
        chapters_number = list()
        chapters_content = list()
        chapters_title = list()
        regex = r"(?<!\w| |,|\.|:|;|!|\?)" \
                r"(?:(?:(?:CHAPTER)|(?:Chapter)|(?:Scene)|(?:SCENE))?[ ]?" \
                r"([IVLX1234567890]+)" \
                r"[-:—\.\s]+" \
                r"?(?!(mean|wrote|write|believe|suppose|would|was|have|am|will|do|think))" \
                r"([\s\S+]*?)\s{2})(?=[\s\S+]*?\n{2})"
        # Setting up the regex to match chapters/parts
        chap_regex = re.compile(regex, re.MULTILINE)
        # chap_num_regex = re.compile(r"[IVLX1234567890]+")

        # Searching every chapter in the text
        chapter_beginning = re.finditer(chap_regex, self.__raw_text)

        # If any, for every chapter, get the chapter title, number and content
        if chapter_beginning:
            for chapter in chapter_beginning:
                # Getting the indice of the start of the chapter
                chapter_indices.append(chapter.start())

                # Getting chapter number (first capturing group)
                if chapter.group(0):
                    chapters_number.append(chapter.group(0))
                else:
                    # If no chapter number, append None (easier to process after)
                    chapters_number.append(None)

                # Getting chapter title
                if chapter.group(1):
                    chapters_title.append(chapter.group(1))
                else:
                    chapters_title.append(None)

            # Getting chapter parts with indices
            for i, chapter_index in enumerate(chapter_indices):
                # If it is not the last one get chapter content from an indice to the next one
                if i != len(chapter_indices) - 1:
                    chapters_content.append(self.__raw_text[chapter_index:chapter_indices[i + 1]])
                # If it is the last indice, gets the chapter content from the indice to the end
                else:
                    chapters_content.append(self.__raw_text[chapter_index:])

        return zip(chapters_number, chapters_title, chapters_content)

    def get_footnotes(self):
        """
        This function gets the footnotes

        :param self.__raw_text
        :return tuple([in-text-footnotes],[end-of-text-footnotes])

        Example :
        input: full book text
        output: (
            ["[Footnote 1: Dharma is acquisition of religious merit,...",...],
            ["Footnotes: Footnote 1: Games of strength...",...]
        )
        """

        # Initializing lists
        in_text_footnotes_list = list()
        end_of_the_text_footnotes_list = list()

        # Setting up the regex to match in-text footnotes
        in_text_footnotes_regex = re.compile(
            r"(\[(?:(?:FOOTNOTE)|(?:Footnote)|(?:footnote)|"
            r"(?:FOOTNOTES)|(?:Footnotes)|(?:footnotes))"
            + r"[-:.\n]+.+\])",
            re.MULTILINE)

        # Setting up the regex to match end-of-the-text footnotes
        end_of_the_text_footnotes_regex = re.compile(
            r"(^(?:(?:FOOTNOTE)|(?:Footnote)|(?:footnote)|"
            r"(?:FOOTNOTES)|(?:Footnotes)|(?:footnotes))"
            + r"(?:\s.*)+?)(?=\s\*)",
            re.MULTILINE)

        # Searching every in-text footnotes in the text
        in_text_footnotes = re.finditer(in_text_footnotes_regex, self.__raw_text)

        # Searching every end-of-the-text footnotes in the text
        end_of_the_text_footnotes = re.finditer(end_of_the_text_footnotes_regex, self.__raw_text)

        # Lists the in-text footnotes, if there are any
        if in_text_footnotes:
            for in_text_footnote in in_text_footnotes:
                in_text_footnotes_list.append(in_text_footnote.group())

        # Lists the end-text footnotes, if there are any
        if end_of_the_text_footnotes:
            for end_of_the_text_footnote in end_of_the_text_footnotes:
                end_of_the_text_footnotes_list.append(end_of_the_text_footnote.group())

        # Returns a Tuple with both lists, if both are full
        if in_text_footnotes_list and end_of_the_text_footnotes_list:
            return in_text_footnotes_list, end_of_the_text_footnotes_list

        # Returns a Tuple with the first list
        if in_text_footnotes_list and not end_of_the_text_footnotes_list:
            return in_text_footnotes_list, None

        # Returns a Tuple with the second list
        if not in_text_footnotes_list and end_of_the_text_footnotes_list:
            return None, end_of_the_text_footnotes_list

        # If none of the above: a.k.a. both lists are empty, return a Tuple with None and None
        LOGGER.info("No footnotes were found!")
        return None, None

    def get_books(self):
        """
        This function gets the books

        :return: list(tuple(book number, content)):

        Example:

        self.__raw_text = '''
        Project Gutenberg's The Poetical Works of John Milton, by John Milton

        ...

        Title: The Poetical Works of John Milton

        Author: John Milton

        Release Date: May, 1999  [Etext #1745]
        Posting Date: November 10, 2014

        Language: English


        *** START OF THIS PROJECT GUTENBERG EBOOK THE POETICAL WORKS OF JOHN MILTON ***




        Produced by Donal O'Danachair





        THE POETICAL WORKS OF JOHN MILTON

        By John Milton



        ...

        PARADISE LOST.

        ON Paradise Lost.

        THE VERSE.

        BOOK I.

        BOOK II.

        BOOK III.

        ...

        BOOK III.


          THE ARGUMENT.

        God sitting on his Throne sees Satan flying towards this world, then
        newly created; shews him to the Son who sat at his right hand;
        foretells the success of Satan in perverting mankind; clears his own
        Justice and Wisdom from all imputation, having created Man free and able
        enough to have withstood his Tempter; yet declares his purpose of grace
        towards him, in regard he fell not of his own malice, as did Satan, but
        by him seduc't.

        '''

        output = get_books()
        print(output)
        [...,('III', "BOOK III.\n\n\n  THE ARGUMENT.\n
            \nGod sitting on his Throne sees Satan flying towards this world,"),...]
        """

        # Initializations of empty lists
        book_indices = list()
        book_number = list()
        book_content = list()
        regex = r"((?:(?:BOOK)|(?:Book))[ ][IVLX\d]+)[:.\s]"
        num_regex = r"[IVLX\d]+"

        # Setting up the regex to match "books"
        books_regex = re.compile(regex, re.MULTILINE)
        books_num_regex = re.compile(num_regex, re.MULTILINE)
        # Searching every book in the serie
        book_beginning = re.finditer(books_regex, self.__raw_text)
        # For every book, get the entire book
        if book_beginning:
            for book in book_beginning:
                book_indices.append(book.start())
                number = re.search(books_num_regex, book.group())
                if number:
                    book_number.append(number.group())

            for i, book_index in enumerate(book_indices):
                if i != len(book_indices) - 1:
                    book_content.append(self.__raw_text[book_index:book_indices[i + 1]])
                else:
                    book_content.append(self.__raw_text[book_index:])

        return zip(book_number, book_content)

    def get_parts(self):
        """
        This function gets the parts of the text and return their number and content.

        :return: list(tuple(part n°, content))

        Example :
        input: full book text
        output: [...,('ACT III.', "ACT III.  Drawing-Room at the Manor House, Woolton...),...]
        """

        # Initializing lists
        parts_index = list()
        parts_number = list()
        parts_content = list()

        # Creating regex
        regex = r"(?<!\w| |,|\.|:|;|!|\?)" \
                r"(?:((?:(?:PART)|(?:Part)|(?:part)|" \
                r"(?:ACT)|(?:Act)|(?:act))\s+[IVLX]+)[:.\s]" \
                + r"([\s\S+]*?))(?=[\s\S+]*?\n{2})"

        # Setting up regex to find parts
        parts_regex = re.compile(regex, re.MULTILINE)

        # searching for parts
        parts_start = re.finditer(parts_regex, self.__raw_text)

        # If there are any parts
        if parts_start:
            for part in parts_start:
                # Getting part beginning
                parts_index.append(part.start())

                # Getting part number
                if part.group(0):
                    parts_number.append(part.group(0))
                # If no part number, append None (so that it is easier to process after)
                else:
                    parts_number.append(None)

            # Getting parts content
            for i, part_index in enumerate(parts_index):
                # If it is not the last one get part content from an index to the next one
                if i != len(parts_index) - 1:
                    parts_content.append(self.__raw_text[part_index:parts_index[i + 1] - 1])
                # If it is the last index, gets the chapter content from the index to the end
                else:
                    parts_content.append(self.__raw_text[part_index:])

        return zip(parts_number, parts_content)
