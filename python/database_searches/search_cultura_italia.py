#!/usr/bin/env python3

## DEPRECIATED: Site is currently not working.

import sparql  # type: ignore # Can't find stubs

s = sparql.Service("http://dati.culturaitalia.it", "utf-8", "GET")
q = "SELECT DISTINCT ?class WHERE { ?s a ?class . } LIMIT 25 OFFSET 0"
result = s.query(q)
print(result)
