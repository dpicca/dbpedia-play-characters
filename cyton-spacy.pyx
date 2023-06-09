%%cython -+
import numpy # Sometime we have a fail to import numpy compilation error if we don't import numpy
from cymem.cymem cimport Pool
from spacy.tokens.doc cimport Doc
from spacy.typedefs cimport hash_t
from spacy.structs cimport TokenC

cdef struct DocElement:
    TokenC* c
    int length

cdef int fast_loop(DocElement* docs, int n_docs, hash_t word, hash_t tag):
    cdef int n_out = 0
    for doc in docs[:n_docs]:
        for c in doc.c[:doc.length]:
            if c.lex.lower == word and c.tag == tag:
                n_out += 1
    return n_out

def main_nlp_fast(doc_list):
    cdef int i, n_out, n_docs = len(doc_list)
    cdef Pool mem = Pool()
    cdef DocElement* docs = <DocElement*>mem.alloc(n_docs, sizeof(DocElement))
    cdef Doc doc
    for i, doc in enumerate(doc_list): # Populate our database structure
        docs[i].c = doc.c
        docs[i].length = (<Doc>doc).length
    word_hash = doc.vocab.strings.add('run')
    tag_hash = doc.vocab.strings.add('NN')
    n_out = fast_loop(docs, n_docs, word_hash, tag_hash)
    print(n_out)