import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg


def convert_volume_to_float(volume_str):
    if isinstance(volume_str, str):
        if 'M' in volume_str:
            return float(volume_str.replace('M', '')) * 1e6  # 1 million
        elif 'K' in volume_str:
            return float(volume_str.replace('K', '')) * 1e3  # 1 thousand
        else:
            return float(volume_str)
    elif isinstance(volume_str, float):
        return volume_str  # Return the float value as is
    else:
        return None  


# Load and rename columns for BEST Historical Data
best_data = pd.read_csv("construction\BEST Historical Data.csv", parse_dates=['Date'])
best_data = best_data.rename(columns={"Price": "close_BEST", "Open": "open_BEST", "High": "high_BEST", "Low": "low_BEST","Vol.": "vol_BEST", "Change %": "change%_BEST"})
best_data['close_BEST'] = best_data['close_BEST'].astype(float)
best_data['high_BEST'] = best_data['high_BEST'].astype(float)
best_data['low_BEST'] = best_data['low_BEST'].astype(float)
best_data['open_BEST'] = best_data['open_BEST'].astype(float)
best_data['change%_BEST'] = best_data['change%_BEST'].str.rstrip('%').astype(float)
# Apply the function to the 'Volume' column
best_data['vol_BEST'] = best_data['vol_BEST'].apply(convert_volume_to_float)

best_data=best_data.set_index('Date')
# best_data = best_data.resample('D').ffill()

# Calculate EMA 55
# best_data['BEST_EMA_55'] = best_data['close_BEST'].ewm(span=55, adjust=False).mean()

# Calculate EMA 100
# best_data['BEST_EMA_100'] = best_data['close_BEST'].ewm(span=100, adjust=False).mean()

# Calculate EMA 200
# best_data['BEST_EMA_200'] = best_data['close_BEST'].ewm(span=200, adjust=False).mean()

# Display the DataFrame with the added EMA columns
print(best_data)

# Load and rename columns for KOHC
kohc_data = pd.read_csv("construction\KOHC Historical Data.csv", parse_dates=['Date'])
kohc_data = kohc_data.rename(columns={"Price": "close_KOHC", "Open": "open_KOHC", "High": "high_KOHC", "Low": "low_KOHC","Vol.": "vol_KOHC", "Change %": "change%_KOHC"})
kohc_data['close_KOHC'] = kohc_data['close_KOHC'].astype(float)
kohc_data['high_KOHC'] = kohc_data['high_KOHC'].astype(float)
kohc_data['low_KOHC'] = kohc_data['low_KOHC'].astype(float)
kohc_data['open_KOHC'] = kohc_data['open_KOHC'].astype(float)
kohc_data['change%_KOHC'] = kohc_data['change%_KOHC'].str.rstrip('%').astype(float)

# Apply the function to the 'Volume' column
kohc_data['vol_KOHC'] = kohc_data['vol_KOHC'].apply(convert_volume_to_float)


kohc_data=kohc_data.set_index('Date')
# kohc_data = kohc_data.resample('D').ffill()

# Calculate EMA 55
kohc_data['KOHC_EMA_55'] = kohc_data['close_KOHC'].ewm(span=55, adjust=False).mean()
# Calculate EMA 100
kohc_data['KOHC_EMA_100'] = kohc_data['close_KOHC'].ewm(span=100, adjust=False).mean()
# Calculate EMA 200
kohc_data['KOHC_EMA_200'] = kohc_data['close_KOHC'].ewm(span=200, adjust=False).mean()

# Display the DataFrame with the added EMA columns
# print(kohc_data.head(15))

# Load and rename columns for LUKC
LUKC_data = pd.read_csv("construction\LUKC Historical Data.csv", parse_dates=['Date'])
LUKC_data = LUKC_data.rename(columns={"Price": "close_LUKC", "Open": "open_LUKC", "High": "high_LUKC", "Low": "low_LUKC","Vol.": "vol_LUKC", "Change %": "change%_LUKC"})
LUKC_data['close_LUKC'] = LUKC_data['close_LUKC'].astype(float)
LUKC_data['high_LUKC'] = LUKC_data['high_LUKC'].str.replace(',', '').astype(float)
LUKC_data['low_LUKC'] = LUKC_data['low_LUKC'].astype(float)
LUKC_data['open_LUKC'] = LUKC_data['open_LUKC'].str.replace(',', '').astype(float)
LUKC_data['change%_LUKC'] = LUKC_data['change%_LUKC'].str.rstrip('%').astype(float)

# Apply the function to the 'Volume' column
LUKC_data['vol_LUKC'] = LUKC_data['vol_LUKC'].apply(convert_volume_to_float)


LUKC_data=LUKC_data.set_index('Date')
# LUKC_data = LUKC_data.resample('D').ffill()


# Calculate EMA 55
LUKC_data['LUKC_EMA_55'] = LUKC_data['close_LUKC'].ewm(span=55, adjust=False).mean()
# Calculate EMA 100
LUKC_data['LUKC_EMA_100'] = LUKC_data['close_LUKC'].ewm(span=100, adjust=False).mean()
# Calculate EMA 200
LUKC_data['LUKC_EMA_200'] = LUKC_data['close_LUKC'].ewm(span=200, adjust=False).mean()

# Display the DataFrame with the added EMA columns
# print(LUKC_data.tail(15))

# Find the sector with the maximum date length
sectors = [best_data, kohc_data, LUKC_data]
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
combined_data['BEST_EMA_55'] = combined_data['close_BEST'].ewm(span=55, adjust=False).mean()

# Calculate EMA 100
combined_data['BEST_EMA_100'] = combined_data['close_BEST'].ewm(span=100, adjust=False).mean()

# Calculate EMA 200
combined_data['BEST_EMA_200'] = combined_data['close_BEST'].ewm(span=200, adjust=False).mean()

print(combined_data)
combined_data.to_csv('D:/sahar_cpins/Phd/NLFF/DATA/construction/combined_all_construction.csv')

# Create subplots for each company
fig, ax = plt.subplots(figsize=(12, 6))

# Plot closing prices for Company 1
combined_data['close_BEST'].plot(label='BEST', ax=ax)

# Plot closing prices for Company 2
combined_data['close_KOHC'].plot(label='KOHC', ax=ax)

# Plot closing prices for Company 3
combined_data['close_LUKC'].plot(label='LUKC', ax=ax)

# Customize the plot
ax.set_title('Closing Prices Over Time - Construction Sector')
ax.set_xlabel('Year')
ax.set_ylabel('Closing Price')
plt.grid(True)
plt.legend()

# Show the plot
plt.tight_layout()
plt.show()


# Extract the relevant columns for BEST, KOHC, and LUKC
best_data = combined_data[['close_BEST', 'BEST_EMA_55', 'BEST_EMA_100', 'BEST_EMA_200']]
kohc_data = combined_data[['close_KOHC', 'KOHC_EMA_55', 'KOHC_EMA_100', 'KOHC_EMA_200']]
LUKC_data = combined_data[['close_LUKC', 'LUKC_EMA_55', 'LUKC_EMA_100', 'LUKC_EMA_200']]

print(best_data)
# Create a 2x2 grid of subplots
fig, axs = plt.subplots(2, 2, figsize=(12, 8))

# Plot APL data in the first subplot
axs[0, 0].plot(best_data.index, best_data['close_BEST'], label='Close Price', linewidth=2)
axs[0, 0].plot(best_data.index, best_data['BEST_EMA_55'], label='EMA 55', linestyle='--')
axs[0, 0].plot(best_data.index, best_data['BEST_EMA_100'], label='EMA 100', linestyle='--')
axs[0, 0].plot(best_data.index, best_data['BEST_EMA_200'], label='EMA 200', linestyle='--')
axs[0, 0].set_title('BEST Close Price and EMAs')
axs[0, 0].set_xlabel('Year')
axs[0, 0].set_ylabel('Price')
axs[0, 0].legend()
axs[0, 0].grid(True)


# Plot KOHC data in the second subplot
axs[0, 1].plot(kohc_data.index, kohc_data['close_KOHC'], label='Close Price', linewidth=2)
axs[0, 1].plot(kohc_data.index, kohc_data['KOHC_EMA_55'], label='EMA 55', linestyle='--')
axs[0, 1].plot(kohc_data.index, kohc_data['KOHC_EMA_100'], label='EMA 100', linestyle='--')
axs[0, 1].plot(kohc_data.index, kohc_data['KOHC_EMA_200'], label='EMA 200', linestyle='--')
axs[0, 1].set_title('KOHC Close Price and EMAs')
axs[0, 1].set_xlabel('Year')
axs[0, 1].set_ylabel('Price')
axs[0, 1].legend()
axs[0, 1].grid(True)



# Plot LUKC data in the third subplot
axs[1, 0].plot(LUKC_data.index, LUKC_data['close_LUKC'], label='Close Price', linewidth=2)
axs[1, 0].plot(LUKC_data.index, LUKC_data['LUKC_EMA_55'], label='EMA 55', linestyle='-')
axs[1, 0].plot(LUKC_data.index, LUKC_data['LUKC_EMA_100'], label='EMA 100', linestyle='-')
axs[1, 0].plot(LUKC_data.index, LUKC_data['LUKC_EMA_200'], label='EMA 200', linestyle='-')
axs[1, 0].set_title('LUKC Close Price and EMAs')
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




