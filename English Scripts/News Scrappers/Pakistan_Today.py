# all import statements go here
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
    url = "https://www.pakistantoday.com.pk/wp-json/wp/v2/"
    if type_of_selection == 1:
        url = url + f"categories?order=asc&page={page_no}"
    else:
        url = url + f"posts?order=asc&page={page_no}"
    req = requests.get(url)
    data = json.loads(req.text)  # a `bytes` object
    return data


# entrypoint of the program
if __name__ == '__main__':
    categories_name = {}
    all_posts = []
    for i in range(1, 6):
        categories_json = import_json_from_url(1, i)
        for j in range(0, len(categories_json)):
            categories_name[categories_json[j]["id"]] = categories_json[j]["name"]

    for x in range(1, 5) :
        end = 1032*x
        start = 1032*(x-1)
        if start == 0:
            start = 1
        if end > 4126:
            end = 4125
        for i in range(start, end):
            print("Getting Page " + str(i) + " Of 4126")
            posts_json = import_json_from_url(2, i)
            for j in range(0, len(posts_json)):
                posts = {
                    "headline": unicodedata.normalize("NFKD",
                                                      cleanhtml(
                                                          parser.unescape(posts_json[j]["title"]["rendered"]))).replace(
                        '\n', ' ').replace('\r', '').replace('&#8217;', "'"),
                    "date": posts_json[j]["date"],
                    "link": posts_json[j]["link"],
                    "source": "Pakistan Today",
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
    df = pd.read_json(json.dumps(all_posts))
    df.to_csv('pakistan_today_final.csv', index=True)
    print(len(all_posts))
