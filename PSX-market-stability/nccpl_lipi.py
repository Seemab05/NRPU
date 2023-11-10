import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
import time as t
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# access nccpl for lipi broker and lipi_all net values
browser = uc.Chrome(use_subprocess=True)
url = 'https://www.nccpl.com.pk/en/portfolio-investments/lipi-normal-daily'
start_date = datetime(2023, 1, 1)

end_date = datetime(2023, 5, 12)
pd.options.mode.chained_assignment = None


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days + 1)):
        yield start_date + timedelta(n)


browser.get(url)
df = pd.DataFrame()
df1 = pd.DataFrame()
list_a = []
list_a1 = []
sub_set = pd.DataFrame()
sub_set1 = pd.DataFrame()
df2 = pd.DataFrame()
#dfs = pd.DataFrame()
date_list_filtered = []
date_list_filtered1 = []
x = 0
y = 0

# daily lipi net value data
for single_date in daterange(start_date, end_date):
    print(single_date.strftime("%d/%m/%Y"))
    picker = wait(browser, 40).until(EC.presence_of_element_located((By.ID, 'popupDatepicker')))
    t.sleep(2)
    browser.execute_script('arguments[0].scrollIntoView();', picker)
    picker.click()
    t.sleep(3)
    browser.execute_script(f'arguments[0].value = "{single_date.strftime("%d/%m/%Y")}";', picker)
    print('clicked the day!')
    t.sleep(5)
    picker1 = wait(browser, 40).until(EC.presence_of_element_located((By.ID, 'popupDatepicker1')))
    t.sleep(2)
    browser.execute_script('arguments[0].scrollIntoView();', picker1)
    picker1.click()
    t.sleep(4)
    browser.execute_script(f'arguments[0].value = "{single_date.strftime("%d/%m/%Y")}";', picker1)
    print('clicked the second day!')
    t.sleep(1)

    search_button = browser.find_element(By.CLASS_NAME, 'search_btn')
    t.sleep(2)
    search_button.click()
    browser.refresh()
    t.sleep(5)
    print('clicked search!')
    #t.sleep(10)

# load lipi_broker and lipi_all net value data
# list_of_values = ['INDIVIDUALS', 'BROKER PROPRIETARY TRADING', 'OTHER ORGANIZATION', 'NBFC', 'MUTUAL FUNDS', 'INSURANCE COMPANIES', 'COMPANIES', 'BANKS / DFI']

    dfs = pd.read_html(browser.page_source, flavor='html5lib')
    df2 = pd.DataFrame.from_records(dfs[0])
    sub_set = df2.loc[(df2['CLIENT TYPE'] == 'INDIVIDUALS')]
    sub_set2 = df2.loc[(df2['CLIENT TYPE'] == 'BROKER PROPRIETARY TRADING')]
    frames = [sub_set, sub_set2]
    df = pd.concat(frames)
    df['NET VALUE'] = df['NET VALUE'].astype(str).str.replace('(', '-', regex=True).str.replace(')', '', regex=True).str.replace(',', '', regex=True).astype(np.int64)
    print(df['NET VALUE'])
    x = df['NET VALUE'].sum()
    print(x)

    sub_set1 = df2.loc[(df2['CLIENT TYPE'] == 'OTHER ORGANIZATION')]
    sub_set3 = df2.loc[(df2['CLIENT TYPE'] == 'NBFC')]
    sub_set4 = df2.loc[(df2['CLIENT TYPE'] == 'MUTUAL FUNDS')]
    sub_set5 = df2.loc[(df2['CLIENT TYPE'] == 'INSURANCE COMPANIES')]
    sub_set6 = df2.loc[(df2['CLIENT TYPE'] == 'COMPANIES')]
    sub_set7 = df2.loc[(df2['CLIENT TYPE'] == 'BANKS / DFI')]
    frames1 = [sub_set1, sub_set3, sub_set4, sub_set5, sub_set6, sub_set7]
    df1 = pd.concat(frames1)
    df1['NET VALUE'] = df1['NET VALUE'].astype(str).str.replace('(', '-', regex=True).str.replace(')', '', regex=True).str.replace(',', '', regex=True).astype(np.int64)
    # print(sub_set1)
    y = df1['NET VALUE'].sum()
    print(y)

# lipi_broker list
    list_a += [x]
    date_list_filtered.append(single_date.strftime('%d/%m/%Y'))
#lipi_all list
    list_a1 += [y]
    date_list_filtered1.append(single_date.strftime('%d/%m/%Y'))


df_broker = pd.DataFrame(list(zip(date_list_filtered, list_a)), columns=['Date', 'lipi_broker'])
df_broker.set_index('Date', inplace=True)
print(df_broker)
df_broker.to_csv('nccpl_lipi_df_broker.csv', mode='w')

df_all = pd.DataFrame(list(zip(date_list_filtered1, list_a1)), columns=['Date', 'lipi_all'])
df_all.set_index('Date', inplace=True)
print(df_all)
df_all.to_csv('nccpl_lipi_df_all.csv', mode='w')
# # read old psx file
# df_psx = pd.read_csv('KSE_5yr_comb.csv')
# df_psx.set_index('Date', inplace=True)
# print(df_psx)

# # combining old psx data with lipi_broker new data
# for i in df_broker:
#     df_append = pd.merge(df_psx, df_broker, how='left', on='Date')
#     dup = 'lipi_broker'
#     if dup+"_x" in df_append.columns:
#         x = dup+"_x"
#         y = dup+"_y"
#         df_append["lipi_broker"] = df_append[y].fillna(df_append[x])
#         df_append.drop([x, y], 1, inplace=True)
# #print(df_append)
# #df_append.set_index('Date', inplace=True)

# # concatenating lipi_all new data
# for i in df_all:
#     df_append1 = pd.merge(df_append, df_all, how='left', on='Date')
#     dup = 'lipi_all'
#     if dup+"_x" in df_append1.columns:
#         x = dup+"_x"
#         y = dup+"_y"
#         df_append1["lipi_all"] = df_append1[y].fillna(df_append1[x])
#         df_append1.drop([x, y], 1, inplace=True)
# print(df_append1)
# # writing file
# df_append1.to_csv('KSE_5yr_comb.csv')

# #print(df_append1[df_append1['Date'] == '2022-07-01'])




