## DEPRECIATED: Site is currently not working.

import sparql  # type: ignore[import] # Can't find stubs

s = sparql.Service("http://dati.culturaitalia.it", "utf-8", "GET")
QUERY_STR = "SELECT DISTINCT ?class WHERE { ?s a ?class . } LIMIT 25 OFFSET 0"
result = s.query(QUERY_STR)
print(result)
