# !/usr/local/bin/python
# -*- coding: utf-8 -*-
"""Contains the DbpediaMetadata Class."""

import re
from time import sleep
from urllib.parse import unquote, quote

from SPARQLWrapper import SPARQLWrapper, JSON
from SPARQLWrapper.SPARQLExceptions import QueryBadFormed, EndPointNotFound

from dhtk import LOGGER

class DbpediaMetadata:
    """
    Acts as interface between dhtk and Dbpedia.

    Specifically allows user to serach a dbtk.common.Book on dbpedia.
    TODO: Add some persistent cache (books found, books not found) to \
    lessen the interrogation on dbpedia
    """

    _sparql_endpoint = SPARQLWrapper("http://dbpedia.org/sparql")

    def __init__(self):
        """The init function."""
        self._sparql_endpoint.setReturnFormat(JSON)

    def query_dbpedia(self, query):
        """
        Return query result.

        :param str query: A sparql query
        :return:
        """
        sparql = self._sparql_endpoint
        sparql.setQuery(query)
        try:
            results = sparql.queryAndConvert()
            return results
        except QueryBadFormed:
            return {"boolean": False}
        except EndPointNotFound:
            # TODO: WARNING
            sleep(3000)
            return {"boolean": False}

    def _test_book_uri(self, uri):
        """
        Check if the uri is the uri of a dbo:Book in dbpedia.

        :param str uri:
        :return:
        """
        query = "ASK {<%s> rdf:type dbo:Book.}" % uri
        return self.query_dbpedia(query)['boolean']

    def search_book_uri(self, book, author_uri=None):
        """
        Return the uri of the book in DBPEDIA.

        TODO: clean-up this method using a list of replacement tuples and optional suffixes.
        TODO: remove Volume (Vol 1) and such information at the end of the title.
        TODO: use fuzzy matching.
        TODO: maybe get full list of book titles in dbpedia and search in that list.
        :param book:
        :return:
        """
        base_url = "http://dbpedia.org/resource/{}"
        if not author_uri:
            author_uri = self.search_author_uri(book.get_author())
        title = book.get_title()
        if author_uri:
            LOGGER.info("Author URI found: %s .", author_uri)
            query = """
                PREFIX dbo: <http://dbpedia.org/ontology/>
                SELECT ?dbpedia_uri 
                WHERE {
                  ?dbpedia_uri ?author <%s>
                 {?dbpedia_uri dbo:author <%s> .}
                UNION
                 {?dbpedia_uri dbo:writer <%s> .}
                }
            """ % (author_uri, author_uri, author_uri)
            # TODO: implement following queries
            # query_2 =
            # """
            #     PREFIX dbo: <http://dbpedia.org/ontology/>
            #     PREFIX dbp: <http://dbpedia.org/property/>
            #     prefix dbr: <http://dbpedia.org/resource/>
            #     prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            #     prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            #     prefix owl: <http://www.w3.org/2002/07/owl#>
            #     prefix pgterms: <http://www.gutenberg.org/2009/pgterms/>
            #     prefix dcterms: <http://purl.org/dc/terms/>
            #     prefix dcam: <http://purl.org/dc/dcam/>
            #
            #     SELECT DISTINCT ?dbpedia_uri ?title
            #     WHERE {
            #     ?dbpedia_uri ?author dbr:Leonid_Andreyev
            #     {?dbpedia_uri dbo:author dbr:Leonid_Andreyev .}
            #     UNION
            #     {?dbpedia_uri dbo:writer dbr:Leonid_Andreyev .}
            #     ?dbpedia_uri ?label ?title
            #     {?dbpedia_uri rdfs:label ?title}
            #     UNION
            #     {?dbpedia_uri foaf:name ?title}
            #     UNION
            #     {?dbpedia_uri dbp:name ?title}
            #     UNION
            #     {?dbpedia_uri dbp:title ?title}
            #     }
            # """
            # # query_3 =
            # """
            # PREFIX dbo: < http://dbpedia.org/ontology/>
            # SELECT *
            # WHERE {
            # ?dbpedia_uri dbo: author <%s>.
            # ?alias dbo: wikiPageRedirects ?dbpedia_uri.
            # """
            book_uris = self.query_dbpedia(query)

            clean_titles = [t.replace(base_url[:-2], "").replace(
                " (_novel)", "").replace("_", " ") for t in book_uris]

            if title in clean_titles:
                return base_url.format(title)

            letters_only = [re.sub(r"[^A-Za-z]", "", t) for t in clean_titles]
            for to_remove in ["", r"\n.+", r";.+", r":.+"]:
                letters_only_title = re.sub(r"[^A-Za-z]", "", re.sub(to_remove, "", title))
                if letters_only_title in letters_only:
                    return book_uris[letters_only.index(letters_only_title)]
            LOGGER.info("Could not find book URI with author info provided.")
        else:
            LOGGER.info("Author URI not found.")

        if "\n" in title:
            uri = base_url.format(unquote(quote(
                title.replace("\n", ", ").replace(" ", "_")
            )))
            if self._test_book_uri(uri):
                return uri

            uri = base_url.format(unquote(quote(
                title.replace("\n", " ").replace(" ", "_")
            )))
            if self._test_book_uri(uri):
                return uri

            uri = base_url.format(unquote(quote(
                re.sub(r"\n.+", "", title).replace(" ", "_")
            )))
            if self._test_book_uri(uri):
                return uri

        if ":" in title:
            uri = base_url.format(unquote(quote(
                title.replace(":", ", ").replace(" ", "_")
            )))
            if self._test_book_uri(uri):
                return uri

            uri = base_url.format(unquote(quote(
                title.replace(":", " ").replace(" ", "_")
            )))
            if self._test_book_uri(uri):
                return uri

            uri = base_url.format(unquote(quote(
                re.sub(r":.+", "", title).replace(" ", "_")
            )))
            if self._test_book_uri(uri):
                return uri

        if ";" in title:
            uri = base_url.format(unquote(quote(
                title.replace(";", ", ").replace(" ", "_")
            )))
            if self._test_book_uri(uri):
                return uri

            uri = base_url.format(unquote(quote(
                title.replace(";", " ").replace(" ", "_")
            )))
            if self._test_book_uri(uri):
                return uri

            uri = base_url.format(unquote(quote(
                re.sub(r";.+", "", title).replace(" ", "_")
            )))
            if self._test_book_uri(uri):
                return uri

        if "(" in title:
            uri = base_url.format(unquote(quote(
                re.sub(r" [(].+[)]", "", title).replace(" ", "_")
            )))
            if self._test_book_uri(uri):
                return uri

        if "[" in title:
            uri = base_url.format(unquote(quote(
                re.sub(r"[[].+[]]", "", title).replace(" ", "_")
            )))
            if self._test_book_uri(uri):
                return uri

            uri = base_url.format(unquote(quote(
                re.sub(r"[[].+[]]", "", title) + "_(novel)"
            )))
            if self._test_book_uri(uri):
                return uri

        uri = base_url.format(unquote(quote(
            title.replace(" ", "_")
        )))
        if self._test_book_uri(uri):
            return uri

        uri = base_url.format(unquote(quote(
            title.replace(" ", "_") + "_(novel)"
        )))
        if self._test_book_uri(uri):
            return uri

        uri = base_url.format(unquote(quote(
            title.replace(" ", "-")
        )))
        if self._test_book_uri(uri):
            return uri

        uri = base_url.format(unquote(quote(
            re.sub(r";.+", "", title.replace(" ", "-"))
        )))
        if self._test_book_uri(uri):
            return uri

        uri = base_url.format(unquote(quote(
            title.replace(" ", "-") + "_(novel)"
        )))
        if self._test_book_uri(uri):
            return uri
        LOGGER.info("Book uri not found.")
        return ""

    def get_book_metadata(self, book):
        """
        Search for metadata of a book.

        :param book:
        :return:
        """
        uri = self.search_book_uri(book)
        if not uri:
            return {}

        metadata = {
            "dbpedia": uri
        }

        # general metadata
        query = """
            SELECT  ?releasedate ?published ?where ?lang ?comment ?wikipedia ?pagenum {
                OPTIONAL { <%(uri)s> dbp:published ?published.}
                OPTIONAL { <%(uri)s> dbp:country ?where.}
                OPTIONAL { <%(uri)s> dbp:language ?lang.}
                OPTIONAL { <%(uri)s> rdfs:comment ?comment.}
                OPTIONAL { ?wikipedia foaf:primaryTopic <%(uri)s>.}
                OPTIONAL { <%(uri)s> dbp:no ?pagenum.}
                FILTER(LANG(?comment)='en')
            }
            """ % {'uri': uri}
        results = self.query_dbpedia(query)
        try:
            results = results['results']['bindings'][0]
            for key, value in results.items():
                metadata[key] = value["value"]
        except KeyError:
            pass

        # releasedate
        query = """
            SELECT ?releasedate {
                OPIONAL { <%s dbo:releaseDate ?releasedate.}
            }
            """ % uri
        results = self.query_dbpedia(query)

        try:
            results = results['results']['bindings']
            for item in results:
                for key, value in item.items():
                    try:
                        metadata["release_date"].append(value["value"])
                    except KeyError:
                        metadata["release_date"] = [value["value"]]
        except KeyError:
            pass

        # subjects
        query = """
            SELECT ?subjects {
                OPTIONAL { <%s> dct:subject ?subjects. }
            }
        """ % uri
        results = self.query_dbpedia(query)
        results = results['results']['bindings']
        for item in results:
            for key, value in item.items():
                try:
                    metadata["subjects"].append(value["value"])
                except KeyError:
                    metadata["subjects"] = [value["value"]]

        # genres
        query = """
            SELECT ?genres {
                OPTIONAL { <%s> dbo:literaryGenre ?genres. }
            }
        """ % uri
        results = self.query_dbpedia(query)
        results = results['results']['bindings']
        for item in results:
            for key, value in item.items():
                try:
                    metadata["genres"].append(value["value"])
                except KeyError:
                    metadata["genres"] = [value["value"]]

        # characters
        query = """
            SELECT  ?dbpedia ?wikipedia {
                <%s> rdfs:seeAlso ?dbpedia.
                ?dbpedia dct:subject dbc:Lists_of_literary_characters .
                OPTIONAL { ?wikipedia foaf:primaryTopic ?dbpedia. }
            }
        """ % uri
        results = self.query_dbpedia(query)
        try:
            results = results['results']['bindings'][0]
            metadata["characters"] = {
                'dbpedia': results["dbpedia"]["value"],
                'wikipedia': results["wikipedia"]["value"],
            }
        except (KeyError, IndexError):
            pass

        return metadata

    def _test_person_uri(self, uri):
        """
        Check if the uri is the uri of a dbo:Person in dbpedia.

        :param str uri:
        :return:
        """
        query = "ASK {<%s> rdf:type dbo:Person. }" % uri
        return self.query_dbpedia(query)['boolean']

    def search_author_uri(self, author):
        """
        Return the uri of the autor in DBPEDIA.

        :param author:
        :return:
        """

        for web_site in author.metadata.get("web_pages", []):
            uri = "http://dbpedia.org/resource/{}".format(
                unquote(quote(web_site.rsplit("/", 1)[1]))
            )
            if self._test_person_uri(uri):
                LOGGER.info("Found author uri from webpages.")
                return uri

        uri = "http://dbpedia.org/resource/{}".format(
            author.get_first_name().replace(" ", "_") + "_" +
            author.get_last_name().replace(" ", "_")
        )
        if self._test_person_uri(uri):
            LOGGER.info("Found author uri from name.")
            return uri

        for alias in author.metadata.get("aliases", []):
            if ", " in alias:
                alias = "_".join(alias.split(", ")[::-1])
            uri = "http://dbpedia.org/resource/{}".format(unquote(quote(alias)))
            if self._test_person_uri(uri):
                LOGGER.info("Found author uri from aliases.")
                return uri

        return ""

    def get_author_metadata(self, author):
        """
        Return author medatada.

        :param author:
        :return:
        """
        pass
