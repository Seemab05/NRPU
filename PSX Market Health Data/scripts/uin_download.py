import requests
import undetected_chromedriver as uc
import time as t
import datetime
import os
import urllib.parse as urlparse
import pandas as pd
import io

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException

def download_file(url, file_path):
    response = requests.get(url)
    with open(file_path, 'wb') as file:
        file.write(response.content)

# Function to format the date as per your requirement
def format_date(date):
    return date.strftime('%d/%m/%Y')

# Date range inputs
start_date = datetime.datetime(2023, 4, 24)
end_date = datetime.datetime(2023, 5, 12)

browser = uc.Chrome(use_chromium=True)
url = 'https://www.nccpl.com.pk/en/market-information/settlement-un-listed-tfc-report'  # Replace with the actual website URL
browser.get(url)

# Wait for the page to load
wait(browser, 60).until(EC.presence_of_element_located((By.ID, 'popupDatepicker2')))

# Locate and click the desired tab
tab = wait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, '//a[contains(text(), "Sett Info-UIN Wise")]')))
tab.click()

# Wait for the tab content to load
wait(browser, 10).until(EC.presence_of_element_located((By.ID, 'popupDatepicker2')))

# Iterate through the date range
current_date = start_date
while current_date <= end_date:
    # Format the current date
    formatted_date = format_date(current_date)

    # Find the date input field and handle StaleElementReferenceException
    stale_element = True
    while stale_element:
        try:
            # Start date picker
            date_input = wait(browser, 20).until(EC.presence_of_element_located((By.ID, 'popupDatepicker2')))
            browser.execute_script(f'arguments[0].value = "{formatted_date}";', date_input)
            t.sleep(5)
            print('Clicked the day!')

            browser.execute_script("window.scrollTo(0, 250.98)")
            t.sleep(2)
            stale_element = False
        except StaleElementReferenceException:
            stale_element = True

    # Find the search button and handle StaleElementReferenceException
    stale_element = True
    while stale_element:
        try:
            wait(browser, 20).until(EC.element_to_be_clickable((By.XPATH, '/html/body/section[2]/div/div[2]/div[1]/div/div/div/div[2]/div/div[1]/form/div/div[2]/button'))).click()
            t.sleep(5)
            stale_element = False
        except StaleElementReferenceException:
            stale_element = True

    # Find the export button and handle StaleElementReferenceException
    stale_element = True
    while stale_element:
        try:
            export_button = wait(browser, 30).until(EC.presence_of_element_located((By.ID, 'export1')))
            # export_button.click()
            browser.execute_script("arguments[0].scrollIntoView();", export_button)
            stale_element = False
        except StaleElementReferenceException:
            stale_element = True

    # Scroll to the export button to ensure it's visible
    browser.execute_script("arguments[0].scrollIntoView();", export_button)

    wait(browser, 40).until(EC.element_to_be_clickable((By.ID, 'export1'))).click()
    print("EXPORT BUTTON CLICKED!")
    # Wait for the href value of the export button to change
    # wait(browser, 30).until(EC.not_(EC.attribute_contains((By.ID, 'export1'), 'href', 'javascript:;')))
  
    # Get the updated href value from the export button
    href_attr = export_button.get_attribute('href')
    count = 0
    while href_attr == 'javascript:;':
        # Get the updated href value from the export button
        count+=1
        wait(browser, 40).until(EC.element_to_be_clickable((By.ID, 'export1'))).click()
        href_attr = export_button.get_attribute('href')
    print(count)
    # Check if the href attribute is present
    if href_attr:
        # Extract the data from the href attribute
        data_start = "data:application/csv;charset=utf-8,"
        data = urlparse.unquote(href_attr.replace(data_start, ""))

        # Convert the data to a DataFrame
        df = pd.read_csv(io.StringIO(data))

        file_name = current_date.strftime("%Y-%m-%d") + '.csv'
        file_path = os.path.join('C:/Users/Dell/Desktop/downloads_uin', file_name)
        df.to_csv(file_path, index=False)
        print(f'Saved file: {file_path}')
    else:
        print(f'No file available for {current_date.strftime("%Y%m%d")}.csv')

    # Move to the next date
    current_date += datetime.timedelta(days=1)

# Close the browser
browser.quit()
