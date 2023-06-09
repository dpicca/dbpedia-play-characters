import os
import pickle
import pandas as pd
import matplotlib.pyplot as plt

def relabel_prefixed(labels):
    prefixes = {
    "http://www.w3.org/2005/Atom": "a:",
    "http://schemas.talis.com/2005/address/schema#": "address:",
    "http://webns.net/mvcb/": "admin:",
    "http://www.w3.org/ns/activitystreams#": "as:",
    "http://atomowl.org/ontologies/atomrdf#": "atom:",
    "http://soap.amazon.com/": "aws:",
    "http://b3s.openlinksw.com/": "b3s:",
    "http://schemas.google.com/gdata/batch": "batch:",
    "http://purl.org/ontology/bibo/": "bibo:",
    "bif:": "bif:",
    "http://www.openlinksw.com/schemas/bugzilla#": "bugzilla:",
    "http://www.w3.org/2002/12/cal/icaltzd#": "c:",
    "http://www.openlinksw.com/campsites/schema#": "campsite:",
    "http://www.crunchbase.com/": "cb:",
    "http://web.resource.org/cc/": "cc:",
    "http://purl.org/rss/1.0/modules/content/": "content:",
    "http://purl.org/captsolo/resume-rdf/0.2/cv#": "cv:",
    "http://purl.org/captsolo/resume-rdf/0.2/base#": "cvbase:",
    "http://www.w3.org/2001/sw/DataAccess/tests/test-dawg#": "dawgt:",
    "http://dbpedia.org/resource/Category:": "dbc:",
    "http://dbpedia.org/ontology/": "dbo:",
    "http://dbpedia.org/property/": "dbp:",
    "http://af.dbpedia.org/resource/": "dbpedia-af:",
    "http://als.dbpedia.org/resource/": "dbpedia-als:",
    "http://an.dbpedia.org/resource/": "dbpedia-an:",
    "http://ar.dbpedia.org/resource/": "dbpedia-ar:",
    "http://az.dbpedia.org/resource/": "dbpedia-az:",
    "http://bar.dbpedia.org/resource/": "dbpedia-bar:",
    "http://be.dbpedia.org/resource/": "dbpedia-be:",
    "http://be-x-old.dbpedia.org/resource/": "dbpedia-be-x-old:",
    "http://bg.dbpedia.org/resource/": "dbpedia-bg:",
    "http://br.dbpedia.org/resource/": "dbpedia-br:",
    "http://ca.dbpedia.org/resource/": "dbpedia-ca:",
    "http://commons.dbpedia.org/resource/": "dbpedia-commons:",
    "http://cs.dbpedia.org/resource/": "dbpedia-cs:",
    "http://cy.dbpedia.org/resource/": "dbpedia-cy:",
    "http://da.dbpedia.org/resource/": "dbpedia-da:",
    "http://de.dbpedia.org/resource/": "dbpedia-de:",
    "http://dsb.dbpedia.org/resource/": "dbpedia-dsb:",
    "http://el.dbpedia.org/resource/": "dbpedia-el:",
    "http://eo.dbpedia.org/resource/": "dbpedia-eo:",
    "http://es.dbpedia.org/resource/": "dbpedia-es:",
    "http://et.dbpedia.org/resource/": "dbpedia-et:",
    "http://eu.dbpedia.org/resource/": "dbpedia-eu:",
    "http://fa.dbpedia.org/resource/": "dbpedia-fa:",
    "http://fi.dbpedia.org/resource/": "dbpedia-fi:",
    "http://fr.dbpedia.org/resource/": "dbpedia-fr:",
    "http://frr.dbpedia.org/resource/": "dbpedia-frr:",
    "http://fy.dbpedia.org/resource/": "dbpedia-fy:",
    "http://ga.dbpedia.org/resource/": "dbpedia-ga:",
    "http://gd.dbpedia.org/resource/": "dbpedia-gd:",
    "http://gl.dbpedia.org/resource/": "dbpedia-gl:",
    "http://he.dbpedia.org/resource/": "dbpedia-he:",
    "http://hr.dbpedia.org/resource/": "dbpedia-hr:",
    "http://hsb.dbpedia.org/resource/": "dbpedia-hsb:",
    "http://hu.dbpedia.org/resource/": "dbpedia-hu:",
    "http://id.dbpedia.org/resource/": "dbpedia-id:",
    "http://ie.dbpedia.org/resource/": "dbpedia-ie:",
    "http://io.dbpedia.org/resource/": "dbpedia-io:",
    "http://is.dbpedia.org/resource/": "dbpedia-is:",
    "http://it.dbpedia.org/resource/": "dbpedia-it:",
    "http://ja.dbpedia.org/resource/": "dbpedia-ja:",
    "http://ka.dbpedia.org/resource/": "dbpedia-ka:",
    "http://kk.dbpedia.org/resource/": "dbpedia-kk:",
    "http://ko.dbpedia.org/resource/": "dbpedia-ko:",
    "http://ku.dbpedia.org/resource/": "dbpedia-ku:",
    "http://la.dbpedia.org/resource/": "dbpedia-la:",
    "http://lb.dbpedia.org/resource/": "dbpedia-lb:",
    "http://lmo.dbpedia.org/resource/": "dbpedia-lmo:",
    "http://lt.dbpedia.org/resource/as": "dbpedia-lt:",
    "http://lv.dbpedia.org/resource/a": "dbpedia-lv:",
    "http://mk.dbpedia.org/resource/": "dbpedia-mk:",
    "http://mr.dbpedia.org/resource/": "dbpedia-mr:",
    "http://ms.dbpedia.org/resource/": "dbpedia-ms:",
    "http://nah.dbpedia.org/resource/": "dbpedia-nah:",
    "http://nds.dbpedia.org/resource/": "dbpedia-nds:",
    "http://nl.dbpedia.org/resource/": "dbpedia-nl:",
    "http://nn.dbpedia.org/resource/": "dbpedia-nn:",
    "http://no.dbpedia.org/resource/": "dbpedia-no:",
    "http://nov.dbpedia.org/resource/": "dbpedia-nov:",
    "http://oc.dbpedia.org/resource/": "dbpedia-oc:",
    "http://os.dbpedia.org/resource/": "dbpedia-os:",
    "http://pam.dbpedia.org/resource/": "dbpedia-pam:",
    "http://pl.dbpedia.org/resource/": "dbpedia-pl:",
    "http://pms.dbpedia.org/resource/": "dbpedia-pms:",
    "http://pnb.dbpedia.org/resource/": "dbpedia-pnb:",
    "http://pt.dbpedia.org/resource/": "dbpedia-pt:",
    "http://ro.dbpedia.org/resource/": "dbpedia-ro:",
    "http://ru.dbpedia.org/resource/": "dbpedia-ru:",
    "http://sh.dbpedia.org/resource/": "dbpedia-sh:",
    "http://simple.dbpedia.org/resource/": "dbpedia-simple:",
    "http://sk.dbpedia.org/resource/": "dbpedia-sk:",
    "http://sl.dbpedia.org/resource/": "dbpedia-sl:",
    "http://sq.dbpedia.org/resource/": "dbpedia-sq:",
    "http://sr.dbpedia.org/resource/": "dbpedia-sr:",
    "http://sv.dbpedia.org/resource/": "dbpedia-sv:",
    "http://sw.dbpedia.org/resource/": "dbpedia-sw:",
    "http://th.dbpedia.org/resource/": "dbpedia-th:",
    "http://tr.dbpedia.org/resource/": "dbpedia-tr:",
    "http://ug.dbpedia.org/resource/": "dbpedia-ug:",
    "http://uk.dbpedia.org/resource/": "dbpedia-uk:",
    "http://vi.dbpedia.org/resource/": "dbpedia-vi:",
    "http://vo.dbpedia.org/resource/": "dbpedia-vo:",
    "http://war.dbpedia.org/resource/": "dbpedia-war:",
    "http://dbpedia.openlinksw.com/wikicompany/": "dbpedia-wikicompany:",
    "http://wikidata.dbpedia.org/resource/": "dbpedia-wikidata:",
    "http://yo.dbpedia.org/resource/": "dbpedia-yo:",
    "http://zh.dbpedia.org/resource/": "dbpedia-zh:",
    "http://zh-min-nan.dbpedia.org/resource/": "dbpedia-zh-min-nan:",
    "http://dbpedia.org/resource/": "dbr:",
    "http://dbpedia.org/resource/Template:": "dbt:",
    "http://purl.org/dc/elements/1.1/": "dc:",
    "http://purl.org/dc/terms/": "dct:",
    "http://digg.com/docs/diggrss/": "digg:",
    "http://www.ontologydesignpatterns.org/ont/dul/DUL.owl": "dul:",
    "urn:ebay:apis:eBLBaseComponents": "ebay:",
    "http://purl.oclc.org/net/rss_2.0/enc#": "enc:",
    "http://www.w3.org/2003/12/exif/ns/": "exif:",
    "http://api.facebook.com/1.0/": "fb:",
    "http://api.friendfeed.com/2008/03": "ff:",
    "http://www.w3.org/2005/xpath-functions/#": "fn:",
    "http://xmlns.com/foaf/0.1/": "foaf:",
    "http://rdf.freebase.com/ns/": "freebase:",
    "http://base.google.com/ns/1.0": "g:",
    "http://www.openlinksw.com/schemas/google-base#": "gb:",
    "http://schemas.google.com/g/2005": "gd:",
    "http://www.w3.org/2003/01/geo/wgs84_pos#": "geo:",
    "http://sws.geonames.org/": "geodata:",
    "http://www.geonames.org/ontology#": "geonames:",
    "http://www.georss.org/georss/": "georss:",
    "http://www.opengis.net/gml": "gml:",
    "http://purl.org/obo/owl/GO#": "go:",
    "http://www.openlinksw.com/schemas/hlisting/": "hlisting:",
    "http://wwww.hoovers.com/": "hoovers:",
    "http:/www.purl.org/stuff/hrev#": "hrev:",
    "http://www.w3.org/2002/12/cal/ical#": "ical:",
    "http://web-semantics.org/ns/image-regions": "ir:",
    "http://www.itunes.com/DTDs/Podcast-1.0.dtd": "itunes:",
    "http://www.w3.org/ns/ldp#": "ldp:",
    "http://linkedgeodata.org/triplify/": "lgdt:",
    "http://linkedgeodata.org/vocabulary#": "lgv:",
    "http://www.xbrl.org/2003/linkbase": "link:",
    "http://lod.openlinksw.com/": "lod:",
    "http://www.w3.org/2000/10/swap/math#": "math:",
    "http://search.yahoo.com/mrss/": "media:",
    "http://purl.org/commons/record/mesh/": "mesh:",
    "urn:oasis:names:tc:opendocument:xmlns:meta:1.0": "meta:",
    "http://www.w3.org/2001/sw/DataAccess/tests/test-manifest#": "mf:",
    "http://musicbrainz.org/ns/mmd-1.0#": "mmd:",
    "http://purl.org/ontology/mo/": "mo:",
    "http://www.freebase.com/": "mql:",
    "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#": "nci:",
    "http://www.semanticdesktop.org/ontologies/nfo/#": "nfo:",
    "http://www.openlinksw.com/schemas/ning#": "ng:",
    "http://data.nytimes.com/": "nyt:",
    "http://www.openarchives.org/OAI/2.0/": "oai:",
    "http://www.openarchives.org/OAI/2.0/oai_dc/": "oai_dc:",
    "http://www.geneontology.org/formats/oboInOwl#": "obo:",
    "urn:oasis:names:tc:opendocument:xmlns:office:1.0": "office:",
    "http://www.opengis.net/": "ogc:",
    "http://www.opengis.net/ont/gml#": "ogcgml:",
    "http://www.opengis.net/ont/geosparql#": "ogcgs:",
    "http://www.opengis.net/def/function/geosparql/": "ogcgsf:",
    "http://www.opengis.net/def/rule/geosparql/": "ogcgsr:",
    "http://www.opengis.net/ont/sf#": "ogcsf:",
    "urn:oasis:names:tc:opendocument:xmlns:meta:1.0:": "oo:",
    "http://a9.com/-/spec/opensearchrss/1.0/": "openSearch:",
    "http://sw.opencyc.org/concept/": "opencyc:",
    "http://www.openlinksw.com/schema/attribution#": "opl:",
    "http://www.openlinksw.com/schemas/getsatisfaction/": "opl-gs:",
    "http://www.openlinksw.com/schemas/meetup/": "opl-meetup:",
    "http://www.openlinksw.com/schemas/xbrl/": "opl-xbrl:",
    "http://www.openlinksw.com/schemas/oplweb#": "oplweb:",
    "http://www.openarchives.org/ore/terms/": "ore:",
    "http://www.w3.org/2002/07/owl#": "owl:",
    "http://www.buy.com/rss/module/productV2/": "product:",
    "http://purl.org/science/protein/bysequence/": "protseq:",
    "http://www.w3.org/ns/prov#": "prov:",
    "http://backend.userland.com/rss2": "r:",
    "http://www.radiopop.co.uk/": "radio:",
    "http://www.w3.org/1999/02/22-rdf-syntax-ns#": "rdf:",
    "http://www.w3.org/ns/rdfa#": "rdfa:",
    "http://www.openlinksw.com/virtrdf-data-formats#": "rdfdf:",
    "http://www.w3.org/2000/01/rdf-schema#": "rdfs:",
    "http://purl.org/stuff/rev#": "rev:",
    "http:/www.purl.org/stuff/rev#": "review:",
    "http://purl.org/rss/1.0/": "rss:",
    "http://purl.org/science/owl/sciencecommons/": "sc:",
    "http://schema.org/": "schema:",
    "http://purl.org/NET/scovo#": "scovo:",
    "http://www.w3.org/ns/sparql-service-description#": "sd:",
    "urn:sobject.enterprise.soap.sforce.com": "sf:",
    "http://rdfs.org/sioc/ns#": "sioc:",
    "http://rdfs.org/sioc/types#": "sioct:",
    "http://www.openlinksw.com/ski_resorts/schema#": "skiresort:",
    "http://www.w3.org/2004/02/skos/core#": "skos:",
    "http://purl.org/rss/1.0/modules/slash/": "slash:",
    "sql:": "sql:",
    "http://xbrlontology.com/ontology/finance/stock_market#": "stock:",
    "http://www.openlinksw.com/schemas/twfy#": "twfy:",
    "http://umbel.org/umbel#": "umbel:",
    "http://umbel.org/umbel/ac/": "umbel-ac:",
    "http://umbel.org/umbel/rc/": "umbel-rc:",
    "http://umbel.org/umbel/sc/": "umbel-sc:",
    "http://purl.uniprot.org/": "uniprot:",
    "http://dbpedia.org/units/": "units:",
    "http://www.rdfabout.com/rdf/schema/uscensus/details/100pct/": "usc:",
    "http://www.openlinksw.com/xsltext/": "v:",
    "http://www.w3.org/2001/vcard-rdf/3.0#": "vcard:",
    "http://www.w3.org/2006/vcard/ns#": "vcard2006:",
    "http://www.openlinksw.com/virtuoso/xslt/": "vi:",
    "http://www.openlinksw.com/virtuoso/xslt": "virt:",
    "http://www.openlinksw.com/schemas/virtcxml#": "virtcxml:",
    "http://www.openlinksw.com/schemas/virtpivot#": "virtpivot:",
    "http://www.openlinksw.com/schemas/virtrdf#": "virtrdf:",
    "http://rdfs.org/ns/void#": "void:",
    "http://www.worldbank.org/": "wb:",
    "http://www.w3.org/2007/05/powder-s#": "wdrs:",
    "http://www.w3.org/2005/01/wf/flow#": "wf:",
    "http://wellformedweb.org/CommentAPI/": "wfw:",
    "http://commons.wikimedia.org/wiki/": "wiki-commons:",
    "http://www.wikidata.org/entity/": "wikidata:",
    "http://en.wikipedia.org/wiki/": "wikipedia-en:",
    "http://www.w3.org/2004/07/xpath-functions": "xf:",
    "http://gmpg.org/xfn/11#": "xfn:",
    "http://www.w3.org/1999/xhtml": "xhtml:",
    "http://www.w3.org/1999/xhtml/vocab#": "xhv:",
    "http://www.xbrl.org/2003/instance": "xi:",
    "http://www.w3.org/XML/1998/namespace": "xml:",
    "http://www.ning.com/atom/1.0": "xn:",
    "http://www.w3.org/2001/XMLSchema#": "xsd:",
    "http://www.w3.org/XSL/Transform/1.0": "xsl10:",
    "http://www.w3.org/1999/XSL/Transform": "xsl1999:",
    "http://www.w3.org/TR/WD-xsl": "xslwd:",
    "urn:yahoo:maps": "y:",
    "http://dbpedia.org/class/yago/": "yago:",
    "http://yago-knowledge.org/resource/": "yago-res:",
    "http://gdata.youtube.com/schemas/2007": "yt:",
    "http://s.zemanta.com/ns#": "zem:",
    "http://www.wikidata.org/prop/statement/": "ps:",
    "http://www.wikidata.org/entity/": "wd:",
    "http://www.wikidata.org/prop/direct/": "wdt:",
    "http://wikiba.se/ontology#": "wikibase:",
    "http://www.wikidata.org/prop/": "p:",
    "http://www.wikidata.org/prop/statement/": "v:",
    "http://www.wikidata.org/prop/qualifier/": "qualifier:",
    "http://www.wikidata.org/prop/statement/": "statement:",
    "http://www.wikidata.org/prop/qualifier/": "pq:",
    "http://www.wikidata.org/prop/reference/": "pr:",
    "http://www.wikidata.org/prop/reference/": "reference:",
    "http://purl.uniprot.org/core/": "up:",
    "http://purl.uniprot.org/database/": "database:",
    "http://purl.uniprot.org/taxonomy/": "taxonomy:",
    "http://www.wikidata.org/prop/qualifier/": "q:",


    }
    for i, l in enumerate(labels):
        for k, v in prefixes.items():
            if k in l:
                labels[i] = l.replace(k, v)
    return labels

with open(os.path.expanduser("~/Desktop/dbpedia_properties.p"), "rb") as f:
    dbpedia_properties = pickle.load(f)


## ATTENTION: contains list of characters
dbpedia_properties = pd.DataFrame(dbpedia_properties).rename(columns={0:'entity', 1:'count'})
dbpedia_properties.to_csv(os.path.expanduser("~/Desktop/dbpedia_properties.csv"))

## ATTENTION: most described are Star Trek characters
wikidata_properties = pd.read_csv(os.path.expanduser("~/Desktop/wikidata_properties_count.csv"))

wikidata_properties_sorted = wikidata_properties.sort_values('count', ascending=0)
wikidata_properties_sorted.iloc[0:100].plot(use_index=False, title="wikidata number of properties per character (first 100)")
plt.show()
plt.close()

wikidata_properties_sorted = wikidata_properties.sort_values('count', ascending=0)
wikidata_properties_sorted.plot(use_index=False, title="wikidata number of properties per character (all)")
plt.show()
plt.close()


dbpedia_properties_sorted = dbpedia_properties.sort_values('count', ascending=0)
dbpedia_properties_sorted.iloc[0:100].plot(use_index=False, title="dbpedia number of properties per character (first 100)")
plt.show()
plt.close()

dbpedia_properties_sorted = dbpedia_properties.sort_values('count', ascending=0)
dbpedia_properties_sorted.plot(use_index=False, title="dbpedia number of properties per character (all)")
plt.show()
plt.close()




dbpedia_characters_propreties_matrix = pd.read_csv(
    os.path.expanduser("~/Desktop/dbpedia_character_properties_matrix.csv"),
    index_col=1
)
wikidata_characters_propreties_matrix = pd.read_csv(
    os.path.expanduser("~/Desktop/wikidata_character_properties_matrix.csv"),
    index_col=1
)

dbpedia_characters_propreties_matrix.columns = relabel_prefixed(dbpedia_characters_propreties_matrix.columns.to_list())
dbpedia_characters_propreties_matrix.index = [i.replace("http://dbpedia.org/resource/", "") for i in list(dbpedia_characters_propreties_matrix.index)]

dbpedia_characters_propreties_matrix = dbpedia_characters_propreties_matrix.drop(
    dbpedia_characters_propreties_matrix.columns[0], axis=1
)
from wikidata.client import Client

client = Client()
wikidata_characters_propreties_matrix.columns = relabel_prefixed(wikidata_characters_propreties_matrix.columns.to_list())
wikidata_characters_propreties_matrix.index = [i.replace("http://www.wikidata.org/entity/", "") for i in list(wikidata_characters_propreties_matrix.index)]
labels = [client.get(e, load=True).label for e in wikidata_characters_propreties_matrix.index.to_list()]
wikidata_characters_propreties_matrix = wikidata_characters_propreties_matrix.drop(
    wikidata_characters_propreties_matrix.columns[0], axis=1
)

sum = dbpedia_characters_propreties_matrix.sum(axis=0).sort_values(ascending=False)
sum.reset_index()
sum.iloc[0:500].plot(figsize=(80, 20), xticks=range(500))
plt.xticks(rotation=90)
plt.tick_params(axis='both', which='major', labelsize=8)
plt.tick_params(axis='both', which='minor', labelsize=8)
plt.savefig(os.path.expanduser("~/Desktop/dbpedia_most_present_predicates.svg"), format="svg")
plt.close()

sum = dbpedia_characters_propreties_matrix.sum(axis=1).sort_values(ascending=False)
sum.reset_index()
sum.iloc[0:500].plot(figsize=(80, 20), xticks=range(500))
plt.xticks(rotation=90)
plt.tick_params(axis='both', which='major', labelsize=6)
plt.tick_params(axis='both', which='minor', labelsize=6)
plt.savefig(os.path.expanduser("~/Desktop/dbpedia_characters_with_mots_predicates.svg"), format="svg")
plt.close()

sum = wikidata_characters_propreties_matrix.sum(axis=0).sort_values(ascending=False)
sum.reset_index()
sum.iloc[0:500].plot(figsize=(80, 20), xticks=range(500))
plt.xticks(rotation=90)
plt.tick_params(axis='both', which='major', labelsize=6)
plt.tick_params(axis='both', which='minor', labelsize=6)
plt.savefig(os.path.expanduser("~/Desktop/wikidata_most_present_predicates.svg"), format="svg")
plt.close()

sum = wikidata_characters_propreties_matrix.sum(axis=1).sort_values(ascending=False)
sum.reset_index()
sum.iloc[0:1000].plot(figsize=(160, 20), xticks=range(1000))
plt.xticks(rotation=90)
plt.tick_params(axis='both', which='major', labelsize=6)
plt.tick_params(axis='both', which='minor', labelsize=6)
plt.savefig(os.path.expanduser("~/Desktop/wikidata_characters_with_mots_predicates.svg"), format="svg")
plt.close()


sum = dbpedia_characters_propreties_matrix.sum(axis=0).sort_values(ascending=False)
sum.reset_index()
sum.iloc[0:100].plot(figsize=(30, 20), xticks=range(100))
plt.xticks(rotation=90)
plt.tick_params(axis='both', which='major', labelsize=8)
plt.tick_params(axis='both', which='minor', labelsize=8)
plt.savefig(os.path.expanduser("~/Desktop/dbpedia_most_present_predicates100.svg"), format="svg")
plt.close()

sum = dbpedia_characters_propreties_matrix.sum(axis=1).sort_values(ascending=False)
sum.reset_index()
sum.iloc[0:100].plot(figsize=(30, 20), xticks=range(100))
plt.xticks(rotation=90)
plt.tick_params(axis='both', which='major', labelsize=6)
plt.tick_params(axis='both', which='minor', labelsize=6)
plt.savefig(os.path.expanduser("~/Desktop/dbpedia_characters_with_mots_predicates100.svg"), format="svg")
plt.close()

sum = wikidata_characters_propreties_matrix.sum(axis=0).sort_values(ascending=False)
sum.reset_index()
sum.iloc[0:100].plot(figsize=(30, 20), xticks=range(100))
plt.xticks(rotation=90)
plt.tick_params(axis='both', which='major', labelsize=6)
plt.tick_params(axis='both', which='minor', labelsize=6)
plt.savefig(os.path.expanduser("~/Desktop/wikidata_most_present_predicates100.svg"), format="svg")
plt.close()

sum = wikidata_characters_propreties_matrix.sum(axis=1).sort_values(ascending=False)
sum.reset_index()
sum.iloc[0:100].plot(figsize=(30, 20), xticks=range(100))
plt.xticks(rotation=90)
plt.tick_params(axis='both', which='major', labelsize=6)
plt.tick_params(axis='both', which='minor', labelsize=6)
plt.savefig(os.path.expanduser("~/Desktop/wikidata_characters_with_mots_predicates100.svg"), format="svg")
plt.close()
