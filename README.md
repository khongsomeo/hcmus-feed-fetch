# Feed Fetcher for HCMUS

A small project by [@KhongSoMeo](https://github.com/khongsomeo) to track some website's posts using RSS.

Licensed under [The GPU GPL v3.0](LICENSE)

## Basic use
### 1. Clone the project

```
git clone git@github.com:khongsomeo/hcmus-feed-fetch.git
```

### 2. Install required packages

```
cd hcmus-feed-fetch
pip install -r requirements.txt
```

### 3. Run

```
usage: feed_fetch.py [-h] --urls URLS [--save SAVE]

optional arguments:
  -h, --help   show this help message and exit
  --urls URLS  JSON file stores list of RSS (default: None)
  --save SAVE  Saving new news (if any) to a file (default: feed.txt)
```

- If there are new feeds, they'll be fetch and save on **the feed file (feed.txt by default)**.

## Keywords mentioning

Inside `config/keywords.txt`, add more keywords. When a title (has these keywords) is fetched, a notice will be print out on the screen.

## Reset configuration

```
bash clean.sh
```
