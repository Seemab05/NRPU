import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
import time as t
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# access nccpl for foreign investors net values from 2016 onwards
browser = uc.Chrome(use_subprocess=True)
url = 'https://www.nccpl.com.pk/en/portfolio-investments/fipi-sector-wise'

start_date = datetime(2023, 5, 1)
end_date = datetime(2023, 5, 12)

def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days + 1)):
        yield start_date + timedelta(n)


browser.get(url)
list_a = []
joinedlist = []
df = pd.DataFrame()
date_list_filtered = []

# daily foreign net value data
for single_date in daterange(start_date, end_date):
    print(single_date)
    picker = wait(browser, 20).until(EC.presence_of_element_located((By.ID, 'popupDatepicker')))
    t.sleep(2)
    browser.execute_script('arguments[0].scrollIntoView();', picker)
    picker.click()
    t.sleep(3)
    browser.execute_script(f'arguments[0].value = "{single_date.strftime("%d/%m/%Y")}";', picker)
    print('clicked the day!')
    t.sleep(5)

    picker = wait(browser, 20).until(EC.presence_of_element_located((By.ID, 'popupDatepicker1')))
    t.sleep(2)
    browser.execute_script('arguments[0].scrollIntoView();', picker)
    picker.click()
    t.sleep(4)
    browser.execute_script(f'arguments[0].value = "{single_date.strftime("%d/%m/%Y")}";', picker)
    print('clicked the second day!')
    t.sleep(1)

    search_button = browser.find_element(By.XPATH, '//button[@class="search_btn"]/parent::div')
    t.sleep(2)
    search_button.click()
    browser.refresh()
    t.sleep(5)
    print('clicked search!')

# load foreign net value data
    dfs = pd.read_html(browser.page_source)
    x = dfs[0]['NET VALUE'].iloc[-1]
    print(x)
    print(type(x))
    if x == 0:
        list_a += [str(x)]
        date_list_filtered.append(single_date.strftime('%d/%m/%Y'))
    else:
        list_a += [x.replace(',', '')]
        date_list_filtered.append(single_date.strftime('%d/%m/%Y'))

#print(date_list_filtered)
#print(list_a)
#joinedlist = list(zip(date_list_filtered, list_a))
#print(joinedlist)

df_foreign = pd.DataFrame(list(zip(date_list_filtered, list_a)), columns=['Date', 'NET values_all fipi sectors'])
df_foreign.set_index('Date', inplace=True)
print(df_foreign)

df_foreign.to_csv('nccpl_foreign.csv', mode='w')
# # read old psx file
# df_psx = pd.read_csv('KSE_5yr_comb1.csv')
# df_psx.set_index('Date', inplace=True)
# print(df_psx)

# # combining old psx data with lipi_broker new data
# for i in df_foreign:
#     df_append = pd.merge(df_psx, df_foreign, how='left', on='Date')
#     dup = 'NET values_all fipi sectors'
#     if dup+"_x" in df_append.columns:
#         x = dup+"_x"
#         y = dup+"_y"
#         df_append["NET values_all fipi sectors"] = df_append[y].fillna(df_append[x])
#         df_append.drop([x, y], 1, inplace=True)

# #print(df_append)
# #df_append.set_index('Date', inplace=True)

# df_append.to_csv('KSE_5yr_comb1.csv')
# with open('foreign_2022_2.csv','w') as f:
#     for sublist in joinedlist:
#         for item in sublist:
#             f.write(item + ',')
#         f.write('\n')



# a = np.matrix(dfs)
# df = pd.DataFrame.from_records(dfs)

