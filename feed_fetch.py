import feedparser
import json
from datetime import datetime
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter

CONF_FILE = "conf.json"

def main():
    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("--urls", required=True, help="JSON file stores list of RSS")
    parser.add_argument("--save", default="feed.txt", help="Saving new news (if any) to a file")

    args = parser.parse_args()


    # Load urls and configuration file.

    with open(args.urls, "r+", encoding="utf8") as f:
        urls_dict = json.load(f)

    try:
        with open(CONF_FILE, "r+") as f:
            conf_dict = json.load(f)
            last_update_date = datetime.fromisoformat(conf_dict["last_update"])
    except:
        conf_dict = {"last_update" : None}
        last_update_date = None

    # Get current timestamps for later logs.
    current_date = datetime.now()

    with open(args.save, "w+") as f:
        for url_alias in urls_dict:
            url_obj = urls_dict[url_alias]

            url_fullname = url_obj["name"]
            url = url_obj["url"]

            print(f"Fetching {url_fullname} ({url})")

            has_news = False

            feed_list = feedparser.parse(url)["entries"]
            for feed in feed_list:
                feed_title = feed["title"]
                feed_published = datetime(*feed["published_parsed"][:6])
                feed_url = feed["link"]

                if last_update_date is None or feed_published.date() > last_update_date.date():
                    has_news = True
                    
                    print(f"Title: {feed_title}", file = f)
                    print(f"URL: {feed_url}", file = f)
                    print(f"Published on {feed_published}", file = f)
                    print("-" * 10, file = f)

    if has_news is False:
        print("No new news!")
    else:
        print(f"There are some new news, saved in {args.save}")

    conf_dict["last_update"] = current_date.__str__()
    with open(CONF_FILE, "w+") as f:
        json.dump(obj = conf_dict, fp = f)

if __name__ == "__main__":
    main()
