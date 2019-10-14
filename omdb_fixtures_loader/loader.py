"""OMDB data loader"""

from datetime import datetime

import requests

base_url = "http://www.omdbapi.com/"


class LoaderException(Exception):
    pass


SOURCE_OPTION = "source"
DATE_FMT_OPTION = "date_fmt"


def _format_hit(hit: dict, options: dict = {}) -> dict:
    ret_hit = dict((k.lower(), v) for k, v in hit.items())
    del ret_hit["response"]

    for field in ("actors", "genre", "writer"):
        if field not in ret_hit:
            continue
        ret_hit[field] = [x.strip() for x in ret_hit[field].split(",")]

    for field in ("released", "dvd"):
        if field not in ret_hit:
            continue
        try:
            date_value = datetime.strptime(ret_hit[field], "%d %b %Y")
            ret_hit[field] = date_value.strftime(options.get(DATE_FMT_OPTION, "%Y-%m-%d"))
        except ValueError:
            pass

    if SOURCE_OPTION in options:
        source_fields = options.get(SOURCE_OPTION, list())
        return dict((k, v) for k, v in ret_hit.items() if k in source_fields)

    return dict((k, v) for k, v in ret_hit.items())


def search_and_fetch(api_key: str, search: str, media_type: str = "movie", **options):
    """Perform a search against the OMDB database and yield the returned hits

    Arguments:
        api_key {str} -- API key
        search {str} -- The searched text
        media_type {str} -- Type of media: "movie", "series" or "episode"  (default: {"movie"})
        options {dict} -- extra options
            - source: list of fields to return (ex: {"source": ["title", "actors"]})
            - date_fmt: date formatting template (ex: {"date_format": "%Y-%m-%d"})
            (https://docs.python.org/fr/3.6/library/datetime.html?highlight=strftime#strftime-and-strptime-behavior)
    """

    resp = requests.get(
        base_url, params={"apikey": api_key, "type": media_type, "s": search}
    )
    if resp.status_code != 200:
        raise LoaderException(
            "URL {} returned code{}".format(resp.url, resp.status_code)
        )

    json_resp = resp.json()
    if "Search" not in json_resp:
        raise LoaderException(resp.text)

    for hit in json_resp.get("Search"):
        resp = requests.get(
            base_url, params={"apikey": api_key, "i": hit.get("imdbID")}
        )
        yield _format_hit(resp.json(), options)


if __name__ == '__main__':
    from pprint import pprint
    hits = search_and_fetch(api_key="eb88cc", search="back to the future", date_fmt="%Y-%m", source=["title", "released"])
    pprint(list(hits))
