import feedparser as fp
from src.debug import rss_statistics, entries_statistics
from src.rss_tools import get_img_links, url_to_images, run_linux_commands

# url = "https://www.reddit.com/r/MinimalWallpaper/top/.rss?t=week"
url = "https://www.reddit.com/r/MinimalWallpaper/.rss"

rss = fp.parse(url)
# rss = fp.parse("../testingFiles/MinimalWallpaper.rss")
# rss_statistics(rss, url=url)

# entries = rss["entries"]

# entries_statistics(entries)

img_links = get_img_links(rss, exclude_galleries=True)
# print("\n".join(img_links))

# url_to_images(img_links, clear_directory=True)

run_linux_commands()