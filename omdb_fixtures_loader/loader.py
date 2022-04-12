"""OMDB data loader"""

from datetime import datetime

import requests

base_url = "http://www.omdbapi.com/"


class LoaderError(Exception):
    pass


SOURCE_OPTION = "source"
DATE_FMT_OPTION = "date_fmt"


def _format_rating_value(value: str) -> int:
    if value.endswith("%"):
        return int(value.replace("%", "").strip())
    if value.endswith("/100"):
        return int(value.replace("/100", "").strip())
    if value.endswith("/10"):
        return int(float(value.replace("/10", "").strip()) * 10)
    return 0


def _format_hit(hit: dict, options: dict = {}) -> dict:
    ret_hit = dict((k.lower(), v) for k, v in hit.items())
    del ret_hit["response"]

    for field in ("actors", "genre", "writer", "language"):
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

    ret_hit["boxoffice"] = str(ret_hit["boxoffice"]).replace("$", "").replace(",", "")
    ret_hit["imdbvotes"] = str(ret_hit["imdbvotes"]).replace(",", "")
    ret_hit["runtime"] = str(ret_hit["imdbvotes"]).replace("min", "").strip()

    # rename movie type field to avoid problems with type keyword
    ret_hit["movie_type"] = ret_hit.pop("type")

    ratings = []
    for rating in ret_hit.pop("ratings"):
        ratings.append(
            {
                "source": rating.get("Source"),
                "value": _format_rating_value(value=rating.get("Value")),
            }
        )
    ret_hit["ratings"] = ratings

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

    resp = requests.get(base_url, params={"apikey": api_key, "type": media_type, "s": search})
    if resp.status_code != 200:
        raise LoaderError("URL {} returned code{}".format(resp.url, resp.status_code))

    json_resp = resp.json()
    if "Search" not in json_resp:
        raise LoaderError(resp.text)

    for hit in json_resp.get("Search"):
        resp = requests.get(base_url, params={"apikey": api_key, "i": hit.get("imdbID")})
        yield _format_hit(resp.json(), options)
