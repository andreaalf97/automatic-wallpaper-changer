from feedparser.util import FeedParserDict


def entries_statistics(entries: list, show_list_type=False):
    """
        [0] authors --> <class 'list'>
        [1] author_detail --> <class 'feedparser.util.FeedParserDict'>
        [2] href --> <class 'str'>
        [3] author --> <class 'str'>
        [4] tags --> <class 'list'>
        [5] content --> <class 'list'>
        [6] summary --> <class 'str'>
        [7] id --> <class 'str'>
        [8] guidislink --> <class 'bool'>
        [9] link --> <class 'str'>
        [10] media_thumbnail --> <class 'list'>
        [11] links --> <class 'list'>
        [12] updated --> <class 'str'>
        [13] updated_parsed --> <class 'time.struct_time'>
        [14] title --> <class 'str'>
        [15] title_detail --> <class 'feedparser.util.FeedParserDict'>
    """
    for entry in entries:

        print("There are {} keys in each entry".format(len(entry)))

        if show_list_type:
            for i, key in enumerate(entry):
                print("[{}] {} -->".format(i, key), type(entry[key]))

        print("[author]", entry["author"].replace("/u/", ""))

        print("[tags]", [tag["term"] for tag in entry["tags"]])

        for element in entry["content"]:
            print("[content] Each entry is a dict with keys {}".format([key for key in element]))
            print("[content] --- TYPE: ", element["type"])
            print("[content] --- LANGUAGE: ", element["language"])
            print("[content] --- BASE: ", element["base"])
            print("[content] --- VALUE: {}...".format(element["value"][:30]))
            print("[content] --- VALUE contains {} HTML tags".format(element["value"].count("<")))

        # with open("../testingFiles/content_value_example.html", "a") as file:
        #     file.write(entry["summary"])

        print("[summary]", entry["summary"])

        print("[id]", entry["id"])

        print("[guidislink]", entry["guidislink"])

        print("[link]", entry["link"])

        for media in entry["media_thumbnail"]:
            print("[media]", media)

        for link in entry["links"]:
            print("[links]", link)

        print("[updated]", entry["updated"])

        print("[updated_parsed]", entry["updated_parsed"])

        print("[title]", entry["title"])

        print("[title_detail]", entry["title_detail"])



        break



def rss_statistics(rss: FeedParserDict, url="https://www.reddit.com/r/MinimalWallpaper/top/.rss?t=week"):
    """
    'entries' --> This is a list of dictionaries, each dictionary is a post from one author
    'feed' --> a dictionary of data about the feed
    'headers' --> A dictionary of all the HTTP headers received from the web server when retrieving the feed.
    'href' --> contains the url the RSS was retrieved from (useful for redirections)
    'status' --> the HTTP status code
    'encoding' --> The character encoding that was used to parse the feed
    'version' --> The format and version of the feed
    'namespaces' --> namespaces used by this file
    :param rss: The retrieved RSS, must be a feedparser.util.FeedParserDict
    :param url: The url used to retrieve the RSS
    :return: n/a
    """

    if rss["bozo"]:
        print("[bozo]\t\t\tThe file is not properly XML formatted")
    else:
        print("[bozo]\t\t\tThe file is properly XML formatted")

    entries = rss["entries"]
    print("[entries]\t\tThere are {} posts in this RSS".format(len(entries)))

    feed = rss["feed"]
    print("[feed]\t\t\tThe feed dictionary contains {} keys such as {}".format(len(feed.keys()), [
        "tags",
        "title",
        "logo"
    ]))

    headers: dict = rss["headers"]
    print("[headers]\t\tThe headers dict contains {} keys".format(len(headers.keys())))

    try:
        href = rss["href"]
        if href != url:
            print("[href]\t\t\tThe request was redirected to {}".format(href))
        else:
            print("[href]\t\t\tThe request was not redirected")
    except:
        print("[href]\t\t\tNo 'href' key found")

    try:
        status = rss["status"]
        print("[status]\t\tHTTP status code: {}".format(status))
    except:
        print("[status]\t\tNo 'status' key found")


    encoding = rss["encoding"]
    print("[encoding]\t\tThe character encoding used to parse the feed:", encoding)

    version = rss["version"]
    print("[version]\t\tThe version of the feed is :", version)

    namespaces = rss["namespaces"]
    for key in namespaces:
        print("[namespaces]\t" + "'" + str(key) + "'" + " : " + str(namespaces[key]))
