import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
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
categories = []
dates = []
urlstart = "https://urdu.dunyanews.tv"
date_today = datetime.datetime.today()
tareekh = date_today.date()
print(date_today)
print(f"Today's Date: {tareekh}")

filename = f'Dunya_{str(tareekh)}.csv'
path = r'H:\My Drive\Datasets\DailyDataDumps\Dunya/'
file_exists = os.path.exists(path+filename)
def url_extraction():
    everything = driver.find_element(By.CLASS_NAME, "col-md-8")
    innerHTML = everything.get_attribute('innerHTML')
    soup = BeautifulSoup(innerHTML, 'html.parser')
    if everything:
        print("YASS")
        # print(innerHTML)
    category_name = soup.find(class_="categoryhead").get_text()  # Save category name
    if '&nbsp;' in category_name:
        category_name = category_name.replace('&nbsp;', '')
    print(f"{category_name}")
    current_time = time.time() - start_time
    print(f'Current Time: {current_time / 3600:.2f} hr, {current_time / 60:.2f} min, {current_time:.2f} sec',
          flush=True)
    print('---------------------------------------------------------')
    # ----- GET TOP ARTICLE -----
    top_article = soup.find(class_="col-md-12 newsttl")
    top_url = top_article.find('a')['href']
    top_url = urlstart + top_url
    print(f"top_url: {top_url}")
    top_headline = top_article.find('a').get_text()
    print(f"top_headline: {top_headline}")
    top_date_element = soup.find(class_= "newsdtls col-md-4")
    top_date_element = top_date_element.find(class_="newsdate")
    top_date = top_date_element.get_text()
    # top_date = everything.find_element(By.CLASS_NAME, "newsdate").text
    print(f"top_date: {top_date}")
    Url.append(top_url)
    titles.append(top_headline)
    categories.append(category_name)
    dates.append(top_date)
    print(f'{len(Url)} urls extracted')
    print(f'{len(titles)} titles extracted')
    print(f'{len(categories)} categories extracted')
    print(f'{len(dates)} dates extracted')
    # ----- GET 4 BIG ARTICLES -----
    news_articles4 = soup.find_all(class_="col-md-6 col-sm-6 col-xs-6")
    # print(f"news_articles4: {news_articles4}")  # Get article link data
    for ind, element in enumerate(news_articles4):
        print(f'index: {ind+1}')
        link_element = element.find('h3').find('a')
        link = link_element['href']
        link = urlstart+link
        print(link)
        title = link_element.get_text()
        print(title)
        date_element = element.find(class_="newsdate")
        date = date_element.get_text()
        print(date)
        Url.append(link)
        titles.append(title)
        dates.append(date)
        categories.append(category_name)
        current_time = time.time() - start_time
        print(f'{len(Url)} urls extracted')
        print(f'{len(titles)} titles extracted')
        print(f'{len(categories)} categories extracted')
        print(f'{len(dates)} dates extracted')
        print(f'Current Time: {current_time / 3600:.2f} hr, {current_time / 60:.2f} min, {current_time:.2f} sec',
              flush=True)
    # ----- REST OF THE ARTICLES -----
    news_articles = soup.find_all(class_="cNewsBox")  # Get article link data
    # print(news_articles)
    for ind, element in enumerate(news_articles):
        print(f'index: {ind + 1}')
        element = element.find(class_="col-md-8")
        link_element = element.find('h3').find('a')
        link = link_element['href']
        link = urlstart+link
        print(link)
        title = link_element.get_text()
        print(title)
        date_element = element.find(class_="newsdate")
        date = date_element.get_text()
        print(date)
        Url.append(link)
        titles.append(title)
        dates.append(date)
        categories.append(category_name)
        current_time = time.time() - start_time
        print(f'{len(Url)} urls extracted')
        print(f'{len(titles)} titles extracted')
        print(f'{len(categories)} categories extracted')
        print(f'{len(dates)} dates extracted')
        print(f'Current Time: {current_time / 3600:.2f} hr, {current_time / 60:.2f} min, {current_time:.2f} sec',
              flush=True)




url_cats = ['https://urdu.dunyanews.tv/index.php/ur/Pakistan', 'https://urdu.dunyanews.tv/index.php/ur/World',
            'https://urdu.dunyanews.tv/index.php/ur/Sports', 'https://urdu.dunyanews.tv/index.php/ur/Business',
            'https://urdu.dunyanews.tv/index.php/ur/Entertainment', 'https://urdu.dunyanews.tv/index.php/ur/Crime',
            'https://urdu.dunyanews.tv/index.php/ur/Cricket']

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
cols = ['Headline', 'Date', 'Url', 'Category', 'Source', 'News']
data = pd.DataFrame(columns=cols, index=range(len(Url)))
for index in range(len(Url)):
    data.loc[index].Headline = titles[index]
    data.loc[index].Url = Url[index]
    data.loc[index].Date = dates[index]
    data.loc[index].Category = categories[index]
    data.loc[index].Source = "Dunya"
    data.loc[index].News = " "

''' DUPLICATE REMOVAL '''
print(f'{data.shape} items in the file.')
print(f"Total duplicates {data.duplicated(subset='Url', keep='first').sum()}")  # Answer:

# Drop all duplicate pairs in DataFrame
data2 = data.copy()
# data2 = data2.groupby("Url").agg({"Category": list}).reset_index()
data2 = data2.drop_duplicates()
# # data = data.drop(['Unnamed: 0'], axis=1)
print(f'Previously {data.shape}')   # Answer: (5714, 3)
print(f'Now {data2.shape}')  # Answer: (4663,2)
if 'Unnamed: 0' in data2.columns:
    del data2['Unnamed: 0']
# resetting the DataFrame index
data2 = data2.reset_index(drop=True)
# data2.to_csv(path + filename, index=False)
print('file saved')

# ----- GET NEWS -----
News = []
url_list = list(data2['Url'])
# start_time = time.time()
for index, url in enumerate(url_list):
    print(f'Url Index: {index}', flush=True)
    print(f'URL: {url}', flush=True)    # Error at url 107 or 108
    # WebDriverWait(driver, 20).until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, "iframeCssSelector")))
    try:
        driver.get(url)
        driver.implicitly_wait(30)
        wait = WebDriverWait(driver, 40)
        ne = driver.find_element(By.CLASS_NAME, "col-md-8")
        innerHTML = ne.get_attribute('innerHTML')
        soup = BeautifulSoup(innerHTML, 'html.parser')
        news_element = soup.find(class_="main-news col-md-12")
        paras = news_element.find_all('p')
        text = []
        for element in paras:
            text.append(element.get_text())
        text2 = ' '.join(text)
        News.append(text2)
        data2.loc[data2['Url'] == url, 'News'] = text2
    except Exception as e:
        print(f'{e}')
        text2 = 'error'
        data2.loc[data2['Url'] == url, 'News'] = text2
    current_time = time.time() - start_time
    print(f'News: {text2}', flush=True)
    print(f'{len(News)} news extracted', flush=True)
    print(f'Current Time: {current_time / 3600:.2f} hr, {current_time / 60:.2f} min, {current_time:.2f} sec',
          flush=True)
    # data2.to_csv(path + filename)
    print('file saved')
    print('-----------------------------------------------------------------------')
    time.sleep(2)

"""CONVERTING DATES to DATETIME"""
data2.to_csv(path+filename)
data2['DateTime'] = ''
data2['DateTime'] = pd.to_datetime(data2['Date'])
data2['DateTime'] = data2['DateTime'].dt.floor('D')

''' SAVING TO CSV '''
if file_exists:
    print("file already exists")
    data2.to_csv(path+filename, mode='a', header=False, index=False)
else:
    print("file saved")
    data2.to_csv(path+filename, header=True, index=False)

# data2.to_csv(path+filename)      # Add directory path
print(data2)

driver.quit()
