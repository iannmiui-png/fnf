"""
Quote-post your own pinned post, with an added message.

Env vars required:
    BSKY_HANDLE
    BSKY_APP_PASSWORD
    POST_TEXT   -- the message to add above the quoted post
"""

import os
from atproto import Client, models

HANDLE = os.environ["BSKY_HANDLE"]
APP_PASSWORD = os.environ["BSKY_APP_PASSWORD"]
POST_TEXT = os.environ["POST_TEXT"]


def main():
    if not POST_TEXT.strip():
        raise SystemExit("POST_TEXT is empty, nothing to post.")

    client = Client()
    client.login(HANDLE, APP_PASSWORD)

    profile = client.app.bsky.actor.get_profile({"actor": HANDLE})
    pinned = getattr(profile, "pinned_post", None)

    if not pinned:
        raise SystemExit(
            "No pinned post found on your profile. "
            "Pin a post in the Bluesky app first (open the post -> ... -> Pin to your profile)."
        )

    embed = models.AppBskyEmbedRecord.Main(
        record=models.ComAtprotoRepoStrongRef.Main(uri=pinned.uri, cid=pinned.cid)
    )

    client.send_post(text=POST_TEXT, embed=embed)
    print("Quote-posted your pinned post successfully.")
    print(f"Added text: {POST_TEXT}")


if __name__ == "__main__":
    main()
