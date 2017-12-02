#SPARQL queries for selecting named enitities

prefixes = """
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX fbase: <http://rdf.freebase.com/ns/>
PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX wds: <http://www.wikidata.org/entity/statement/>
PREFIX wdv: <http://www.wikidata.org/value/>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
"""


#select person entity 
"""
SELECT  ?person 
WHERE
{
	?person wdt:P31 wd:Q5 .       #where ?person isa(wdt:P31) human(wd:Q5)
}
"""

#select organisation enitity 

SELECT ?organisation ?organisation2 
WHERE 
{
  ?organisation wdt:P31 wd:Q43229. #organisation (collective goal)
  ?organisation2 wdt:P31 wd:Q2029841. #organisation (economical concept)
}

#select location enitity 

SELECT ?location ?locationLabel 
WHERE 
{
  ?location wdt:P31 wd:Q17334923. #where ?location isa location
}
