import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg


# Define a function to convert the values
def convert_volume_to_float(volume_str):
    if 'M' in volume_str:
        return float(volume_str.replace('M', '')) * 1e6  # 1 million
    elif 'K' in volume_str:
        return float(volume_str.replace('K', '')) * 1e3  # 1 thousand
    else:
        return float(volume_str)

# Load and rename columns for APL Historical Data
apl_data = pd.read_csv("oil_n_gas\APL Historical Data.csv", parse_dates=['Date'])
apl_data = apl_data.rename(columns={"Price": "close_APL", "Open": "open_APL", "High": "high_APL", "Low": "low_APL","Vol.": "vol_APL", "Change %": "change%_APL"})
apl_data['close_APL'] = apl_data['close_APL'].astype(float)
apl_data['high_APL'] = apl_data['high_APL'].astype(float)
apl_data['low_APL'] = apl_data['low_APL'].astype(float)
apl_data['open_APL'] = apl_data['open_APL'].astype(float)
apl_data['change%_APL'] = apl_data['change%_APL'].str.rstrip('%').astype(float)
# Apply the function to the 'Volume' column
apl_data['vol_APL'] = apl_data['vol_APL'].apply(convert_volume_to_float)
# print(apl_data)
apl_data=apl_data.set_index('Date')
# apl_data = apl_data.resample('D').ffill()

# # Calculate EMA 55
# apl_data['APL_EMA_55'] = apl_data['close_APL'].ewm(span=55, adjust=False).mean()

# # Calculate EMA 100
# apl_data['APL_EMA_100'] = apl_data['close_APL'].ewm(span=100, adjust=False).mean()

# # Calculate EMA 200
# apl_data['APL_EMA_200'] = apl_data['close_APL'].ewm(span=200, adjust=False).mean()

# Display the DataFrame with the added EMA columns
# print(apl_data.head(15))

# Load and rename columns for MGAS
MGAS_data = pd.read_csv("oil_n_gas\MGAS Historical Data.csv", parse_dates=['Date'])
MGAS_data = MGAS_data.rename(columns={"Price": "close_MGAS", "Open": "open_MGAS", "High": "high_MGAS", "Low": "low_MGAS","Vol.": "vol_MGAS", "Change %": "change%_MGAS"})
MGAS_data['close_MGAS'] = MGAS_data['close_MGAS'].str.replace(',', '').astype(float)
MGAS_data['high_MGAS'] = MGAS_data['high_MGAS'].str.replace(',', '').astype(float)
MGAS_data['low_MGAS'] = MGAS_data['low_MGAS'].str.replace(',', '').astype(float)
MGAS_data['open_MGAS'] = MGAS_data['open_MGAS'].str.replace(',', '').astype(float)
MGAS_data['change%_MGAS'] = MGAS_data['change%_MGAS'].str.rstrip('%').astype(float)

# Apply the function to the 'Volume' column
MGAS_data['vol_MGAS'] = MGAS_data['vol_MGAS'].apply(convert_volume_to_float)
# print(MGAS_data)

MGAS_data=MGAS_data.set_index('Date')
# MGAS_data = MGAS_data.resample('D').ffill()
# print(MGAS_data)

# Calculate EMA 55
MGAS_data['MGAS_EMA_55'] = MGAS_data['close_MGAS'].ewm(span=55, adjust=False).mean()
# Calculate EMA 100
MGAS_data['MGAS_EMA_100'] = MGAS_data['close_MGAS'].ewm(span=100, adjust=False).mean()
# Calculate EMA 200
MGAS_data['MGAS_EMA_200'] = MGAS_data['close_MGAS'].ewm(span=200, adjust=False).mean()

# Display the DataFrame with the added EMA columns
print(MGAS_data.head(15))

# Load and rename columns for OGDC
OGDC_data = pd.read_csv("oil_n_gas\OGDC Historical Data.csv", parse_dates=['Date'])
OGDC_data = OGDC_data.rename(columns={"Price": "close_OGDC", "Open": "open_OGDC", "High": "high_OGDC", "Low": "low_OGDC","Vol.": "vol_OGDC", "Change %": "change%_OGDC"})
OGDC_data['close_OGDC'] = OGDC_data['close_OGDC'].astype(float)
OGDC_data['high_OGDC'] = OGDC_data['high_OGDC'].astype(float)
OGDC_data['low_OGDC'] = OGDC_data['low_OGDC'].astype(float)
OGDC_data['open_OGDC'] = OGDC_data['open_OGDC'].astype(float)
OGDC_data['change%_OGDC'] = OGDC_data['change%_OGDC'].str.rstrip('%').astype(float)

# Apply the function to the 'Volume' column
OGDC_data['vol_OGDC'] = OGDC_data['vol_OGDC'].apply(convert_volume_to_float)
# print(OGDC_data)

OGDC_data=OGDC_data.set_index('Date')
# OGDC_data = OGDC_data.resample('D').ffill()
# print(OGDC_data)

# Calculate EMA 55
OGDC_data['OGDC_EMA_55'] = OGDC_data['close_OGDC'].ewm(span=55, adjust=False).mean()
# Calculate EMA 100
OGDC_data['OGDC_EMA_100'] = OGDC_data['close_OGDC'].ewm(span=100, adjust=False).mean()
# Calculate EMA 200
OGDC_data['OGDC_EMA_200'] = OGDC_data['close_OGDC'].ewm(span=200, adjust=False).mean()

# Display the DataFrame with the added EMA columns
# print(OGDC_data.tail(15))

# Merge all DataFrames on the 'Date' column
# combined_data = pd.merge(apl_data, MGAS_data, on='Date', how='inner')
# combined_data = pd.merge(combined_data, OGDC_data, on='Date', how='inner')
# Find the sector with the maximum date length
sectors = [apl_data, MGAS_data, OGDC_data]
max_length_sector = max(sectors, key=lambda x: len(x))
print(max_length_sector)

max_length_sector.set_index(max_length_sector.index, inplace=True)
combined_data = max_length_sector.copy()

# Merge data from each sector based on the date column
for sector_df in sectors:
    if sector_df is not max_length_sector:
        combined_data = combined_data.merge(sector_df, on='Date', how='outer', suffixes=('', f'_{sector_df.iloc[0, 0]}'))

# Forward fill missing data in the combined DataFrame
combined_data.fillna(method='ffill', inplace=True)

# Calculate EMA 55
combined_data['APL_EMA_55'] = combined_data['close_APL'].ewm(span=55, adjust=False).mean()

# Calculate EMA 100
combined_data['APL_EMA_100'] = combined_data['close_APL'].ewm(span=100, adjust=False).mean()

# Calculate EMA 200
combined_data['APL_EMA_200'] = combined_data['close_APL'].ewm(span=200, adjust=False).mean()

# Display the combined DataFrame
print(combined_data)

combined_data.to_csv('D:/sahar_cpins/Phd/NLFF/DATA/oil_n_gas/combined_all_petroleum.csv')


# Create subplots for each company
fig, ax = plt.subplots(figsize=(12, 6))

# Plot closing prices for Company 1
combined_data['close_APL'].plot(label='Attock petroleum Limited', ax=ax)

# Plot closing prices for Company 2
combined_data['close_MGAS'].plot(label='Mari', ax=ax)

# Plot closing prices for Company 3
combined_data['close_OGDC'].plot(label='OGDCL', ax=ax)

# Customize the plot
ax.set_title('Closing Prices Over Time - Petroleum Sector')
ax.set_xlabel('Year')
ax.set_ylabel('Closing Price')
plt.grid(True)
plt.legend()

# Show the plot
plt.tight_layout()
plt.show()


# print(combined_data.columns)
# combined_data.to_csv('oil_n_gas/combined_Sector_petroleum.csv')

# Extract the relevant columns for APL, MGAS, and OGDC
apl_data = combined_data[['close_APL', 'APL_EMA_55', 'APL_EMA_100', 'APL_EMA_200']]
mgas_data = combined_data[['close_MGAS', 'MGAS_EMA_55', 'MGAS_EMA_100', 'MGAS_EMA_200']]
ogdc_data = combined_data[['close_OGDC', 'OGDC_EMA_55', 'OGDC_EMA_100', 'OGDC_EMA_200']]

# Create a 2x2 grid of subplots
fig, axs = plt.subplots(2, 2, figsize=(12, 8))

# Plot APL data in the first subplot
axs[0, 0].plot(apl_data.index, apl_data['close_APL'], label='Close Price', linewidth=2)
axs[0, 0].plot(apl_data.index, apl_data['APL_EMA_55'], label='EMA 55', linestyle='--')
axs[0, 0].plot(apl_data.index, apl_data['APL_EMA_100'], label='EMA 100', linestyle='--')
axs[0, 0].plot(apl_data.index, apl_data['APL_EMA_200'], label='EMA 200', linestyle='--')
axs[0, 0].set_title('APL Close Price and EMAs')
axs[0, 0].set_xlabel('Year')
axs[0, 0].set_ylabel('Price')
axs[0, 0].legend()
axs[0, 0].grid(True)


# Plot MGAS data in the second subplot
axs[0, 1].plot(mgas_data.index, mgas_data['close_MGAS'], label='Close Price', linewidth=2)
axs[0, 1].plot(mgas_data.index, mgas_data['MGAS_EMA_55'], label='EMA 55', linestyle='--')
axs[0, 1].plot(mgas_data.index, mgas_data['MGAS_EMA_100'], label='EMA 100', linestyle='--')
axs[0, 1].plot(mgas_data.index, mgas_data['MGAS_EMA_200'], label='EMA 200', linestyle='--')
axs[0, 1].set_title('MGAS Close Price and EMAs')
axs[0, 1].set_xlabel('Year')
axs[0, 1].set_ylabel('Price')
axs[0, 1].legend()
axs[0, 1].grid(True)



# Plot OGDC data in the third subplot
axs[1, 0].plot(ogdc_data.index, ogdc_data['close_OGDC'], label='Close Price', linewidth=2)
axs[1, 0].plot(ogdc_data.index, ogdc_data['OGDC_EMA_55'], label='EMA 55', linestyle='-')
axs[1, 0].plot(ogdc_data.index, ogdc_data['OGDC_EMA_100'], label='EMA 100', linestyle='-')
axs[1, 0].plot(ogdc_data.index, ogdc_data['OGDC_EMA_200'], label='EMA 200', linestyle='-')
axs[1, 0].set_title('OGDC Close Price and EMAs')
axs[1, 0].set_xlabel('Year')
axs[1, 0].set_ylabel('Close Price')
axs[1, 0].legend()
axs[1, 0].grid(True)

# Hide the fourth subplot
axs[1, 1].axis('off')

# Add an image to the fourth subplot
img = mpimg.imread('dollor_pkr\CLOSE-KSE100.png')  # Replace 'your_image_file.png' with your image file path
axs[1, 1].imshow(img)

# Adjust spacing between subplots
plt.tight_layout()

# Show the plot
plt.show()




