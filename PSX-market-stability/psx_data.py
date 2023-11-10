import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.support import expected_conditions as EC
import time as t
import pandas as pd
import numpy as np
from datetime import datetime, timedelta


browser = uc.Chrome(use_subprocess=True)
url = 'https://www.investorslounge.com/stock-market/index-history'
pd.options.mode.chained_assignment = None
browser.get(url)

# set date to fetch latest data from psx
start_date = datetime(2012, 1, 1)
if start_date.strftime('%Y_%m_%d') == datetime.now().strftime('%Y_%m_%d'):
    print("Data not available for current date")
    start_date = start_date - timedelta(days=1)

# select KSE index
indices = wait(browser, 40).until(EC.presence_of_element_located((By.ID, 'ddIndices')))
t.sleep(2)
browser.execute_script("return arguments[0].selected=true;", indices)
indices.click()
t.sleep(3)
browser.execute_script(f'arguments[0].value = "2";', indices)
print('selected the indices!')
t.sleep(5)

res = pd.DataFrame()
dfs = pd.DataFrame()
df2 = pd.DataFrame()
start_date = start_date.strftime('%d %b %Y')
#end_date1 = end_date.strftime('%d %b %Y')

# start date picker
picker = wait(browser, 20).until(EC.presence_of_element_located((By.ID, 'dateFrom')))
t.sleep(2)
browser.execute_script(f'arguments[0].value = "{start_date}";', picker)
print('clicked the day!')
print(start_date)
t.sleep(5)

# end date picker
#print(end_date1)
#picker1 = wait(browser, 20).until(EC.presence_of_element_located((By.ID, 'dateTo')))
#t.sleep(2)
#browser.execute_script('arguments[0].click();', picker1)
#browser.execute_script(f'arguments[0].value = {end_date1}";', picker1)
#print('clicked the day!')
##print(end_date1)
#t.sleep(5)

# search data for date range provided
search_button = browser.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div/div[3]/div[1]/div/div/div[4]/button')
t.sleep(2)
search_button.click()
print('clicked search!')
t.sleep(3)

# set page show to all
show = wait(browser, 40).until(EC.presence_of_element_located((By.XPATH, '//*[@id="tblIndexHistory_length"]/label/select/option[5]')))
show.click()
print('show all entries!')
#browser.refresh()
t.sleep(3)

# load and count latest psx_data
dfs = pd.read_html(browser.page_source)
df2 = pd.DataFrame.from_records(dfs[0])
rows_count = df2.count()[0]
print(rows_count)

# sorting data date-wise in ascending form
#print(df2.dtypes)
df2['Date'] = pd.to_datetime(df2['Date'])
df2['Date'] = df2['Date'].dt.strftime('%Y-%m-%d')
df2 = df2.sort_values(by='Date', ascending=True)
df2.set_index('Date', inplace=True)
print(df2.head())

# # load old psx file
# df_psx = pd.read_csv('KSE_5yr_comb.csv')
# df_psx.set_index('Date', inplace=True)
# print(df_psx.head())

# # concatenates fetched data to old file
# res = pd.concat([df_psx, df2], ignore_index=False)
# res = res[~res.index.duplicated(keep='first')]
# print(res)
#df_psx.to_csv('PSX_KSE100 ' + str(datetime.now().strftime('%Y_%m_%d')) + '.csv')
# res.to_csv('KSE_5yr_comb1.csv', mode='w')
df2.to_csv('KSE_5yr_comb1.csv', mode='w')