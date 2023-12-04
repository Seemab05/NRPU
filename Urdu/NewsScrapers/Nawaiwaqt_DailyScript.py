import os
from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchWindowException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.remote.webelement import WebElement
import pandas as pd
import time
from csv import writer
import csv
import urllib3
import datetime


options = webdriver.ChromeOptions()
options.binary_location = r"C:\Program Files\Google\Chrome Beta\Application\chrome.exe"
options.headless = True
options.add_argument("--incognito")
# putting time set's in milliseconds, so 60k will be 1 minute.
# This fixes the problem of timeout for slow PC.
options.add_experimental_option('extensionLoadTimeout', 60000)
PATH = r"C:\Niki\Study\MSDS\Thesis\Code & Datasets\Selenium_Scraping\pythonProject1/chromedriver.exe"
driver = webdriver.Chrome(PATH, options=options)

date_today = datetime.datetime.today()
tareekh = date_today.date()
print(date_today)
print(f"Today's Date: {tareekh}")

filename = 'Nawaiwaqt_'+str(tareekh)+'.csv'
path = r'G:\My Drive\Datasets\DailyDataDumps/Nawaiwaqt/'

Url = []
titles = []
categories = []
dates = []

# row = []
# headers = ['Url', 'Headline', 'Category']
# print(headers)


# with open(filename, 'w', newline='') as csvfile:
#     csvwriter = csv.writer(csvfile)
#     csvwriter.writerow(headers)
#     csvfile.close()


# def append_file_as_row(file_name, list_of_elem):
#     # Open file in append mode
#     with open(file_name, 'a+', newline='', encoding='utf-8-sig') as write_obj:
#         # Create a writer object from csv module
#         csv_writer = writer(write_obj)
#         # Add contents of list as last row in the csv file
#         csv_writer.writerow(list_of_elem)


def url_extraction():
    category_name = driver.find_element_by_css_selector('h4[class="heading-aham"]').text  # Save category name
    print(f"{category_name}")
    # while True:
    # i = [1, 2, 3, 4, 5]
    # while True:
    for num in range(24):
        print(f'i = {num+1}')
        try:
            driver.execute_script("arguments[0].scrollIntoView();",
                                  driver.find_element(By.XPATH, '//*[@id="post_show_more"]'))
        # WebDriverWait(driver, 20).until(
        #        EC.element_to_be_clickable((By.XPATH, '/html/body/section/div/div/div[1]/div[4]/button'))).click()
            driver.execute_script("arguments[0].click();", WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/section/div/div/div[1]/div[4]/button"))))

            print("LOAD MORE RESULTS button clicked")
            # news_article = driver.find_elements_by_css_selector('div[class="col-md-6 col-sm-6 col-xs-12"]')
            # date_element = news_article[-1].find_element_by_tag_name('div[class="date"]')
            # date = date_element.get_attribute('innerHTML')
            # print(date)
            # if 'Dec 31, 2017' in date:
            #     print("--------------\nDec 31, 2017 FOUND!\n--------------")
            #     break
            # time.sleep(2)
        except Exception as e:
            print(e)
            print('No more Clicks')
            break
    current_time = time.time() - start_time
    print(f'Current Time: {current_time / 3600:.2f} hr, {current_time / 60:.2f} min, {current_time:.2f} sec',
          flush=True)
    print('---------------------------------------------------------')
    news_articles = driver.find_elements_by_css_selector('div[class="col-md-6 col-sm-6 col-xs-12"]')  # Get article link data
    # # print(f"{news_articles.get_attribute('href')}")
    for ind, element in enumerate(news_articles):
        print(f'index: {ind+1}')
        if ind+1 <= 4:
            link_element = element.find_element_by_tag_name('a[class="urdu_font"]')
            link = link_element.get_attribute('href')
            print(link)
            # title = link_element.get_attribute('innerHTML')
            # print(title)
            date_element = element.find_element_by_tag_name('span[class="time"]')
            date = date_element.get_attribute('innerHTML')
            print(date)
        elif 5 <= ind+1 <= 10:
            date_element = element.find_element_by_tag_name('div[class="date"]')
            date = date_element.get_attribute('innerHTML')
            print(date)
        else:
            date_element = element.find_element_by_tag_name('div[class="date"]')
            date = date_element.get_attribute('innerHTML')
            print(date)
        # if 'Dec 31, 2017' in date:
        #     print("--------------\nDec 31, 2017 FOUND!\n--------------")
        #     break
        Url.append(link)
        # titles.append(title)
        dates.append(date)
        categories.append(category_name)
    #     row = [link, title, category_name]
    #     # append_file_as_row(filename, row)
        current_time = time.time() - start_time
        print(f'{len(Url)} urls extracted')
        # print(f'{len(titles)} titles extracted')
        print(f'{len(categories)} categories extracted')
        print(f'{len(dates)} dates extracted')
        print(f'Current Time: {current_time / 3600:.2f} hr, {current_time / 60:.2f} min, {current_time:.2f} sec',
              flush=True)


url_cats = ['https://www.nawaiwaqt.com.pk/national', 'https://www.nawaiwaqt.com.pk/international',
            'https://www.nawaiwaqt.com.pk/business', 'https://www.nawaiwaqt.com.pk/miscellaneous',
            'https://www.nawaiwaqt.com.pk/sports', 'https://www.nawaiwaqt.com.pk/crime-court',
            'https://www.nawaiwaqt.com.pk/entertainment']

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
    data.loc[index].Headline = ""
    data.loc[index].Url = Url[index]
    data.loc[index].Date = dates[index]
    data.loc[index].Category = categories[index]
    data.loc[index].Source = "Nawaiwaqt"
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
print('file saved')

''' GET NEWS '''
News = []
url_list = list(data2['Url'])
for index, url in enumerate(url_list):
    print(f'Url Index: {index}', flush=True)
    print(f'URL: {url}', flush=True)    # Error at url 107 or 108
    # WebDriverWait(driver, 20).until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, "iframeCssSelector")))
    try:
        driver.get(url)
        driver.implicitly_wait(60)
        headline_element = driver.find_element_by_css_selector('div[class="head-post"]')
        headline = headline_element.find_element_by_tag_name('h2').text
        news_element = driver.find_element_by_css_selector('div[class="entry-post mrgn-top"]')
        paras = news_element.find_elements_by_tag_name('p')
        text = []
        for element in paras:
            text.append(element.text)
        text2 = ' '.join(text)
        News.append(text2)
        titles.append(headline)
        data2.loc[data2['Url'] == url, 'News'] = text2
        current_time = time.time() - start_time
    except Exception as e:
        print(f'{e}')
        text2 = 'error'
        data2.loc[data2['Url'] == url, 'News'] = text2
        data2.loc[data2['Url'] == url, 'Headline'] = headline
    current_time = time.time() - start_time
    print(f'Headline: {headline}', flush=True)
    print(f'News: {text2}', flush=True)
    print(f'{len(News)} news extracted', flush=True)
    print(f'Current Time: {current_time / 3600:.2f} hr, {current_time / 60:.2f} min, {current_time:.2f} sec',
          flush=True)
    if index % 5 == 0:
        data2.to_csv(path + filename)
        print('file saved')
    print('-----------------------------------------------------------------------')
    time.sleep(1)

"""CONVERTING DATES to DATETIME"""
data2.to_csv(path+filename)
data2['DateTime'] = ''
for index, val in enumerate(data2['Date']):
    data2['DateTime'][index] = val.split('|')[0].strip()

data2['DateTime'] = pd.to_datetime(data2['DateTime'], format='%b %d, %Y')

''' SAVING TO CSV '''
data2.to_csv(path+filename)      # Add directory path
print(data2)

driver.quit()
