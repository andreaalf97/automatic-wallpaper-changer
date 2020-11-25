"""
This script will be run every 10 minutes.
First, it checks the time_info.txt file, which contains the name of the current wallpaper
and the datetime of the last wallpapers refresh
"""

from feedparser.util import FeedParserDict
from os import path, mkdir, listdir, remove, system
from os.path import isfile
import requests
import subprocess
import feedparser as fp
import datetime as dt

# SUBREDDIT_URL = "https://www.reddit.com/r/MinimalWallpaper/top/.rss?t=week"

ROOT_DIR = path.dirname(path.abspath(__file__))  # This is the src root
IMAGES_DIR = path.join(ROOT_DIR, "images")
DATETIME_PATH = path.join(ROOT_DIR, ".datetime.txt")
SUBREDDIT_URL = "https://www.reddit.com/r/wallpaper/top/.rss?t=week"
WALLPAPER_UPDATE_RATE_MIN = 30
RSS_REFRESH_RATE_DAYS = 6


def print_log(out: str):
    print("[{}]--{}".format(str(dt.datetime.now()), out))

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

    print_log("The item following image {} was not found. Restarting from image 0.{}".format(last_image_index, zero_ext))

    # If the following image was not found, we return image 0
    return (
        0,
        path.join(IMAGES_DIR, "0.{}".format(zero_ext))
    )


def set_wallpaper(wallpaper_path: str) -> int:
    """
    This function calls the correct linux commands which set the wallpaper
    :param wallpaper_path: the path to the image
    :return: 0 if everything went fine
    """

    # Terminal command to retrieve desktop env name
    system_type_command = 'gsettings list-schemas'

    # Executes the command and saves the output
    out = subprocess.run(system_type_command.split(" "), stdout=subprocess.PIPE).stdout.decode('utf-8')

    # Reads the desktop env name
    system_type = "na"
    for line in out.splitlines():
        if "desktop.background" in line:
            system_type = line.replace("org.", "").replace(".desktop.background", "").lower()
            break

    available_envs = ["gnome", "cinnamon"]

    if system_type == "na":
        raise Exception("Could not retrieve desktop environment name. Compatible envs: " + "/".join(available_envs))

    if system_type not in available_envs:
        raise Exception(
            "Unknown desktop environment '{}'. Compatible envs: ".format(system_type) + "/".join(available_envs)
        )

    # Terminal command to set the background
    set_background_command = '/usr/bin/gsettings set org.' + system_type + '.desktop.background picture-uri FILENAME'

    if not isfile(wallpaper_path):
        raise Exception("{} is not a valid path".format(wallpaper_path))

    set_background_command = set_background_command.replace(
        "FILENAME",
        wallpaper_path
    )
    
    #print_log("Trying command {}".format(set_background_command))

    # Runs the command which changes the desktop wallpaper
    subprocess.Popen(set_background_command, shell=True)

    return 0


def get_html_summaries(rss: FeedParserDict) -> list:
    """
    Returns the entries formatted as HTML from the rss
    :param rss: the already parsed rss
    :return: the list of HTML summaries
    """
    return [entry["summary"] for entry in rss["entries"]]


def get_img_links(rss: FeedParserDict, exclude_galleries=True) -> list:
    """
    This function takes the rss as input and extracts the list of links to the wallpapers
    :param rss: the already parsed rss in FeedParserDict format
    :param exclude_galleries: if True, the url to image galleries will not be added to the list
    :return: the list of valid urls
    """

    html_summaries = get_html_summaries(rss)

    url_list = []

    for summary in html_summaries:
        split_list = summary.split("<")
        split_list = [el.replace(">", "") for el in split_list]

        if len(split_list) != 23:
            raise Exception("This summary should contain 23 tags, has {} instead".format(len(split_list)))

        link_found = False
        for tag in split_list:
            if "[link]" in tag and not link_found:
                link_found = True
                url = tag.split('"', 1)[1].split('"', 1)[0]
                if exclude_galleries and "gallery" in url:
                    continue
                url_list.append(url)

        if not link_found:
            raise Exception("The rss entry contained 23 HTML tags but [link] was not found")

    return url_list


def url_to_images(img_links: list, images_dir: str, clear_directory=True) -> None:
    """
    This function takes a list of urls which point directly to an image and download it into the 'images' folder
    :param img_links: the list of urls
    :param clear_directory: if True, all files in the 'images' folder will be deleted
    :return None
    """

    if not path.isdir(images_dir):
        mkdir(images_dir)
        print_log("DIRECTORY CREATED")

    if clear_directory:
        for file in listdir(images_dir):
            if isfile(path.join(images_dir, file)):
                remove(path.join(images_dir, file))

    for i, url in enumerate(img_links, 0):
        img = requests.get(url)
        extension = url.split(".")[-1]
        file_name = str(i) + "." + extension

        print_log("RECEIVED {}".format(file_name))

        with open(path.join(images_dir, file_name), "wb") as file:
            file.write(img.content)


if __name__ == '__main__':

    # If the DATETIME file does not exist yet, it is initialized
    if not isfile(DATETIME_PATH):
        print_log(".datetime.txt NOT FOUND....")
        update_datetime_file(
            dt.datetime.strptime("1997/03/10 22:59:00.881997", "%Y/%m/%d %H:%M:%S.%f"),
            dt.datetime.strptime("1997/03/10 22:59:00.881997", "%Y/%m/%d %H:%M:%S.%f"),
            -1
        )
        print_log(".datetime.txt CREATED")

    # Reads the DATETIME file into a dictionary
    environment: dict = read_datetime()

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
    if delta.days > 0 or delta.seconds > WALLPAPER_UPDATE_RATE_MIN * 60:  # Update wallpaper if X minutes have passed since last update
        last_image_index: int = environment["LAST_IMAGE_INDEX"]

        new_image_index, path = get_next_image(last_image_index)

        print_log("New image index: {}\nPath: {}".format(new_image_index, path))

        set_wallpaper(path)
        update_datetime_file(
            dt.datetime.now(),
            environment["LAST_RSS_REFRESH"],
            new_image_index
        )

        exit(0)

    print_log("NOTHING CHANGED")
    exit(0)
