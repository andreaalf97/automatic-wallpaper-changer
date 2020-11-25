import feedparser as fp
import datetime as dt
from os import path, listdir
from definitions import DATETIME_PATH, SUBREDDIT_URL, RSS_REFRESH_RATE_DAYS, WALLPAPER_UPDATE_RATE_MIN, IMAGES_DIR
from src.debug import rss_statistics, entries_statistics
from src.rss_tools import get_img_links, url_to_images, set_wallpaper
"""
This script will be run every hour.
First, it checks the time_info.txt file, which contains the name of the current wallpaper
and the datetime of the last wallpapers refresh
"""


def update_datetime_file(
        wallpaper_change_time: dt.datetime,
        rss_refresh_time: dt.datetime,
        last_img_index: int
) -> None:
    """
    This function rewrites the DATETIME file with the new parameters
    :param wallpaper_change_time: the last time the wallpaper was changed
    :param rss_refresh_time: the last time the RSS was loaded from Reddit
    :param last_img_index: the last image set as
    :return: None
    """
    with open(DATETIME_PATH, "w") as file:
        file.write("LAST_WALLPAPER_UPDATE={}\n".format(wallpaper_change_time.strftime("%Y/%m/%d %H:%M:%S.%f")))
        file.write("LAST_RSS_REFRESH={}\n".format(rss_refresh_time.strftime("%Y/%m/%d %H:%M:%S.%f")))
        file.write("LAST_IMAGE_INDEX={}\n".format(last_img_index))


def read_datetime() -> dict:
    """
    Reads the DATETIME file and returns it in a dictionary
    :return: the dict containing all the env variables from the DATETIME file
    """
    env = {}
    with open(DATETIME_PATH, "r") as file:
        k, v = file.readline().replace('\n', '').split('=', 1)  # LAST_WALLPAPER_UPDATE
        env[k] = dt.datetime.strptime(v, "%Y/%m/%d %H:%M:%S.%f")

        k, v = file.readline().replace('\n', '').split("=", 1)  # LAST_RSS_REFRESH
        env[k] = dt.datetime.strptime(v, "%Y/%m/%d %H:%M:%S.%f")

        k, v = file.readline().replace('\n', '').split("=", 1)  # LAST_IMAGE_INDEX
        env[k] = int(v)

    return env


def get_next_image(last_image_index: int) -> (int, str):

    for image in listdir(IMAGES_DIR):
        image_index, extension = int(image.split(".")[0]), image.split(".")[1]

        if image_index == 0:
            zero_ext = extension

        if image_index == last_image_index + 1:
            return (
                image_index,
                path.join(IMAGES_DIR, image)
            )

    print("The item following image {} was not found. Restarting from image 0.{}".format(last_image_index, zero_ext))

    # If the following image was not found, we return image 0
    return (
        0,
        path.join(IMAGES_DIR, "0.{}".format(zero_ext))
    )


if __name__ == '__main__':

    # If the DATETIME file does not exist yet, it is initialized
    if not path.isfile(DATETIME_PATH):
        print(".datetime.txt NOT FOUND....")
        update_datetime_file(
            dt.datetime.strptime("1997/03/10 22:59:00.881997", "%Y/%m/%d %H:%M:%S.%f"),
            dt.datetime.strptime("1997/03/10 22:59:00.881997", "%Y/%m/%d %H:%M:%S.%f"),
            -1
        )
        print(".datetime.txt CREATED")

    # Reads the DATETIME file into a dictionary
    environment: dict = read_datetime()

    for key in environment:
        print("{} --> {}".format(key, environment[key]))

    now = dt.datetime.now()

    delta: dt.timedelta = now - environment["LAST_RSS_REFRESH"]
    if delta.days >= RSS_REFRESH_RATE_DAYS:  # Refresh rss if N days have passed
        rss = fp.parse(SUBREDDIT_URL)
        img_links = get_img_links(rss)

        url_to_images(img_links, IMAGES_DIR)

        new_image_index, path = get_next_image(-1)

        set_wallpaper(path)
        update_datetime_file(
            dt.datetime.now(),
            dt.datetime.now(),
            0
        )
        exit(0)

    delta: dt.timedelta = now - environment["LAST_WALLPAPER_UPDATE"]
    # if delta.seconds > 1:  # Update wallpaper if X minutes have passed since last update
    if delta.seconds > WALLPAPER_UPDATE_RATE_MIN * 60:  # Update wallpaper if X minutes have passed since last update
        last_image_index: int = environment["LAST_IMAGE_INDEX"]

        new_image_index, path = get_next_image(last_image_index)

        print("New image index: {}\nPath: {}".format(new_image_index, path))

        set_wallpaper(path)
        update_datetime_file(
            dt.datetime.now(),
            environment["LAST_RSS_REFRESH"],
            new_image_index
        )

        exit(0)

    print("NOTHING CHANGED")
    exit(-1)
