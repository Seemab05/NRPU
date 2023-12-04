# all import statements go here
import time
from html import parser

import requests
import json
import re
import unicodedata
import pandas as pd

# function calls for Pakistan today goes here
CLEANR = re.compile('<.*?>')


def cleanhtml(raw_html):
    cleantext = re.sub(CLEANR, '', raw_html)
    return cleantext


def import_json_from_url(type_of_selection, page_no):
    url = "https://www.dailytimes.com.pk/wp-json/wp/v2/"
    data = {}
    if type_of_selection == 1:
        url = url + f"categories?order=asc&page={page_no}"
    else:
        url = url + f"posts?order=asc&page={page_no}"
    try:
        req = requests.get(url, headers={
            "User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 12871.102.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.141 Safari/537.36"},
                           timeout=10)
    except:
        print("Exception occurred")
        time.sleep(10)
        req = requests.get(url, headers={
            "User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 12871.102.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.141 Safari/537.36"})
    data = json.loads(req.text)  # a `bytes` object
    return data


# entrypoint of the program
if __name__ == '__main__':
    categories_name = {}

    for i in range(1, 8):
        categories_json = import_json_from_url(1, i)
        for j in range(0, len(categories_json)):
            categories_name[categories_json[j]["id"]] = categories_json[j]["name"]

    for x in range(5, 11):
        all_posts = []
        end = 23640 + (1500 * x)
        start = 23640 + (1500 * (x - 1))
        print(f"===========Start Phase {x}===========")
        for i in range(start, end):
            print(f"Getting Page {i} Of {end}")
            posts_json = {}
            posts_json = import_json_from_url(2, i)
            for j in range(0, len(posts_json)):

                posts = {
                    "headline": unicodedata.normalize("NFKD",
                                                      cleanhtml(
                                                          parser.unescape(posts_json[j]["title"]["rendered"]))).replace(
                        '\n', ' ').replace('\r', '').replace('&#8217;', "'"),
                    "date": posts_json[j]["date"],
                    "link": posts_json[j]["link"],
                    "source": "Daily Times",
                    "categories": ""
                }
                for k in range(0, len(posts_json[j]["categories"])):
                    if 0 < k < len(posts_json[j]["categories"]):
                        posts["categories"] += " & "
                    category_id = posts_json[j]['categories'][k]
                    posts["categories"] += categories_name[category_id]
                html_decoded_string = parser.unescape(posts_json[j]["content"]["rendered"])
                posts["description"] = unicodedata.normalize("NFKD",
                                                             cleanhtml(html_decoded_string)).replace('\n', ' ').replace(
                    '\r', '').replace('&#8217;', "'")
                all_posts.append(posts)
        print(f"===========End Phase {x}===========")
        df = pd.read_json(json.dumps(all_posts))
        df.to_csv(f'daily_times_phase_{x}.csv', index=True)
