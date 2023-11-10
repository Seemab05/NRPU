import pandas as pd

df_tbills = pd.read_excel('tb.xlsx', parse_dates=['Auction Date'])
df_tbills.rename(columns={'Realized Amount': 'tbills_price', 'Auction Date': 'Date'}, inplace=True)
df_tbills = df_tbills[['Date', 'tbills_price']]
df_tbills = df_tbills.groupby('Date').first()

# If bids are rejected, delete the row
df_tbills = df_tbills.drop(df_tbills[df_tbills['tbills_price'] == 'Bids Rejected'].index)
df_tbills['tbills_price'] = df_tbills['tbills_price'].astype(float)

# Set frequency to 'D' for daily
df_tbills = df_tbills.resample('D').asfreq()

# Interpolate missing values using forward fill
df_tbills['tbills_price'] = df_tbills['tbills_price'].interpolate()

df_tbills['tbills_change_pct'] = df_tbills['tbills_price'].pct_change()
df_tbills['tbills_mv10'] = df_tbills['tbills_price'].rolling(10).mean()

# Read old psx file
df_psx = pd.read_csv('KSE_5yr_comb.csv')
df_psx['Date'] = pd.to_datetime(df_psx['Date'])
df_psx.set_index('Date', inplace=True)

#combining old psx data with tbills_change_pct new data
for i in df_tbills:
    df_append = pd.merge(df_psx, df_tbills, how='left', on='Date')
    dup = 'tbills_change_pct'
    if dup+"_x" in df_append.columns:
        x = dup+"_x"
        y = dup+"_y"
        df_append["tbills_change_pct"] = df_append[y].fillna(df_append[x])
        df_append.drop([x, y], 1, inplace=True)



df_append.to_csv('KSE_5yr_comb1.csv')
