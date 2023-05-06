
import re

from numpy import cumsum
from itertools import groupby, chain


class TextSegmenter:
    """ Segments text. """

    def get_newline_char(self, text):
        """ Detect newline character

        Windows:\r\n
        Unix: \n
        """

        if "\r\n" in text:
            return "\r\n"
        else:
            return "\n"

    def get_text_parts(self, text):
        """ Detect parts of text separated by more than one newline and blocks of only newlines"""
        new_line_char = self.get_newline_char(text)
        space_text = re.sub(r"[^%s]" % new_line_char, "a", text)
        space_text = re.sub(r"a\%sa" % new_line_char, lambda m: "a" * len(m.group()), space_text, flags=re.MULTILINE)
        if new_line_char == "\r\n":
            space_text = space_text.replace("\r\n", "\n\n")
        text_part_lengths = [len(list(g)) for _, g in groupby(space_text)]
        end_indexes = list(cumsum([d for d in text_part_lengths]))
        begin_indexes = end_indexes[:-1]
        begin_indexes.insert(0, 0)
        text_parts_indices = list(zip(begin_indexes, end_indexes))
        newline_blocks_indices = [(b, e) for b, e in text_parts_indices if space_text[b:e].count("\n") == e - b]
        text_blocks_indices = [indicies for indicies in text_parts_indices if indicies not in newline_blocks_indices]
        return text_blocks_indices, newline_blocks_indices, text_parts_indices

    def get_numbers(self, text):
        numbers = re.compile(
            "[-+]?(?!0+\.00)(?=.{1,9}([.]|[ ]))?(?!0(?![.]))*\d{1,}([,'`´]\d{1,3})*([.]\d+)*([eE][-+]?[0-9]+)?"
        )
        return ((match.start(), match.end(), match.group()) for match in numbers.finditer(text))

    def get_roman_numbers(self, text, filter=True):
        """
        Get roman numerals.

        Care matches CD in CD-ROM
        Can match names or I in text if not careful.
        TODO: better filters for one char mathches.

        :param text:
        :return:
        """
        roman_numbers = re.compile(
            r"(?<=\b)(?=[MDCLXVI])M*(C[MD]|D?C{0,3})(X[CL]|L?X{0,3})(I[XV]|V?I{0,3})(?=\b)"
        )

        if not filter:
            return ((match.start(), match.end(), match.group()) for match in roman_numbers.finditer(text)
                 if match.group())
        else:

            following_capitalised = r"[A-Z][a-z]+[ ]"
            following_uppercase = r"[A-Z]+"
            return (
                (match.start(), match.end(), match.group()) for match in roman_numbers.finditer(text)
                if match.group() and (len(match.group()) > 1 or (
                        #Case match length == 1
                        not (
                            re.search(r"[a-z]", text[match.end():match.end()+1]) or
                            re.search(r"[ ][a-z]", text[match.end():match.end() + 2])
                        )
                        and (
                            re.search(following_capitalised + match.group(), text[match.start()-10:match.end()]) or
                            re.search(following_uppercase + match.group(), text[0:match.end()]) or
                            re.search(
                                r"\s{2,}"+match.group()+"(?=\s{2,}|" + self.get_newline_char(text)+")",
                                text[match.start()-10:match.end()+3]
                            ) or
                            re.fullmatch(r"[.][ ][A-Z([]", text[match.end():match.end() + 3])
                        )
                    )
                )
            )

    def get_quoted(self, text):
        regex = re.compile(
            r'(".*?")',
            flags=(re.MULTILINE | re.DOTALL)
        )
        match1 = ((match.start(), match.end(), match.group())
                for match in regex.finditer(text))

        regex = re.compile(
            r"('.*?')",
            flags=(re.MULTILINE | re.DOTALL)
        )
        match2 = ((match.start(), match.end(), match.group())
                for match in regex.finditer(text))

        regex = re.compile(
            r"(«.*?»)",
            flags=(re.MULTILINE | re.DOTALL)
        )
        match3 = ((match.start(), match.end(), match.group())
                for match in regex.finditer(text))

        regex = re.compile(
            r"(“.*?”)",
            flags=(re.MULTILINE | re.DOTALL)
        )
        match4 = ((match.start(), match.end(), match.group())
                  for match in regex.finditer(text))

        return chain(match1, match2, match3, match4)

    def get_parentesis(self, text):
        regex = re.compile(
            r"[(].*?[)]",
            flags=(re.MULTILINE | re.DOTALL)
        )
        match1 = ((match.start(), match.end(), match.group())
                for match in regex.finditer(text))

        regex = re.compile(
            r"[[].*?[\]]",
            flags=(re.MULTILINE | re.DOTALL)
        )
        match2 = ((match.start(), match.end(), match.group())
                for match in regex.finditer(text))

        regex = re.compile(
            r"[{].*?[}]",
            flags=(re.MULTILINE | re.DOTALL)
        )
        match3 = ((match.start(), match.end(), match.group())
                for match in regex.finditer(text))

        return chain(match1, match2, match3)

    def get_nonalpha_sequences(self, text):
        regex = re.compile("[^\d\s[A-Za-z]{3,}", flags=re.UNICODE)
        return ((match.start(), match.end(), match.group())
                for match in regex.finditer(text))

    def get_upper_sequences(self, text):
        regex = re.compile("[A-Z][A-Z -:]{2,}", flags=re.UNICODE)
        return ((match.start(), match.end(), match.group())
                for match in regex.finditer(text))

    def get_whitespace_sequences(self, text):
        regex = re.compile("[ ]{2,}")
        return ((match.start(), match.end(), match.group())
                for match in regex.finditer(text))

    def line_count(self, text):
        newline_char = self.get_newline_char(text)
        return text.count(newline_char) + 1

    def get_header_text_footer(self, text):
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

        text_len = len(text)
        regex = r"(^[*]{3,6}(?:[ ]|(?:[ ]{0,1}START)|(?:END)).+?[*]{3,6})" + \
                r"|(^[*](?:END).*[*](?:END)[*])"

        # TODO: Check for bookid < 10000 *END*THE SMALL PRINT...
        header_indexes, text_indexes, footer_indexes = None, None, None
        matches = list(re.finditer(regex, text, re.MULTILINE))
        one_third = text_len / 3
        if not matches:
            print("No text borders found.")
            pass
        elif len(matches) == 1:
            """
            The position of the match defines whether it is part of footer or header
            """
            if matches[0].end(0) < one_third:
                header_indexes = (0, matches[0].end(0))
                text_indexes = (matches[0].end(0), -1)
            else:
                text_indexes = (0, matches[0].start(0))
                footer_indexes = (matches[0].start(0), -1)
        elif len(matches) == 2:
            """ 
            The book's text is between the two matches
            """
            if matches[1].end(0) - matches[0].end(0) < text_len / 10:
                header_indexes = (0, matches[1].end(0))
                text_indexes = (matches[1].end(0), text_len)
            else:
                header_indexes = (0, matches[0].end(0))
                text_indexes = (matches[0].end(0), matches[1].start(0))
                footer_indexes = (matches[1].start(0), text_len)
        elif len(matches) == 3:
            # Second match's position define what is header and what is footer
            if matches[1].end(0) < one_third:
                header_indexes = (0, matches[1].end(0))
                text_indexes = (matches[1].end(0), matches[2].start(0))
                footer_indexes = (matches[2].start(0), text_len)
            else:
                header_indexes = (0, matches[0].end(0))
                text_indexes = (matches[0].end(0), matches[1].start(0))
                footer_indexes = (matches[1].start(0), text_len)
        elif len(matches) > 4:
            print(
                "Too Many Matches:\n %s" % [
                    str(match.start()) + " " + str(match.end()) + " " + match.group(0)
                    for match in matches
                ]
            )
        return header_indexes, text_indexes, footer_indexes
