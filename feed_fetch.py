import feedparser
import json
import os
from datetime import datetime
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter

CONF_FILE = "config/conf.json"
KEYW_FILE = "config/keywords.txt"
LOG_FOLDER = "logs"

def main():
    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("--urls", required=True, help="JSON file stores list of RSS")
    parser.add_argument("--save", default="feed.txt", help="Saving new news (if any) to a file")

    args = parser.parse_args()


    # Load urls and configuration file.

    with open(args.urls, "r+", encoding="utf8") as f:
        urls_dict = json.load(f)

    with open(KEYW_FILE, "r+", encoding="utf8") as f:
        keys_list = [line.strip() for line in f.readlines()]

    try:
        with open(CONF_FILE, "r+") as f:
            conf_dict = json.load(f)
            last_update_date = datetime.fromisoformat(conf_dict["last_update"])
    except:
        conf_dict = {"last_update" : None}
        last_update_date = None

    # Create log folder if not exist
    if not os.path.exists(LOG_FOLDER):
        os.makedirs(LOG_FOLDER)
        
    # Get current timestamps for later logs.
    current_date = datetime.now()
    current_date_day = current_date.strftime("%Y-%m-%d")
    current_date_time = current_date.strftime("%H-%M-%S")
        
    # Create current date folder if not exist
    if not os.path.exists(f"{LOG_FOLDER}/{current_date_day}"):
        os.makedirs(f"{LOG_FOLDER}/{current_date_day}")

    # Filename to save
    save_filename = f"{LOG_FOLDER}/{current_date_day}/{current_date_time}-{args.save}"

    has_change = False

    with open(save_filename, "w+", encoding="utf8") as f:
        for url_alias in urls_dict:
            url_obj = urls_dict[url_alias]

            url_fullname = url_obj["name"]
            url = url_obj["url"]

            print(f"Fetching {url_fullname} ({url})")

            # Is this alias has a new news?
            has_news = False

            # Set of (need to focus) news.
            focus_news = set()

            feed_list = feedparser.parse(url)["entries"]
            for feed in feed_list:
                feed_title = feed["title"]
                feed_published = datetime(*feed["published_parsed"][:6])
                feed_url = feed["link"]

                if last_update_date is None or feed_published > last_update_date:
                    has_news = True

                    has_change |= has_news

                    print(f"Title: {feed_title}", file = f)
                    print(f"URL: {feed_url}", file = f)
                    print(f"Published on {feed_published}", file = f)
                    print("-" * 10, file = f)

                    for key in keys_list:
                        if key.lower() in feed_title.lower():
                            focus_news.add(feed_title)

            if has_news is False:
                print(f"No new news in {url_fullname}!")
            else:
                print(f"There are some new news in {url_fullname}, saved in {save_filename}")

                if len(focus_news) > 0:
                    print(f"There are {len(focus_news)} important news:")
                    for news in focus_news:
                        print(f"- {news}")

            print("-" * 10)

    # Don't save a file if no news fetched
    if has_change is False:
        os.remove(save_filename)

    conf_dict["last_update"] = current_date.__str__()
    with open(CONF_FILE, "w+") as f:
        json.dump(obj = conf_dict, fp = f)

if __name__ == "__main__":
    main()
