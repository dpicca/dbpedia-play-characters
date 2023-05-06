# !/usr/local/bin/python
# -*- coding: utf-8 -*-
"""Module contains the abstract Author class."""

from nameparser import HumanName

class Author:
    """
    The class for a generic author.

    These class should be parent to all authors used with the dhtk library.
    """
    metadata = dict()

    def __init__(
            self,
            name,
            metadata=None,
            **kwargs
    ):
        """
        The init function of the Author class.

        :param str first_name:
        :param str last_name:
        :param date birth_date:
        :param dict metadata:
        """

        if not isinstance(name, HumanName):
            raise ValueError("Name is not an instance of nameparser.HumanName")
        self.name = name

        if isinstance(metadata, dict):
            metadata = dict()

        if kwargs is not None:
            for key, value in kwargs.items():
                self.metadata[key] = value

        self.metadata = {**self.metadata, **metadata}

        self.metadata["birth_date"] = metadata.get("bitrh_date", "")

    def __eq__(self, other):
        """
        Equality function between authors.

        :param Author other:
        :return: bool
        """
        return self.get_first_name() == other.get_first_name() and \
            self.get_last_name() == other.get_last_name() and \
            self.get_birth_date() == other.get_birth_date()

    def __ne__(self, other):
        """
        Inequality function.

        :param Author other:
        :return: bool
        """
        return not self.__eq__(other)

    def get_first_name(self):
        """
        Get authors first name.

        :return: str
        """
        return self.name.first

    def get_middle_name(self):
        """
        Get authors last name.

        :return: str
        """
        return self.name.middle

    def get_last_name(self):
        """
        Get authors last name.

        :return: str
        """
        return self.name.last

    def get_birth_date(self):
        """
        Get authors birth date.

        :return: str
        """
        return self.metadata.get("birth_date", "")

    def get_biography(self):
        """
        Get authors biography.

        :return: str
        """
        return self.metadata.get("biography", "")

    def get_bibliography(self):
        """
              Get author bibliography.

              :return: str
        """
        return self.metadata.get("bibliography", "")

    def print_info(self):
        """
        Print information about the author.

        :return: None
        """
        print(self.get_full_name())
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
        author_dict = self.name.as_dict()
        author_dict["metadata"] = self.metadata
        return author_dict

    def get_full_name(self):
        """
        Get authors full name.

        :return: str
        """
        return str(self.name)

    def __hash__(self):
        """Return hash for the author."""
        return hash((self.name.first, self.name.last, self.get_birth_date()))
