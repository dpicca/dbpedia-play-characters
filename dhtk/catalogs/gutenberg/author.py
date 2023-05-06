# !/usr/local/bin/python
# -*- coding: utf-8 -*-
"""Contains the GutenbergAuthor Class."""

import re
import copy
from nameparser import HumanName
from nameparser.config.titles import FIRST_NAME_TITLES
from dhtk import LOGGER
from dhtk.common.author import Author


class GutenbergAuthor(Author):
    """Extend the Author with variables from the gutenberg project."""

    metadata = dict()

    def __init__(
            self,
            gutenberg_id,
            name,
            aliases=None,
            web_pages=None,
            **kwargs
    ):
        """
        Init function of GutenbergAuthor.
        Implement the Abstract Author class and extend it with gutenberg_id.
        :param str gutenberg_id:
        :param str name:
        :param set aliases:
        :param set web_pages:
        """
        id_format = re.compile(r"http://www.gutenberg.org/2009/agents/\d+$")
        if not id_format.fullmatch(gutenberg_id):
            raise ReferenceError("This gutenberg id is not valid! %s" % gutenberg_id)
        self.metadata["gutenberg_id"] = gutenberg_id
        self.metadata["id"] = gutenberg_id

        self.metadata["gutenberg_name"] = name

        if not isinstance(aliases, set):
            aliases = set()
        self.metadata["gutenberg_aliases"] = aliases
        self.metadata["aliases"] = set()

        if not isinstance(web_pages, set):
            web_pages = set()
        self.metadata["web_pages"] = web_pages

        FIRST_NAME_TITLES.add("saint")
        name = self.convert_name(name)

        LOGGER.debug("converting aliases names: %s", ", ".join(aliases))
        self.metadata["aliases"] = {str(self.convert_name(alias)) for alias in aliases}
        LOGGER.debug("aliases: %s", ", ".join(self.metadata["aliases"]))

        if str(name) in self.metadata["aliases"]:
            LOGGER.debug("removing '%s' from %s", str(name), ", ".join(self.metadata["aliases"]))
            self.metadata["aliases"].remove(str(name))

        metadata = copy.copy(self.metadata)
        super().__init__(
            name,
            metadata=metadata,
            **kwargs
        )

    def convert_name(self, human_name):
        """Convert one string to Human name."""
        human_name = HumanName(human_name)
        if human_name.suffix:
            self.metadata["gutenberg_name_suffix"] = human_name.suffix
            human_name.suffix = ""
        if human_name.nickname:
            LOGGER.debug("%s nickname: %s", str(human_name), human_name.nickname)
            no_nickname = copy.copy(human_name)
            no_nickname.nickname = ""
            first_name_match = re.match(
                re.sub(r"(([A-Z])[a-z]*[.])", r"\2\\w+", human_name.first, re.UNICODE),
                human_name.nickname,
                re.UNICODE
            )
            LOGGER.debug(
                "%s, %s",
                re.sub(
                    r"(([A-Z])[a-z]*[.])", r"\2\\w+",
                    human_name.first,
                    re.UNICODE
                ),
                human_name.nickname
            )
            if first_name_match and len(first_name_match.group(0)) >= len(human_name.first):
                human_name.first = first_name_match.group(0)
                human_name.nickname = human_name.nickname[len(human_name.first):].strip()
                LOGGER.debug("Adding %s to aliases", str(no_nickname))
                self.metadata["aliases"].add(str(no_nickname))
            middle_name_match = re.match(
                re.sub(r"(([A-Z])[a-z]*[.])", r"\2\\w+", human_name.middle, re.UNICODE),
                human_name.nickname,
                re.UNICODE
            )
            LOGGER.debug(
                "%s, %s",
                re.sub(
                    r"(([A-Z])[a-z]*[.])", r"\2\\w+",
                    human_name.middle, re.UNICODE
                ),
                human_name.nickname
            )
            if middle_name_match and len(middle_name_match.group(0)) >= len(human_name.middle):
                human_name.middle = middle_name_match.group(0)
                human_name.nickname = human_name.nickname[len(human_name.middle):].strip()
                LOGGER.debug("Adding %s to aliases", str(no_nickname))
                self.metadata["aliases"].add(str(no_nickname))
        return human_name

    def get_gutenberg_id(self):
        """
        Return the gutenberg id url of the author.
        :return:
        """
        return self.metadata["gutenberg_id"]

    def __eq__(self, other):
        """Author equality."""
        if isinstance(other, GutenbergAuthor):
            equals = self.get_gutenberg_id() == other.get_gutenberg_id()
        else:
            equals = super().__eq__(other)
        return equals

    def __hash__(self):
        """Return hash for the author."""
        return hash((self.name.first, self.name.last, self.get_birth_date()))
