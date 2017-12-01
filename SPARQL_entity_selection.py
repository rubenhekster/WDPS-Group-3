"""
SELECT DISTINCT ?s WHERE {
?s <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://dbpedia.org/ontology/Person> .
} LIMIT 100
"""

# example 100 cats from Wikidata :
"""
SELECT DISTINCT ?s WHERE {
?s <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.wikidata.org/entity/Q146> .
} LIMIT 100
"""

# presidents from the US from Freebase:
"""
SELECT DISTINCT ?s WHERE {
?s <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://rdf.freebase.com/ns/government.us_president> .
}
"""

"""
SPARQL: 
IsA : wdt:P31
location:wd:Q17334923
organisation: wd:Q43229, wd:Q2029841
person: wd:Q5
"""

"""
SELECT ?item ?itemLabel 
WHERE {
  ?item wdt:P31 wd:Q146.
}
