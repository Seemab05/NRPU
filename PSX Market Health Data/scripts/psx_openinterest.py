import requests
import undetected_chromedriver as uc
import time as t
import datetime
from urllib.parse import urlparse

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
    return date.strftime('%Y-%m-%d')

# Date range inputs
start_date = datetime.datetime(2022, 11, 6)
end_date = datetime.datetime(2023, 5, 12)

browser = uc.Chrome(use_chromium=True)
url = 'https://dps.psx.com.pk/downloads'  # Replace with the actual website URL
browser.get(url)

# Wait for the page to load
wait(browser, 30).until(EC.presence_of_element_located((By.ID, 'downloadsDatePicker')))

# Iterate through the date range
current_date = start_date
while current_date <= end_date:
    # Format the current date
    formatted_date = format_date(current_date)

    # Find the search button and handle StaleElementReferenceException
    stale_element = True
    while stale_element:
        try:
            search_button = browser.find_element(By.ID, 'downloadsSearchBtn')
            stale_element = False
        except StaleElementReferenceException:
            stale_element = True

    # Find the date input field and handle StaleElementReferenceException
    stale_element = True
    while stale_element:
        try:
            date_input = wait(browser, 10).until(EC.element_to_be_clickable((By.ID, 'downloadsDatePicker')))
            stale_element = False
        except StaleElementReferenceException:
            stale_element = True

    # Clear the date input field using JavaScript
    browser.execute_script("arguments[0].value = '';", date_input)

    # Enter the current date in the date input field
    date_input.send_keys(formatted_date)

    # Click the search button
    search_button.click()

    # Wait for the page to load
    # Add necessary wait conditions based on the page behavior
    t.sleep(3)  # Example: Wait for 3 seconds (adjust as needed)

    # Find the "downloads__links" element under "Futures Market" heading
    futures_market = wait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//h2[text()="Futures Market"]/following-sibling::ul')))
    download_links = futures_market.find_elements(By.TAG_NAME, 'a')

    # Variables to track the presence of PDF and XLS files
    pdf_found = False
    xls_found = False

    # Iterate through the download links
    for link in download_links:
        # Get the href attribute of the link
        href = link.get_attribute('href')

        # Parse the URL and get the file extension
        parsed_url = urlparse(href)
        file_extension = parsed_url.path.split('.')[-1]

        # Check if it is a PDF or XLS link
        if file_extension == 'pdf' or file_extension == 'xls':
            if file_extension == 'pdf':
                pdf_found = True
            else:
                xls_found = True
        else:
            continue

        # Specify the file path to save the file
        file_path = f'C:/Users/Dell/Desktop/downloads/{formatted_date}.{file_extension}'  # Replace with your desired file path

        # Click on the link to start the download
        link.click()

        # Wait for the file to download
        t.sleep(10)  # Example: Wait for 10 seconds (adjust as needed)

        # Download the file
        download_file(href, file_path)

    # Exception handling
    if not pdf_found:
        print(f"PDF file not found for date: {formatted_date}")
    if not xls_found:
        print(f"xls file not found for date: {formatted_date}")

    # Move to the next date
    current_date += datetime.timedelta(days=1)

# Close the browser
browser.quit()



