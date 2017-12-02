#SPARQL queries for selecting named enitities


#select person entity 
SELECT  ?person 
WHERE
{
	?person wdt:P31 wd:Q5 .       #where ?person isa(wdt:P31) human(wd:Q5)
}

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
