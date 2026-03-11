"""Fetch and display a random joke from the official joke API."""

import json
import urllib.error
import urllib.request

JOKE_URL = "https://official-joke-api.appspot.com/random_joke"


def fetch_joke() -> dict:
    """Fetch a random joke from the API and return its JSON data."""
    with urllib.request.urlopen(JOKE_URL, timeout=10) as response:
        data = response.read()
    return json.loads(data)


def main() -> None:
    try:
        joke = fetch_joke()
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError):
        print("Oops! Could not fetch a joke right now. Check your internet connection and try again.")
        return

    print(joke["setup"])
    input("\nPress Enter for the punchline...")
    print(joke["punchline"])


if __name__ == "__main__":
    main()
