"""
Post a single text post to Bluesky.

Env vars required:
    BSKY_HANDLE
    BSKY_APP_PASSWORD
    POST_TEXT
"""

import os
from atproto import Client

HANDLE = os.environ["BSKY_HANDLE"]
APP_PASSWORD = os.environ["BSKY_APP_PASSWORD"]
POST_TEXT = os.environ["POST_TEXT"]


def main():
    if not POST_TEXT.strip():
        raise SystemExit("POST_TEXT is empty, nothing to post.")

    client = Client()
    client.login(HANDLE, APP_PASSWORD)

    client.send_post(text=POST_TEXT)
    print("Posted successfully.")
    print(f"Text: {POST_TEXT}")


if __name__ == "__main__":
    main()
