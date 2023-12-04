import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.remote.webelement import WebElement
from bs4 import BeautifulSoup
import pandas as pd
import time
import datetime
from csv import writer
import csv
import urllib3


options = webdriver.ChromeOptions()
options.binary_location = r"C:\Program Files\Google\Chrome Beta\Application\chrome.exe"
options.add_argument('--headless')
options.add_argument("--incognito")
# putting time set's in milliseconds, so 60k will be 1 minute.
# This fixes the problem of timeout for slow PC.
options.add_experimental_option('extensionLoadTimeout', 60000)
PATH = r"C:\Niki\Study\MSDS\Thesis\Code & Datasets\Selenium_Scraping\pythonProject1\chromedriver-win64/chromedriver.exe"
driver = webdriver.Chrome(PATH, options=options)
# driver = webdriver.Chrome(options=options)
# driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

Url = []
titles = []
dates = []
headlines = []
News = []
date_today = datetime.datetime.today()
day_today = date_today.day
tareekh = date_today.date()
print(tareekh)
print(date_today)
print(day_today)

filename = 'Jang_'+str(tareekh)+'.csv'
path = r'H:\My Drive\Datasets\DailyDataDumps\Jang/'
# date = '12 دسمبر ، 2022'


def url_extraction():
    # category_name = driver.find_element_by_css_selector('h4[class="heading-aham"]').text  # Save category name
    # print(f"{category_name}")
    SCROLL_PAUSE_TIME = 3
    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)
        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    current_time = time.time() - start_time
    print(f'Current Time: {current_time / 3600:.2f} hr, {current_time / 60:.2f} min, {current_time:.2f} sec',
          flush=True)
    print('---------------------------------------------------------')
    news_articles = driver.find_element(By.CLASS_NAME, "scrollPaginationNew")
    link_elements = news_articles.find_elements(By.CLASS_NAME, "main-heading")
    for ind, element in enumerate(link_elements):
        print(f'index: {ind+1}')
        link = element.find_element(By.TAG_NAME, 'a').get_attribute('href')
        print(link)
        title = element.find_element(By.TAG_NAME, 'h2').get_attribute('innerHTML')
        print(title)
        date = element.find_element(By.CLASS_NAME, "cat-time").get_attribute('innerHTML')
        print(date)
        date2 = date[:2]
        print('Article Date:', date2)

        # if str(day_today) != date2:
        #     print(f"Today's Date {date_today} NOT EQUAL to Articles's Date {date}")
        #     break

        Url.append(link)
        titles.append(title)
        dates.append(date)
        current_time = time.time() - start_time
        print(f'{len(Url)} urls extracted')
        print(f'{len(titles)} titles extracted')
        print(f'{len(dates)} dates extracted')
        print('----------')
        print(f'Current Time: {current_time / 3600:.2f} hr, {current_time / 60:.2f} min, {current_time:.2f} sec',
              flush=True)


url_cats = ['https://jang.com.pk/category/latest-news/national', 'https://jang.com.pk/category/latest-news/world',
            'https://jang.com.pk/category/latest-news/sports', 'https://jang.com.pk/category/latest-news/entertainment',
            'https://jang.com.pk/category/latest-news/amazing', 'https://jang.com.pk/category/latest-news/special-reports',
            'https://jang.com.pk/category/latest-news/health-science', 'https://jang.com.pk/category/latest-news/business']

start_time = time.time()
for ind, url in enumerate(url_cats):
    print(f'----------WEB PAGE {ind+1}-------------')
    try:
        driver.get(url)  # Go to Webpage
        driver.implicitly_wait(30)  # we don't need to wait 30 secs if element is already there (very useful)
        url_extraction()
    except Exception as e:
        print(e)


''' Adding Data to a Dataframe'''
cols = ['Headline', 'Date', 'Url', 'Source', 'News', 'Category']
data = pd.DataFrame(columns=cols, index=range(len(Url)))
for index in range(len(Url)):
    data.loc[index].Headline = titles[index]
    data.loc[index].Url = Url[index]
    data.loc[index].Date = dates[index]
    data.loc[index].Category = ""
    data.loc[index].Source = "Jang"
    data.loc[index].News = " "

''' DUPLICATE REMOVAL '''
print(f'{data.shape} items in the file.')
print(f"Total duplicates {data.duplicated(subset='Url', keep='first').sum()}")  # Answer:

# Drop all duplicate pairs in DataFrame
data2 = data.copy()
data2 = data2.drop_duplicates()
# data = data.drop(['Unnamed: 0'], axis=1)
print(f'Previously {data.shape}')   # Answer: (5714, 3)
print(f'Now {data2.shape}')  # Answer: (4663,2)
if 'Unnamed: 0' in data2.columns:
    del data2['Unnamed: 0']
# resetting the DataFrame index
data2 = data2.reset_index(drop=True)
data2.to_csv(path+filename, index=False)
''' NEWS EXTRACTION '''
wait = WebDriverWait(driver, 10)
# Date = []
News = []
Categories = []

# ind = 1061
url_list = list(data2['Url'])
# start_time = time.time()
for index, url in enumerate(url_list):
    print(f'Url Index: {index}', flush=True)
    print(f'URL: {url}', flush=True)    # Error at url 107 or 108
    # WebDriverWait(driver, 20).until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, "iframeCssSelector")))
    driver.get(url)
    driver.implicitly_wait(60)
    try:
        time.sleep(1)
        category_element = driver.find_element(By.CLASS_NAME, "detail-w-t")
        category_element2 = category_element.find_elements(By.CLASS_NAME, "detail-time")  # Save category name
        category_name = category_element2[1].find_element(By.TAG_NAME, 'a').get_attribute('title')
        print(f"{category_name}")
        time.sleep(3)
        news_element = driver.find_element(By.CLASS_NAME, "detail_view_content")
        paras = news_element.find_elements(By.TAG_NAME, 'p')
        text = []
        for element in paras:
            text.append(element.text)
        text2 = ' '.join(text)
        # News.append(text2)
        # Categories.append(category_name)
    except Exception as e:
        print(f'{e}')
        try:
            category_element = driver.find_element(By.CLASS_NAME, "detail-w-t")
            category_element2 = category_element.find_elements(By.CLASS_NAME, "detail-time")
            category_name = category_element2[1].find_element(By.TAG_NAME, 'a').get_attribute('title')   # Save category name
        except Exception as e:
            print(e)
            category_name = 'error'
            print(f'---NOT FOUND---\nCategory: {category_name}')
        try:
            news_element = driver.find_element(By.CLASS_NAME, "detail_view_content")
            paras = news_element.find_elements(By.CLASS_NAME, 'p')
            text = []
            for element in paras:
                text.append(element.text)
            text2 = ' '.join(text)
        except Exception as e:
            print(e)
            text2 = 'error'
            print(f'---NOT FOUND---\nNews:{text2}')
    News.append(text2)
    Categories.append(category_name)

    current_time = time.time() - start_time
    print(f'News: {text2}', flush=True)
    print(f'{len(News)} news extracted', flush=True)
    data2['News'][index] = text2
    data2['Category'][index] = category_name
    # row = [url, data["Date"][index+ind], data["Headline"][index+ind], text2, category_name, data["Source"][index+ind]]
    # append_file_as_row(file_name, row)
    print(f'Current Time: {current_time / 3600:.2f} hr, {current_time / 60:.2f} min, {current_time:.2f} sec',
          flush=True)
    data2.to_csv(path + filename, index=False)
    print('file saved')
    print('-----------------------------------------------------------------------')
    time.sleep(1)

"""CONVERTING DATES to DATETIME"""
data2.to_csv(path+filename)
months_dict = {
    'جنوری': 'January',
    'فروری': 'February',
    'مارچ': 'March',
    'اپریل': 'April',
    'مئی': 'May',
    'جون': 'June',
    'جولائی': 'July',
    'اگست': 'August',
    'ستمبر': 'September',
    'اکتوبر': 'October',
    'نومبر': 'November',
    'دسمبر': 'December'
}
umon = [key for key, value in months_dict.items()]
data2['DateTime'] = ''
for index, val in enumerate(data2['Date']):
    for m in umon:
        if m in val:
            date_string = val.replace(str(m)+' ،', months_dict[m])
            data2['DateTime'][index] = val.replace(str(m)+' ،', months_dict[m])

data2['DateTime'] = pd.to_datetime(data2['DateTime'], format="%d %B %Y")

''' SAVING TO CSV '''
filename = 'Jang_'+str(tareekh)+'.csv'
path = r'G:\My Drive\Datasets\DailyDataDumps/'
data2.to_csv(path+filename)      # Add directory path
print(data2)
# time.sleep(3)
driver.quit()
