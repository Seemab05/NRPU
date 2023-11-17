import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
import time as t
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# access nccpl for uin_tradeValue and uin_pct
browser = uc.Chrome(use_subprocess=True)
url = 'https://www.nccpl.com.pk/en/market-information/settlement-un-listed-tfc-report'
start_date = datetime(2012, 1, 1)
end_date = datetime(2012, 6, 30)
pd.options.mode.chained_assignment = None


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days + 1)):
        yield start_date + timedelta(n)


browser.get(url)
df = pd.DataFrame()
dfs = pd.DataFrame()
date_list_filtered = []
date_list_filtered1 = []
x = 0
y1 = 0
uin_pct = 0
list_a = []
list_a1 = []

# daily uin trade data
for single_date in daterange(start_date, end_date):
    single_date = single_date.strftime('%d/%m/%Y')
    wait(browser, 20).until(EC.element_to_be_clickable((By.XPATH, "/html/body/section[2]/div/div[2]/div[1]/div/div/ul/li[2]/a"))).click()
    t.sleep(3)
    print('clicked tab!')
    print(single_date)

    # start date picker
    picker = wait(browser, 20).until(EC.presence_of_element_located((By.ID, 'popupDatepicker2')))
    browser.execute_script(f'arguments[0].value = "{single_date}";', picker)
    t.sleep(5)
    print('clicked the day!')

    browser.execute_script("window.scrollTo(0, 250.98)")
    t.sleep(2)

    wait(browser, 20).until(EC.element_to_be_clickable((By.XPATH, '/html/body/section[2]/div/div[2]/div[1]/div/div/div/div[2]/div/div[1]/form/div/div[2]/button'))).click()
    t.sleep(5)


# load uin data
    browser.execute_script("window.scrollTo(0, 400.98)")
    tbl = wait(browser, 20).until(EC.element_to_be_clickable((By.XPATH, "/html/body/section[2]/div/div[2]/div[1]/div/div/div/div[2]/div/div[3]/div/table"))).get_attribute('outerHTML')
    df = pd.read_html(tbl)
    t.sleep(5)
    dfs = pd.DataFrame.from_records(df[0])
    #browser.close()
    #print(type(dfs))

    if dfs.shape[0] == 0:
        x = 0
        uin_pct = 0
        print(x)
        list_a += [x]
        list_a1 += [uin_pct]
        date_list_filtered.append(single_date)
        date_list_filtered1.append(single_date)
    else:
        dfs = dfs[~dfs["Symbol"].isna()]

        x = dfs['Trade Value'].sum()
        dfs['UIN Settlement Value'] = dfs['UIN Settlement Value'].apply(lambda x1: "0" if x1 == "-" else x1)
        dfs[['UIN Settlement Value']] = dfs[['UIN Settlement Value']].apply(pd.to_numeric)
        #print(dfs['UIN Settlement Value'].iloc[119])
        y1 = dfs['UIN Settlement Value'].sum()
        print(dfs.dtypes)
        print(x)
        uin_pct = (y1/x)
        print(uin_pct)
        list_a += [x]
        list_a1 += [uin_pct]
        date_list_filtered.append(single_date)
        date_list_filtered1.append(single_date)

print(list_a)
print(list_a1)

df_uin = pd.DataFrame(list(zip(date_list_filtered, list_a)), columns=['Date', 'uin_tradeValue'])
df_uin.set_index('Date', inplace=True)
print(df_uin)

df_uin_pct = pd.DataFrame(list(zip(date_list_filtered1, list_a1)), columns=['Date', 'uin_pct'])
df_uin_pct.set_index('Date', inplace=True)
print(df_uin_pct)

# read old psx file
df_psx = pd.read_csv('KSE_5yr_comb.csv')
df_psx.set_index('Date', inplace=True)
print(df_psx)


# combining old psx data with uin new data
for i in df_uin:
    df_append = pd.merge(df_psx, df_uin, how='left', on='Date')
    dup = 'uin_tradeValue'
    if dup+"_x" in df_append.columns:
        x = dup+"_x"
        y = dup+"_y"
        df_append["uin_tradeValue"] = df_append[y].fillna(df_append[x])
        df_append.drop([x, y], 1, inplace=True)
print(df_append)

# concatenating uin_pct new data
for i in df_uin_pct:
    df_append1 = pd.merge(df_append, df_uin_pct, how='left', on='Date')
    dup = 'uin_pct'
    if dup+"_x" in df_append1.columns:
        x = dup+"_x"
        y = dup+"_y"
        df_append1["uin_pct"] = df_append1[y].fillna(df_append1[x])
        df_append1.drop([x, y], 1, inplace=True)
print(df_append1)

# writing file
df_append1.to_csv('KSE_5yr_comb.csv')



