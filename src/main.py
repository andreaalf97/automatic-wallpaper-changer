import feedparser as fp
from os import path
from src.debug import rss_statistics, entries_statistics
from src.rss_tools import get_img_links, url_to_images, set_wallpaper
from definitions import DATETIME_PATH, SUBREDDIT_URL, RSS_REFRESH_RATE_DAYS, WALLPAPER_UPDATE_RATE_MIN
import datetime as dt
"""
This script will be run every hour.
First, it checks the time_info.txt file, which contains the name of the current wallpaper
and the datetime of the last wallpapers refresh
"""


def update_datetime_file(
        wallpaper_change_time: dt.datetime,
        rss_refresh_time: dt.datetime,
        last_image_index: int
):
    with open(DATETIME_PATH, "w") as file:
        file.write("LAST_WALLPAPER_UPDATE={}\n".format(wallpaper_change_time.strftime("%Y/%m/%d %H:%M:%S.%f")))
        file.write("LAST_RSS_REFRESH={}\n".format(rss_refresh_time.strftime("%Y/%m/%d %H:%M:%S.%f")))
        file.write("LAST_IMAGE_INDEX={}\n".format(last_image_index))


def read_datetime() -> dict:
    environment = {}
    with open(DATETIME_PATH, "r") as file:
        key, value = file.readline().replace('\n', '').split('=', 1)  # LAST_WALLPAPER_UPDATE
        environment[key] = dt.datetime.strptime(value, "%Y/%m/%d %H:%M:%S.%f")

        key, value = file.readline().replace('\n', '').split("=", 1)  # LAST_RSS_REFRESH
        environment[key] = dt.datetime.strptime(value, "%Y/%m/%d %H:%M:%S.%f")

        key, value = file.readline().replace('\n', '').split("=", 1)  # LAST_IMAGE_INDEX
        environment[key] = int(value)

    return environment


if __name__ == '__main__':

    if not path.isfile(DATETIME_PATH):
        print(".datetime.txt NOT FOUND....")
        update_datetime_file(
            dt.datetime.strptime("1997/03/10 22:59:00.881997", "%Y/%m/%d %H:%M:%S.%f"),
            dt.datetime.strptime("1997/03/10 22:59:00.881997", "%Y/%m/%d %H:%M:%S.%f"),
            -1
        )
        print(".datetime.txt CREATED")

    environment: dict = read_datetime()

    for key in environment:
        print("{} --> {}".format(key, environment[key]))

    now = dt.datetime.now()

    delta: dt.timedelta = now - environment["LAST_WALLPAPER_UPDATE"]
    if delta.seconds > WALLPAPER_UPDATE_RATE_MIN * 60:  # Update wallpaper if one hour has passed since last update

        last_image: int = environment["LAST_IMAGE_INDEX"]

        pass

    delta: dt.timedelta = now - environment["LAST_RSS_REFRESH"]
    if delta.days >= RSS_REFRESH_RATE_DAYS:  # Refresh rss if N days have passed
        pass











    exit(-1)


    rss = fp.parse(SUBREDDIT_URL)
    # rss = fp.parse("../testingFiles/MinimalWallpaper.rss")

    # img_links = get_img_links(rss, exclude_galleries=True)
    # print("\n".join(img_links))

    # url_to_images(img_links, clear_directory=True)

    set_wallpaper("/home/andreaalf/Documents/Other/automatic-wallpaper-changer/images/7.jpg")
