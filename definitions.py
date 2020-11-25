import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))  # This is the src root

IMAGES_DIR = os.path.join(ROOT_DIR, "images")

DATETIME_PATH = os.path.join(ROOT_DIR, ".datetime.txt")

SUBREDDIT_URL = "https://www.reddit.com/r/wallpaper/top/.rss?t=week"
# SUBREDDIT_URL = "https://www.reddit.com/r/MinimalWallpaper/top/.rss?t=week"

WALLPAPER_UPDATE_RATE_MIN = 30

RSS_REFRESH_RATE_DAYS = 6
