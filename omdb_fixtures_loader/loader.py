"""OMDB data loader"""

import requests

base_url = "http://www.omdbapi.com/"


class LoaderException(Exception):
    pass


def _format_hit(hit: dict) -> dict:
    ret_hit = dict((k.lower(), v) for k, v in hit.items())
    for field in ("actors", "genre",):
        ret_hit[field] = [x.trim() for x in ret_hit[field].split(",")]
    return ret_hit


def search_and_fetch(api_key: str, search: str, media_type: str = "movie"):
    """Perform a search against the OMDB database and yield the returned hits

    Arguments:
        api_key {str} -- API key
        search {str} -- The searched text

    Keyword Arguments:
        media_type {str} -- Type of media: "movie", "series" or "episode"  (default: {"movie"})
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
        yield _format_hit(resp.json())
