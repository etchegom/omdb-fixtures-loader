# omdb-fixtures-loader

Fetch data from [The Open Movie Database](http://www.omdbapi.com/) API, in order to populate fixtures for dev purpose.

1. Get an API key
http://www.omdbapi.com/apikey.aspx

2. Use loader to fetch data
Ex:
```
from omdb_fixtures_loader import loader

for hit in loader.search_and_fetch(api_key="xxxxxxx", search="avengers"):
    do_something(hit)
```
