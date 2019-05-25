"""OMDB data loader"""

import requests


base_url = "http://www.omdbapi.com/"


class LoaderException(Exception):
    pass


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
        yield resp.json()


if __name__ == "__main__":
    import argparse
    from pprint import pprint

    parser = argparse.ArgumentParser()
    parser.add_argument("--apikey", dest="api_key", help="OMDB API key")
    parser.add_argument("--search", dest="search", help="The text to search")
    parser.add_argument(
        "--type", dest="media_type", help="Type of media (movie, series or episode)"
    )
    args = parser.parse_args()

    for hit in search_and_fetch(
        api_key=args.api_key, search=args.search, media_type=args.media_type
    ):
        pprint(hit)
