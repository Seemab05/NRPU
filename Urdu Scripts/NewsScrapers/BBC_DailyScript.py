import os
from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.remote.webelement import WebElement
import pandas as pd
import time
import datetime
from csv import writer
import csv
import urllib3


options = webdriver.ChromeOptions()
options.binary_location = r"C:\Program Files\Google\Chrome Beta\Application\chrome.exe"
options.headless = True
options.add_argument("--incognito")
# putting time set's in milliseconds, so 60k will be 1 minute.
# This fixes the problem of timeout for slow PC.
options.add_experimental_option('extensionLoadTimeout', 60000)
PATH = r"C:\Niki\Study\MSDS\Thesis\Code & Datasets\Selenium_Scraping\pythonProject1/chromedriver.exe"
driver = webdriver.Chrome(PATH, options=options)

Category = []
Headline = []
Date = []
Url = []
News = []

date_today = datetime.datetime.today()
tareekh = date_today.date()
print(date_today)
print(f"Today's Date: {tareekh}")

filename = 'BBC_'+str(tareekh)+'.csv'
path = r'G:\My Drive\Datasets\DailyDataDumps/BBC/'


def Url_Extraction():
    category_name = driver.find_element_by_id("content")
    cat = category_name.text  # Save category name in variable
    print(f"{cat}")
    news_articles = driver.find_elements_by_css_selector('li[class="bbc-t44f9r"]')  # Get article link data
    if news_articles == []:
        print('------Articles NOT FOUND!------')
    # print(f"{news_articles.get_attribute('href')}")
    for element in news_articles:
        try:
            URL = element.find_element_by_tag_name('a').get_attribute('href')
        except Exception as e:
            print(e)
            URL = 'error'
        try:
            headline = element.find_element_by_tag_name('a').get_attribute('innerHTML')
        except Exception as e:
            print(e)
            headline = 'error'
        try:
            date = element.find_element_by_tag_name('time').get_attribute('datetime')
        except Exception as e:
            print(e)
            date = 'error'
        Url.append(URL)
        Headline.append(headline)
        Date.append(date)
        Category.append(cat)
        current_time = time.time() - start_time
        print(f'{len(Url)} urls extracted')
        print(f'{len(Headline)} headlines extracted')
        print(f'{len(Date)} dates extracted')
        print(f'{len(Category)} categories extracted')
        print(f'Current Time: {current_time / 3600:.2f} hr, {current_time / 60:.2f} min, {current_time:.2f} sec',
              flush=True)
    # try:
    #     next_page = driver.find_element_by_id('pagination-next-page')
    #     driver.execute_script("arguments[0].click();", next_page)
    # except Exception as e:
    #     print(e)
    # next_page.click()

category_urls = ['https://www.bbc.com/urdu/topics/cjgn7n9zzq7t?page=', 'https://www.bbc.com/urdu/topics/cl8l9mveql2t?page=',
                 'https://www.bbc.com/urdu/topics/cw57v2pmll9t?page=', 'https://www.bbc.com/urdu/topics/c340q0p2585t?page=',
                 'https://www.bbc.com/urdu/topics/ckdxnx900n5t?page=', 'https://www.bbc.com/urdu/topics/c40379e2ymxt?page=']
start_time = time.time()
for num, url in enumerate(category_urls):
    for page in range(2):
        print(f'PAGE = {page+1}')
        driver.get(url+str(page+1))   # Go to Webpage
        driver.implicitly_wait(30)  # we don't need to wait 30 secs if element is already there (very useful)
        print(f'------URL {num+1}------')
        Url_Extraction()

''' Adding Data to a Dataframe'''
cols = ['Headline', 'Date', 'Url', 'Category', 'Source', 'News']
data = pd.DataFrame(columns=cols, index=range(len(Url)))
for index in range(len(Url)):
    data.loc[index].Headline = Headline[index]
    data.loc[index].Url = Url[index]
    data.loc[index].Date = Date[index]
    data.loc[index].Category = Category[index]
    data.loc[index].Source = "BBC"
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
data2 = data2.reset_index()
data2.to_csv(path + filename)
# print('file saved')

''' GET NEWS '''
url_list = list(data2['Url'])
for index, url in enumerate(url_list):
    print(f'URL: {url}', flush=True)    # Error at url 107 or 108
    # WebDriverWait(driver, 20).until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, "iframeCssSelector")))
    try:
        driver.get(url)
        driver.implicitly_wait(60)
        try:
            news_elements = driver.find_elements_by_css_selector('p[class="bbc-yabuuk e17g058b0"]')
        except Exception as e:
            print(e)
            news_elements = driver.find_elements_by_css_selector('p[class="bbc-1sy09mr e1cc2ql70"]')
        text = []
        for element in news_elements:
            text.append(element.text)
        text2 = ' '.join(text)
        News.append(text2)
        current_time = time.time() - start_time
        ''' Adding Data to a Dataframe'''
        data2['News'][index] = text2
    except Exception as e:
        print(f'{e}')
        data2['News'][index] = 'error'

    print(f'News: {text2}', flush=True)
    print(f'{len(News)} news extracted', flush=True)
    print(f'Current Time: {current_time / 3600:.2f} hr, {current_time / 60:.2f} min, {current_time:.2f} sec',
          flush=True)
    print('-----------------------------------------------------------------------')
    time.sleep(5)

"""CONVERTING DATES to DATETIME"""
data2.to_csv(path+filename)
data2['DateTime'] = pd.to_datetime(data2['Date'])

''' SAVING TO CSV '''
data2.to_csv(path+filename)      # Add directory path
print(data2)
print("---------------------")
print("--------------")
print("-----------FILE SAVED----------")
print("--------------")
print("---------------------")
driver.quit()
