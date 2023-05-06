
import pandas as pd
import spacy
import textacy
import re
from glob import glob
from scripts.segmenter import TextSegmenter
from pprint import pprint
from SPARQLWrapper import SPARQLWrapper, JSON
from spacy.pipeline import TextCategorizer

class NaiveClassifier:

    has_header = True
    has_footer = True
    header_end_reached = False
    footer_start_reached = False
    part_type = []
    segmenter = TextSegmenter()


    def __init__(self, raw_text):
        self.text = raw_text
        text_blocks_indices, newline_blocks_indices, text_parts_indices = \
            self.segmenter.get_text_parts()
        self.text_blocks = list(
            [self.text[b:e] for b, e in text_blocks_indices]
        )
        self.separator_blocks =  list(
            [e-b for b, e in newline_blocks_indices]
        )

        header_indicies, _, footer_indicies = self.get_header_text_footer(raw_text)

        # find out if text has header or not
        # TODO: maybe better:
        # https://shuyo.wordpress.com/2008/11/24/extract-body-of-project-gutenbergs-text/

        if not header_indicies:
            self.has_header = False

        if not footer_indicies:
            self.has_footer = False


        # tag the text parts
        for part_index in range(1, len(self.text_blocks)):

            if self.has_header and not self.header_end_reached:
                self.part_type.append("header")
                self.header_end_reached = self.is_header_end(part_index)
                return

            if self.has_footer and self.footer_start_reached:
                self.part_type.append("footer")
                self.footer_start_reached = self.is_footer_start(part_index)
                return


            part_type = "unknown"




    def get_text_part_type(self, part_index):
        pass

    def is_header_end(self, part_index):
        """
        returns True if part_index is the index of the header end.

        :param part_index:
        :return:
        """
        pass

    def is_footer_start(self, part_index):
        """
        returns True if part_index is the index of the start of the footer.

        :param part_index:
        :return:
        """
        pass


def get_language(book_id):
    sparql = SPARQLWrapper("http://dhtk.unil.ch:3030/gutenberg/sparql")
    query = """
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX dcterms: <http://purl.org/dc/terms/>

    SELECT ?language
    WHERE {
        <http://www.gutenberg.org/ebooks/%s> dcterms:language [rdf:value ?language].
    }""" % book_id
    query = re.sub(r"\s+", " ", query.replace("\n", " "))
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    query_results = sparql.queryAndConvert()
    return query_results["results"]["bindings"][0]["language"]["value"]


if __name__ == "__main__":
    output_path = "../naive_annotated/"
    source_path = "../devided_texts/"
    spacy_models_path = "/usr/lib/python3.7/site-packages/spacy/data/"
    models = [lang[-2:] for lang in glob(spacy_models_path + "[a-z][a-z]")]


    dataset_files = glob(source_path + "*.csv")

    for csv_file in dataset_files[:2]:

        text_name = csv_file.replace(source_path, "").replace(".csv", "")
        lang = get_language(text_name)
        if lang in models:
            nlp = spacy.load(lang)
        else:
            nlp = spacy.load("xx")
        textcat = TextCategorizer(nlp.vocab)
        data = pd.read_csv(csv_file)
        data = data.drop(columns=['Unnamed: 0', ])

        spacy_doc = [nlp(row.loc["text"]) for i, row in data.iterrows()]
        for doc in textcat.pipe(spacy_doc, batch_size=50):
            pprint(doc)
