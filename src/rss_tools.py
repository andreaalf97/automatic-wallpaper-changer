from feedparser.util import FeedParserDict
from os import path, mkdir, listdir, remove, system
import requests
import subprocess
from definitions import IMAGES_DIR


def run_linux_commands():

    system_type_command = 'gsettings list-schemas'

    out = subprocess.run(system_type_command.split(" "), stdout=subprocess.PIPE)

    out = out.stdout.decode('utf-8')

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

    set_background_command = 'gsettings set org.' + system_type + '.desktop.background picture-uri FILENAME'

    set_background_command = set_background_command.replace(
        "FILENAME",
        "/home/andreaalf/Documents/Other/automatic-wallpaper-changer/images/1.png"
    )

    valid = system(set_background_command)

    if valid != 0:
        raise Exception("Error while executing command '{}'".format(set_background_command))

    print("VALID:", valid)


def get_html_summaries(rss: FeedParserDict) -> list:
    return [entry["summary"] for entry in rss["entries"]]


def get_img_links(rss: FeedParserDict, exclude_galleries=False) -> list:
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


def url_to_images(img_links: list, clear_directory=False, exclude_galleries=True):

    if not path.isdir(IMAGES_DIR):
        mkdir(IMAGES_DIR)
        print("DIRECTORY CREATED")

    if clear_directory:
        for file in listdir(IMAGES_DIR):
            if path.isfile(path.join(IMAGES_DIR, file)):
                remove(path.join(IMAGES_DIR, file))

    for i, url in enumerate(img_links, 0):
        img = requests.get(url)
        extension = url.split(".")[-1]
        file_name = str(i) + "." + extension

        with open(path.join(IMAGES_DIR, file_name), "wb") as file:
            file.write(img.content)
