from feedparser.util import FeedParserDict
from os import path, mkdir, listdir, remove, system
import requests
import subprocess
from definitions import IMAGES_DIR


def run_linux_commands():



    system_type_command = 'gsettings list-schemas | grep "desktop.background"'

    out = system(system_type_command)
    print(type(out))

    y = 'gsettings set org.gnome.desktop.background picture-uri "/home/andreaalf/Documents/Other/automatic-wallpaper-changer/images/0.png"'


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
