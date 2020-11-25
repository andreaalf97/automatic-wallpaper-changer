from feedparser.util import FeedParserDict
from os import path, mkdir, listdir, remove, system
import requests
import subprocess
from definitions import IMAGES_DIR


def set_wallpaper(wallpaper_path: str) -> int:
    """
    This function calls the correct linux commands which set the wallpaper
    :param wallpaper_path: the path to the image
    :return: 0 if everything went fine
    """

    # Terminal command to retrieve desktop env name
    system_type_command = 'gsettings list-schemas'

    # Executes the command and saves the output
    out = subprocess.run(system_type_command.split(" "), stdout=subprocess.PIPE)

    # Decodes the output to utf-8
    out = out.stdout.decode('utf-8')

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
    set_background_command = 'gsettings set org.' + system_type + '.desktop.background picture-uri FILENAME'

    if not path.isfile(wallpaper_path):
        raise Exception("{} is not a valid path".format(wallpaper_path))

    set_background_command = set_background_command.replace(
        "FILENAME",
        wallpaper_path
    )

    # Runs the command which changes the desktop wallpaper
    valid = system(set_background_command)

    # If execution failed, raises an exception
    if valid != 0:
        raise Exception("Error while executing command '{}'".format(set_background_command))

    return int(valid)


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
        print("DIRECTORY CREATED")

    if clear_directory:
        for file in listdir(images_dir):
            if path.isfile(path.join(images_dir, file)):
                remove(path.join(images_dir, file))

    for i, url in enumerate(img_links, 0):
        img = requests.get(url)
        extension = url.split(".")[-1]
        file_name = str(i) + "." + extension

        print("RECEIVED {}".format(file_name))

        with open(path.join(images_dir, file_name), "wb") as file:
            file.write(img.content)
