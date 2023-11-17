import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
import time as t
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# access nccpl for mts
browser = uc.Chrome(use_subprocess=True)
urls = ['https://www.nccpl.com.pk/en/market-information/margin-financing',
        'https://www.nccpl.com.pk/en/market-information/margin-trading-system']

start_date = datetime(2023, 4, 1)
end_date = datetime(2023, 5, 12)
pd.options.mode.chained_assignment = None


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days + 1)):
        yield start_date + timedelta(n)


def net_open_mrgn_financing(url):
    browser.get(url)
    x = 0
    dfs = pd.DataFrame()
    df = pd.DataFrame()
    df_open = pd.DataFrame()
    df_fin = pd.DataFrame()
    date_list_filtered = []
    list_a = []
    for single_date in daterange(start_date, end_date):
        single_date = single_date.strftime('%d/%m/%Y')
        print(single_date)
        picker = wait(browser, 20).until(EC.presence_of_element_located((By.ID, 'popupDatepicker1')))
        browser.execute_script(f'arguments[0].value = "{single_date}";', picker)
        t.sleep(5)
        print('clicked the day!')

        browser.execute_script("window.scrollTo(0, 250.98)")
        t.sleep(2)
        wait(browser, 20).until(EC.element_to_be_clickable((By.XPATH,'/html/body/section[2]/div/div[2]/div[1]/div/div/div/div[1]/div/div[1]/form/div/div[2]/button'))).click()
        t.sleep(5)

        browser.execute_script("window.scrollTo(0, 400.98)")
        tbl = wait(browser, 20).until(EC.element_to_be_clickable((By.XPATH,"/html/body/section[2]/div/div[2]/div[1]/div/div/div/div[1]/div/div[3]/div[1]/table"))).get_attribute(
            'outerHTML')
        df = pd.read_html(tbl)
        t.sleep(5)
        dfs = pd.DataFrame.from_records(df[0])

        if dfs.shape[0] == 0:
            x = 0
            list_a += [x]
            date_list_filtered.append(single_date)

        else:
            print(dfs)
            dfs = dfs[~dfs['Symbol', 'Unnamed: 0_level_1'].isna()]
            df_open['open'] = dfs['Net Open Position', 'Value']
            df_open['open'] = df_open['open'].apply(lambda x1: "0" if x1 == "-" else x1)
            df_open['open'] = pd.to_numeric(df_open['open'])
            print(df_open.dtypes)
            # print(df_open['open'].iloc[267])
            x = df_open['open'].sum()
            print(df_open)
            print(x)
            list_a += [x]
            date_list_filtered.append(single_date)

    df_fin = pd.DataFrame(list(zip(date_list_filtered, list_a)), columns=['Date', 'df_fin'])
    df_fin.set_index('Date', inplace=True)
    print(df_fin)
    return df_fin


def mts_amount_mrgn_trading(url):
    browser.get(url)
    y = 0
    df_open1 = pd.DataFrame()
    df_mts = pd.DataFrame()
    dfs1 = pd.DataFrame()
    df1 = pd.DataFrame()
    date_list_filtered1 = []
    list_a1 = []
    for single_date in daterange(start_date, end_date):
        single_date = single_date.strftime('%d/%m/%Y')
        print(single_date)
        picker = wait(browser, 40).until(EC.presence_of_element_located((By.ID, 'popupDatepicker1')))
        browser.execute_script(f'arguments[0].value = "{single_date}";', picker)
        t.sleep(5)
        print('clicked the day!')

        browser.execute_script("window.scrollTo(0, 250.98)")
        t.sleep(2)
        wait(browser, 20).until(EC.element_to_be_clickable((By.XPATH,'/html/body/section[2]/div/div[2]/div[1]/div/div/div/div[1]/div/div[1]/form/div/div[2]/button'))).click()
        t.sleep(5)

        browser.execute_script("window.scrollTo(0, 400.98)")
        tbl = wait(browser, 20).until(EC.element_to_be_clickable((By.XPATH, '/html/body/section[2]/div/div[2]/div[1]/div/div/div/div[1]/div/div[3]/div/table'))).get_attribute(
            'outerHTML')
        df1 = pd.read_html(tbl)
        t.sleep(5)
        dfs1 = pd.DataFrame.from_records(df1[0])

        if dfs1.shape[0] == 0:
            y = 0
            list_a1 += [y]
            date_list_filtered1.append(single_date)

        else:
            print(dfs1)
            dfs1 = dfs1[~dfs1['Symbol Code'].isna()]
            df_open1['open1'] = dfs1['Net Open MTS Amount']
            df_open1['open1'] = df_open1['open1'].apply(lambda x2: "0" if x2 == "-" else x2)
            df_open1['open1'] = pd.to_numeric(df_open1['open1'])
            y = df_open1['open1'].sum()
            print(df_open1)
            print(y)
            list_a1 += [y]
            date_list_filtered1.append(single_date)

    df_mts = pd.DataFrame(list(zip(date_list_filtered1, list_a1)), columns=['Date', 'df_mts'])
    df_mts.set_index('Date', inplace=True)
    print(df_mts)
    return df_mts


df_fin1 = pd.DataFrame()
df_mts1 = pd.DataFrame()

for index, url in enumerate(urls):
    if index == 0:
        df_fin1 = net_open_mrgn_financing(url)
    elif index == 1:
        df_mts1 = mts_amount_mrgn_trading(url)

for i in df_mts1:
    df_append = pd.merge(df_fin1, df_mts1, how='left', on='Date')
    dup = 'df_mts'
    if dup+"_x" in df_append.columns:
        x = dup+"_x"
        y = dup+"_y"
        df_append["df_mts"] = df_append[y].fillna(df_append[x])
        df_append.drop([x, y], 1, inplace=True)
# print(df_append)

df_append["sum_mts"] = df_append["df_fin"]+df_append["df_mts"]
df_append.drop("df_fin", axis=1, inplace=True)
df_append.drop("df_mts", axis=1, inplace=True)

#df_append.set_index('Date', inplace=True)
print(df_append)
df_append.to_csv("nccpl_mts.csv", mode='w')
#new_mts = pd.DataFrame()
#new_mts = df_append['sum_mts'].copy()
#print(new_mts)
#new_mts.set_index('Date', inplace=True)

# read old psx file
# df_psx = pd.read_csv('KSE_5yr_comb.csv')
# df_psx.set_index('Date', inplace=True)
# print(df_psx)


# combining old psx data with final mts data
# for i in df_append:
#     df_append1 = pd.merge(df_psx, df_append, how='left', on='Date')
#     dup = 'sum_mts'
#     if dup+"_x" in df_append1.columns:
#         x = dup+"_x"
#         y = dup+"_y"
#         df_append1["sum_mts"] = df_append1[y].fillna(df_append1[x])
#         df_append1.drop([x, y], 1, inplace=True)
# print(df_append1)

# # writing file
# df_append1.to_csv('KSE_5yr_comb.csv')



