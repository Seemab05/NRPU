# all import statements go here
import time
from html import parser
from bs4 import BeautifulSoup

import requests
import re
import unicodedata
import csv

# function calls for Pakistan today goes here
CLEANR = re.compile('<.*?>')


def cleanhtml(raw_html):
    cleantext = re.sub(CLEANR, '', raw_html)
    return cleantext


req_headers = {
    "User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 12871.102.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.141 Safari/537.36"}
month_date_matrix = {
    "2020": [
        {
            "start": 1,
            "end": 31
        },
        {
            "start": 1,
            "end": 29
        },
        {
            "start": 1,
            "end": 31
        },
        {
            "start": 1,
            "end": 30
        },
        {
            "start": 1,
            "end": 31
        },
        {
            "start": 1,
            "end": 30
        },
        {
            "start": 1,
            "end": 31
        },
        {
            "start": 1,
            "end": 31
        },
        {
            "start": 1,
            "end": 30
        },
        {
            "start": 1,
            "end": 31
        },
        {
            "start": 1,
            "end": 30
        },
        {
            "start": 1,
            "end": 31
        }
    ],
        "2021": [
        {
            "start": 1,
            "end": 31
        },
        {
            "start": 1,
            "end": 29
        },
        {
            "start": 1,
            "end": 31
        },
        {
            "start": 1,
            "end": 30
        },
        {
            "start": 1,
            "end": 31
        },
        {
            "start": 1,
            "end": 30
        },
        {
            "start": 1,
            "end": 31
        },
        {
            "start": 1,
            "end": 31
        },
        {
            "start": 1,
            "end": 30
        },
        {
            "start": 1,
            "end": 31
        },
        {
            "start": 1,
            "end": 30
        },
        {
            "start": 1,
            "end": 31
        }
    ],
        "2022": [
        {
            "start": 1,
            "end": 31
        },
        {
            "start": 1,
            "end": 29
        },
        {
            "start": 1,
            "end": 31
        },
        {
            "start": 1,
            "end": 30
        },
        {
            "start": 1,
            "end": 31
        },
        {
            "start": 1,
            "end": 30
        },
        {
            "start": 1,
            "end": 31
        },
        {
            "start": 1,
            "end": 31
        },
        {
            "start": 1,
            "end": 30
        },
        {
            "start": 1,
            "end": 31
        },
        {
            "start": 1,
            "end": 30
        },
        {
            "start": 1,
            "end": 31
        }
    ],
            "2023": [
        {
            "start": 1,
            "end": 31
        },
        {
            "start": 1,
            "end": 29
        },
        {
            "start": 1,
            "end": 31
        }
    ],        
    
}

with open('dawn_data.csv', 'a+', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['headline', 'date', 'link',
                  'source', 'categories', 'description']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()

    for i in month_date_matrix:

        count = 1
        print(f"=============Printing for {i}=============")
        for j in month_date_matrix[i]:
            if i == "2020" and count <= 5:
                count = count+1
                continue
            start = j["start"]
            end = j["end"]
            month_prefix = "0" if count < 10 else ""
            for k in range(start, end+1):
                article_counter_for_current_month = 1
                date_prefix = "0" if k < 10 else ""
                end_range = True
                page = 1
                current_date = f'{i}-{month_prefix}{count}-{date_prefix}{k}'
                print(
                    f'>>>>>>>>>>>>>>Started getting data for {current_date}<<<<<<<<<<<<<<<<<<<')
                base_url = f'https://dawn.com/archive/latest-news/{current_date}'
                req = requests.get(base_url, headers=req_headers)
                time.sleep(6)
                page_content = BeautifulSoup(req.content, "html.parser")
                article_headlines_content = page_content.select(
                    'article.story.box.border-b.border-gray-200.pb-2.mb-4')
                total_articles_current_page = len(
                    article_headlines_content)
                print(
                    f'Total {total_articles_current_page} articles found on page {page}')
                for div in article_headlines_content:
                    print(
                        f"Getting Information for Article {article_counter_for_current_month}")
                    try:
                        news = {}
                        news["link"] = div.find(
                            'a', {"class": "story__link"}).get("href")
                        news["categories"] = div.find(
                            'span', {"class": "badge"}).text.replace("\n", "").replace("\r", "")
                        news["date"] = current_date
                        news["headline"] = div.find(
                            'a', {"class": "story__link"}).text.replace("\n", "").replace("\r", "")
                        news["source"] = "Dawn"

                        article_req = requests.get(
                            news["link"], headers=req_headers)
                        time.sleep(6)
                        article_page_content = BeautifulSoup(
                            article_req.content, "html.parser")
                        news["description"] = article_page_content.find(
                            "div", {"class": "story__content"}).text.replace("\n", "").replace("\r", "")
                        news["description"] = parser.unescape(
                            news["description"])
                        news["description"] = unicodedata.normalize("NFKD",
                                                                    cleanhtml(news["description"])).replace('\n', ' ').replace(
                            '\r', '').replace('&#8217;', "'")
                        writer.writerow(news)
                    except:
                        print("Ignored")
                    article_counter_for_current_month += 1

                print(
                    f'>>>>>>>>>>>>>>Ended getting data for {current_date}<<<<<<<<<<<<<<<<<<<')
                print("\n\n\n")
            count = count + 1
