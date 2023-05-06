# !/usr/local/bin/python
# -*- coding: utf-8 -*-
"""Contains GutenbergSearchTripletStore."""

# TODO: add method to search book when author is known

import re
from SPARQLWrapper import SPARQLWrapper, JSON
from dhtk import LOGGER
from dhtk.catalogs.search import Search
from dhtk.catalogs.gutenberg.author import GutenbergAuthor
from dhtk.catalogs.gutenberg.book import GutenbergBook


class GutenbergSearchTripletStore(Search):
    """
    Class made for searching inside the gutenberg catalog created by GutenbergDBCatalog.

    It uses two very similar functions (search_by_author and search_by_subject) that search
    respectively
    either for an author, or a subject (witch includes genres, subjects and languages).
    It returns what it finds as ids that point to the relevant books.
    """

    # TODO: check if ebook is not audio

    _query_header = "\n".join([
        "PREFIX dcterms: <http://purl.org/dc/terms/>",
        "PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>",
        "PREFIX purl: <http://purl.org/dc/terms/>",
        "PREFIX pgterms: <http://www.gutenberg.org/2009/pgterms/>\n",
    ])
    _query_select = "SELECT DISTINCT ?book_id ?title ?author_id ?author ?language"
    _query_head = "\n".join([
        "\nWHERE {",
        "?book_id purl:title ?title.",
        "?book_id purl:creator ?author_id.",
        "?author_id pgterms:name ?author.",
        "?book_id dcterms:language [rdf:value ?language].\n"
    ])

    _search_cache = dict()

    def get_metadata(self, book):
        """
        Get metadata about book that is present in the triplet store.

        :param book:
        :return:
        """
        # TODO: implement
        pass

    def __init__(
            self,
            sparql_endpoint="http://dhtk.unil.ch:3030/gutenberg/sparql"
    ):
        """
        The init funtion of GutenbergSearchTripletStore.

        Initalize the sparql endpoint.

        :param sparql_endpoint: the url of a triplet store containing the
            Gutenberg Catalog triplets.

        We recommend apache fuseki as it is freely available.

        :param parql_endpoint: URI of the sparql_endpoint of the triplet store.
        :type: str
        """
        self._sparql_endpoint = SPARQLWrapper(sparql_endpoint)

    def _get_query_results(self, query):
        """
        Return the result of a query.

        :param query:
        :return:
        """
        # LOGGER.debug("Executing query: \n%s", re.sub(r"[ ]+", " ", query))
        query = re.sub(r"\s+", " ", query.replace("\n", " "))
        sparql = self._sparql_endpoint
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        # TODO: handle external server better than this, please:
        try:
            query_results = sparql.queryAndConvert()
        except:
            return []
        results = list()
        for entry in query_results["results"]["bindings"]:
            formatted_entry = dict()
            for key, value in entry.items():
                formatted_entry[key] = value["value"]
            results.append(formatted_entry)
        return results

    def search_by_author(self, author_name, author_last_name=None):
        """
        Search books by author name.

        :param author_name: the name or fist name of the author, in plain _original_text (string)
        :param author_last_name: the last name of the author, in plain _original_text (string)
        :return: list of book ids in integer format
        """
        query = self._query_header + self._query_select + "?alias\n" + self._query_head
        if author_last_name:
            query += """
            FILTER (
                (regex(str(?author), "%s", "i") && regex(str(?author), "%s", "i")) ||
                (bound(?alias) && regex(str(?alias), "%s", "i") && regex(str(?alias), "%s", "i")))
            }
            ORDER BY ?author ?title
            """ % (author_name, author_last_name, author_name, author_last_name)
        else:
            query += """
                FILTER (regex(str(?author), "%s", "i") || (bound(?alias) && regex(str(?alias),
                "%s", "i")))
            }
            ORDER BY ?author ?title
            """ % (author_name, author_name)
        return self._get_query_results(query)

    def all_books(self):
        """Wrapper for all titles. For naming consistency and less human memory usage."""
        return self.all_titles()

    def all_titles(self):
        """
        Return the title of all books in the store.

        :return:
        """
        query = """
        PREFIX purl: <http://purl.org/dc/terms/>
            SELECT DISTINCT ?book_id ?title WHERE {
                ?book_id purl:title ?title.
            }
            ORDER BY ?title
        """
        return [(book["title"], book["book_id"]) for book in self._get_query_results(query)]

    def search_by_title(self, title):
        """
        Search by title of the book.

        :param title:
        :return: list of book ids in integer format
        """
        query = self._query_header + "\n" + self._query_select + "\n" + self._query_head
        query += """
            FILTER regex(str(?title), "%s", "i")
        }
        ORDER BY ?author ?title
        """ % title
        return self._get_query_results(query)

    def all_bookshelves(self):
        """
        Return all bookshelves in the catalog.

        :return:
        """
        query = """
            PREFIX pgterms: <http://www.gutenberg.org/2009/pgterms/>
            PREFIX rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            SELECT DISTINCT ?bookshelf WHERE {
                ?book_id pgterms:bookshelf _:blank.
                _:blank rdf:value ?bookshelf.
            }
            ORDER BY ?bookshelf
        """
        return [result["bookshelf"] for result in self._get_query_results(query)]

    def search_by_bookshelf(self, bookshelf):
        """
        Search by bookshelf.

        :param bookshelf: Any sort of bookshelf
        :return: list of book ids in integer format
        pgterms:bookshelf
        """
        query = self._query_header + self._query_select + "?bookshelf\n" + self._query_head
        query += """
                ?book_id pgterms:bookshelf [rdf:value ?bookshelf].
                FILTER regex(str(?bookshelf), "%s", "i")   
            }
            ORDER BY ?author ?title
        """ % (bookshelf,)

        return self._get_query_results(query)

    def all_subjects(self):
        """
        Return all subjects of the catalog.

        :return:
        """
        query = """
            PREFIX dcterms: <http://purl.org/dc/terms/>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            SELECT DISTINCT ?subject WHERE {
                ?book_id dcterms:subject _:blank.
                _:blank rdf:value ?subject.
            }
            ORDER BY ?subject
        """
        return [result["subject"] for result in self._get_query_results(query)]

    def search_by_subject(self, subject):
        """
        Search by subject.

        :param subject: Any sort of subject, genre, subjects (string)
        :return: list of book ids in integer format
        """
        query = self._query_header + self._query_select + "?subject\n" + self._query_head
        query += """
            ?book_id dcterms:subject [rdf:value ?subject].
            FILTER regex(str(?subject), "%s", "i")
        }
        ORDER BY ?author ?title
        """ % (subject,)
        return self._get_query_results(query)

    def bookshelves_subjects(self, book_id):
        """
        Return the bookshelves on which the book is to be found.

        :param book_id:
        :return:
        """
        query = self._query_header
        query += """
        SELECT DISTINCT ?subject
        WHERE {
            <%s> dcterms:subject [rdf:value ?subject].
        }
        ORDER BY ?subject
        """ % book_id
        subjects = [result["subject"] for result in self._get_query_results(query)]
        query = self._query_header
        query += """
        SELECT DISTINCT ?bookshelf
        WHERE {
            <%s> pgterms:bookshelf [rdf:value ?bookshelf].
        }
        ORDER BY ?bookshelf
        """ % book_id
        bookshelves = [result["bookshelf"] for result in self._get_query_results(query)]
        return bookshelves, subjects

    def all_authors(self):
        """
        Return all authors present in the catalog.

        :return:
        """
        query = """
        PREFIX purl: <http://purl.org/dc/terms/>
        PREFIX pgterms: <http://www.gutenberg.org/2009/pgterms/>
            SELECT DISTINCT ?author ?author_id WHERE {
                [] purl:creator ?author_id.
                ?author_id pgterms:name ?author.
            }
            ORDER BY ?author
        """
        return [
            (
                result["author"], result["author_id"]
            ) for result in self._get_query_results(query)
        ]

    def search_author_by_name_or_alias(self, author_name, author_last_name=None):
        """
        Search by author name and alias.

        :param author_name: the name or fist name of the author, in plain _original_text (string)
        :param author_last_name: the last name of the author, in plain _original_text (string)
        :return: list of book ids in integer format
        """
        query = """
        PREFIX purl: <http://purl.org/dc/terms/>
        PREFIX pgterms: <http://www.gutenberg.org/2009/pgterms/>
        SELECT DISTINCT ?author ?author_id WHERE {
                [] purl:creator ?author_id.
                ?author_id pgterms:name ?author.
                OPTIONAL { ?author_id pgterms:alias ?alias. }
        """
        if author_last_name:
            query += """
            FILTER (
                (regex(str(?author), "%s", "i") && regex(str(?author), "%s", "i")) ||
                (bound(?alias) && regex(str(?alias), "%s", "i") && regex(str(?alias), "%s", "i")))
            }
            ORDER BY ?author
            """ % (author_name, author_last_name, author_name, author_last_name)
        else:
            query += """
                FILTER (regex(str(?author), "%s", "i") || (bound(?alias) && regex(str(?alias),
                "%s", "i")))
            }
            ORDER BY ?author
            """ % (author_name, author_name)
        return [(item["author"], item["author_id"]) for item in self._get_query_results(query)]

    def search_author_by_name(self, author_name, author_last_name=None):
        """
        Seach by author name.

        :param author_name: the name or fist name of the author, in plain _original_text (string)
        :param author_last_name: the last name of the author, in plain _original_text (string)
        :return: list of book ids in integer format
        """
        query = """
        PREFIX purl: <http://purl.org/dc/terms/>
        PREFIX pgterms: <http://www.gutenberg.org/2009/pgterms/>
        SELECT DISTINCT ?author ?author_id WHERE {
                [] purl:creator ?author_id.
                ?author_id pgterms:name ?author.
        """
        if author_last_name:
            query += """
            FILTER (regex(str(?author), "%s", "i") && regex(str(?author), "%s", "i"))
            }
            ORDER BY ?author
            """ % (author_name, author_last_name)
        else:
            query += """
                FILTER (regex(str(?author), "%s", "i"))
            }
            ORDER BY ?author
            """ % author_name
        return [(item["author"], item["author_id"]) for item in self._get_query_results(query)]

    def search_by_title_and_author(self, title, auhtor_name, author_last_name):
        """
        Search store for books by title and author.

        :param title:
        :param auhtor_name:
        :param author_last_name:
        :return:
        """
        # TODO: implement
        pass

    def author_from_author_id(self, author_id):
        """
        Return dhtk.common.author.Autor from author_id.

        :param author_id:
        :return:
        """

        query = self._query_header
        query += "\n".join([
            "SELECT DISTINCT ?name",
            "WHERE {",
            "<%s> pgterms:name ?name." % author_id,
            "}",
        ])
        name = self._get_query_results(query)[0]["name"]
        LOGGER.debug("Name: %s", name)

        query = self._query_header
        query += "\n".join([
            "SELECT DISTINCT ?birth_date",
            "WHERE {",
            "<%s> pgterms:birthdate ?birth_date." % author_id,
            "}",
        ])
        result = self._get_query_results(query)
        if result:
            birth_date = result[0]["birth_date"]
        else:
            birth_date = ""
        LOGGER.debug("Birth: %s", birth_date)

        query = self._query_header
        query += "\n".join([
            "SELECT DISTINCT ?death_date",
            "WHERE {",
            "<%s> pgterms:deathdate ?death_date." % author_id,
            "}",
        ])
        result = self._get_query_results(query)
        if result:
            death_date = result[0]["death_date"]
        else:
            death_date = ""
        LOGGER.debug("Death: %s", death_date)

        query = self._query_header
        query += "\n".join([
            "SELECT DISTINCT ?alias",
            "WHERE {",
            "<%s> pgterms:alias ?alias." % author_id,
            "}",
        ])
        aliases = {result.get("alias", None) for result in self._get_query_results(query)}
        LOGGER.debug("Aliases: %s", ", ".join(aliases))


        query = self._query_header
        query += "\n".join([
            "SELECT DISTINCT ?web_page",
            "WHERE {",
            "<%s> pgterms:webpage ?web_page." % author_id,
            "}",
        ])
        web_pages = {result.get("web_page", None) for result in self._get_query_results(query)}
        if not web_pages:
            web_pages = set()
        LOGGER.debug("Web pages: %s", web_pages)

        author = GutenbergAuthor(
            gutenberg_id=author_id,
            name=name,
            aliases=aliases,
            birth_date=birth_date,
            death_date=death_date,
            web_pages=web_pages
        )
        return author

    def get_bibliography_from_author_id(self, author_id):
        """
        Return a set of tuples containing the book tiles and book_ids created by the author.

        :param author_id:
        :return:
        """
        query = self._query_header
        query += "\n".join([
            "SELECT DISTINCT ?book_id ?title",
            "WHERE",
            "{",
            "?book_id purl:title ?title.",
            "?book_id purl:creator <%s>." % author_id,
            "}",
            "ORDER BY ?title"
        ])
        return [(
            result["title"], result["book_id"]
        ) for result in self._get_query_results(query)]

    def book_from_book_id(self, book_id):
        """
        Return dhtk.common.book.Book or subclass.

        :param book_id:
        :return:
        """
        LOGGER.debug("Searching: %s", book_id)
        query = self._query_header
        query += "\n".join([
            "SELECT DISTINCT ?title ?author_id ?language",
            "WHERE",
            "{",
            "<%s> purl:title ?title." % book_id,
            "<%s> purl:creator ?author_id." % book_id,
            "<%s> <http://purl.org/dc/terms/hasFormat> ?format." % book_id,
            "<%s> dcterms:language [rdf:value ?language]." % book_id,
            "FILTER (",
            "CONTAINS(STR(?format), '.txt')",
            ")",
            "}",
        ])
        if not self._get_query_results(query):
            LOGGER.debug("Not Found Found: %s", book_id)
            return None
        book = self._get_query_results(query)[0]
        # TODO: Add bookshelf, subjects, metadata
        LOGGER.debug("Found: %s", book)
        book = GutenbergBook(
            gutenberg_id=book_id,
            title=book["title"],
            language=book["language"],
            author=self.author_from_author_id(book["author_id"])
        )
        return book

    def books_by_author_id(self, author_id):
        """
        Return books of an author.

        :param author_id:
        :return:
        """
        query = """
           PREFIX purl: <http://purl.org/dc/terms/>
           PREFIX pgterms: <http://www.gutenberg.org/2009/pgterms/>
           SELECT DISTINCT ?book_id ?title WHERE {
               ?book_id purl:creator <%s>.
               ?book_id purl:title ?title.
           }
           ORDER BY ?title
        """ % author_id
        return [(result["title"], result["book_id"]) for result in self._get_query_results(query)]

    def statistics(self):
        """
        Print some statistics about  the catalog.

        :return:
        """
        statistics = dict()
        statistics["number_of_books"] = len(self.all_titles())
        statistics["number_of_authors"] = len(self.all_authors())
        statistics["number_of_bookshelves"] = len(self.all_bookshelves())
        subjects = set()
        for subject_string in self.all_subjects():
            for subject in subject_string.split(" -- "):
                subjects.add(subject)
        statistics["number_of_subjects"] = len(subjects)
        for key, value in statistics.items():
            print("{:23}:\t {:>5}".format(key.replace("_", " "), value))
