"""
Search Bluesky for mutual-aid-related accounts and follow them.

Env vars required:
    BSKY_HANDLE
    BSKY_APP_PASSWORD
"""

import os
import time
from atproto import Client

HANDLE = os.environ["BSKY_HANDLE"]
APP_PASSWORD = os.environ["BSKY_APP_PASSWORD"]

SEARCH_TERMS = [
    "mutual aid",
    "#mutualaid",
    "community fridge",
    "mutual aid network",
]

MAX_RESULTS_PER_TERM = 25
MAX_NEW_FOLLOWS_PER_RUN = 30   # cap so a single run can't mass-follow hundreds at once
DELAY_BETWEEN_FOLLOWS = 5      # seconds, keeps you well under rate limits


def collect_candidates(client, terms, max_per_term):
    seen = {}
    for term in terms:
        results = client.app.bsky.feed.search_posts({"q": term, "limit": max_per_term})
        for post in results.posts:
            author = post.author
            if author.did not in seen:
                seen[author.did] = author
        time.sleep(1)
    return list(seen.values())


def main():
    client = Client()
    client.login(HANDLE, APP_PASSWORD)

    candidates = collect_candidates(client, SEARCH_TERMS, MAX_RESULTS_PER_TERM)
    print(f"Found {len(candidates)} unique accounts across all search terms.")

    followed = 0
    for author in candidates:
        if followed >= MAX_NEW_FOLLOWS_PER_RUN:
            print("Hit per-run follow cap, stopping for this run.")
            break
        try:
            profile = client.app.bsky.actor.get_profile({"actor": author.handle})
            if getattr(profile.viewer, "following", None):
                continue  # already following
            client.follow(author.did)
            followed += 1
            print(f"Followed @{author.handle}")
        except Exception as e:
            print(f"Failed on @{author.handle}: {e}")
        time.sleep(DELAY_BETWEEN_FOLLOWS)

    print(f"Done. Followed {followed} new accounts this run.")


if __name__ == "__main__":
    main()
