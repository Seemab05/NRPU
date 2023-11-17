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
        return None  # You can choose to handle other cases as needed


# Load and rename columns for EGCH Historical Data
egch_data = pd.read_csv("chemical\EGCH Historical Data.csv", parse_dates=['Date'])
egch_data = egch_data.rename(columns={"Price": "close_EGCH", "Open": "open_EGCH", "High": "high_EGCH", "Low": "low_EGCH","Vol.": "vol_EGCH", "Change %": "change%_EGCH"})
egch_data['close_EGCH'] = egch_data['close_EGCH'].astype(float)
egch_data['high_EGCH'] = egch_data['high_EGCH'].astype(float)
egch_data['low_EGCH'] = egch_data['low_EGCH'].astype(float)
egch_data['open_EGCH'] = egch_data['open_EGCH'].astype(float)
egch_data['change%_EGCH'] = egch_data['change%_EGCH'].str.rstrip('%').astype(float)
# Apply the function to the 'Volume' column
egch_data['vol_EGCH'] = egch_data['vol_EGCH'].apply(convert_volume_to_float)

egch_data=egch_data.set_index('Date')
egch_data = egch_data.resample('D').ffill()

# Calculate EMA 55
egch_data['EGCH_EMA_55'] = egch_data['close_EGCH'].ewm(span=55, adjust=False).mean()

# Calculate EMA 100
egch_data['EGCH_EMA_100'] = egch_data['close_EGCH'].ewm(span=100, adjust=False).mean()

# Calculate EMA 200
egch_data['EGCH_EMA_200'] = egch_data['close_EGCH'].ewm(span=200, adjust=False).mean()

# Display the DataFrame with the added EMA columns
# print(egch_data.head(15))

# Load and rename columns for FATF
fatf_data = pd.read_csv("chemical\FATF Historical Data.csv", parse_dates=['Date'])
fatf_data = fatf_data.rename(columns={"Price": "close_FATF", "Open": "open_FATF", "High": "high_FATF", "Low": "low_FATF","Vol.": "vol_FATF", "Change %": "change%_FATF"})
fatf_data['close_FATF'] = fatf_data['close_FATF'].astype(float)
fatf_data['high_FATF'] = fatf_data['high_FATF'].astype(float)
fatf_data['low_FATF'] = fatf_data['low_FATF'].astype(float)
fatf_data['open_FATF'] = fatf_data['open_FATF'].astype(float)
fatf_data['change%_FATF'] = fatf_data['change%_FATF'].str.rstrip('%').astype(float)

# Apply the function to the 'Volume' column
fatf_data['vol_FATF'] = fatf_data['vol_FATF'].apply(convert_volume_to_float)


fatf_data=fatf_data.set_index('Date')
fatf_data = fatf_data.resample('D').ffill()

# Calculate EMA 55
fatf_data['FATF_EMA_55'] = fatf_data['close_FATF'].ewm(span=55, adjust=False).mean()
# Calculate EMA 100
fatf_data['FATF_EMA_100'] = fatf_data['close_FATF'].ewm(span=100, adjust=False).mean()
# Calculate EMA 200
fatf_data['FATF_EMA_200'] = fatf_data['close_FATF'].ewm(span=200, adjust=False).mean()

# Display the DataFrame with the added EMA columns
print(fatf_data.head(15))

# Load and rename columns for FAUF
FAUF_data = pd.read_csv("chemical\FAUF Historical Data.csv", parse_dates=['Date'])
FAUF_data = FAUF_data.rename(columns={"Price": "close_FAUF", "Open": "open_FAUF", "High": "high_FAUF", "Low": "low_FAUF","Vol.": "vol_FAUF", "Change %": "change%_FAUF"})
FAUF_data['close_FAUF'] = FAUF_data['close_FAUF'].astype(float)
FAUF_data['high_FAUF'] = FAUF_data['high_FAUF'].astype(float)
FAUF_data['low_FAUF'] = FAUF_data['low_FAUF'].astype(float)
FAUF_data['open_FAUF'] = FAUF_data['open_FAUF'].astype(float)
FAUF_data['change%_FAUF'] = FAUF_data['change%_FAUF'].str.rstrip('%').astype(float)

# Apply the function to the 'Volume' column
FAUF_data['vol_FAUF'] = FAUF_data['vol_FAUF'].apply(convert_volume_to_float)


FAUF_data=FAUF_data.set_index('Date')
FAUF_data = FAUF_data.resample('D').ffill()


# Calculate EMA 55
FAUF_data['FAUF_EMA_55'] = FAUF_data['close_FAUF'].ewm(span=55, adjust=False).mean()
# Calculate EMA 100
FAUF_data['FAUF_EMA_100'] = FAUF_data['close_FAUF'].ewm(span=100, adjust=False).mean()
# Calculate EMA 200
FAUF_data['FAUF_EMA_200'] = FAUF_data['close_FAUF'].ewm(span=200, adjust=False).mean()

# Display the DataFrame with the added EMA columns
# print(FAUF_data.tail(15))

# Merge all DataFrames on the 'Date' column
combined_data = pd.merge(egch_data, fatf_data, on='Date', how='inner')
combined_data = pd.merge(combined_data, FAUF_data, on='Date', how='inner')

# Display the combined DataFrame
print(combined_data)

# Create subplots for each company
fig, ax = plt.subplots(figsize=(12, 6))

# Plot closing prices for Company 1
combined_data['close_EGCH'].plot(label='EGCH', ax=ax)

# Plot closing prices for Company 2
combined_data['close_FATF'].plot(label='FATF', ax=ax)

# Plot closing prices for Company 3
combined_data['close_FAUF'].plot(label='FAUF', ax=ax)

# Customize the plot
ax.set_title('Closing Prices Over Time')
ax.set_xlabel('Date')
ax.set_ylabel('Closing Price')
plt.grid(True)
plt.legend()

# Show the plot
plt.tight_layout()
plt.show()


# print(combined_data.columns)
# combined_data.to_csv('chemical/combined_Sector_chemical.csv')

# Extract the relevant columns for BEST, KOHC, and LUKC
egch_data = combined_data[['close_EGCH', 'EGCH_EMA_55', 'EGCH_EMA_100', 'EGCH_EMA_200']]
fatf_data = combined_data[['close_FATF', 'FATF_EMA_55', 'FATF_EMA_100', 'FATF_EMA_200']]
FAUF_data = combined_data[['close_FAUF', 'FAUF_EMA_55', 'FAUF_EMA_100', 'FAUF_EMA_200']]


# Create a 2x2 grid of subplots
fig, axs = plt.subplots(2, 2, figsize=(12, 8))

# Plot EGCH data in the first subplot
axs[0, 0].plot(egch_data.index, egch_data['close_EGCH'], label='Close Price', linewidth=2)
axs[0, 0].plot(egch_data.index, egch_data['EGCH_EMA_55'], label='EMA 55', linestyle='--')
axs[0, 0].plot(egch_data.index, egch_data['EGCH_EMA_100'], label='EMA 100', linestyle='--')
axs[0, 0].plot(egch_data.index, egch_data['EGCH_EMA_200'], label='EMA 200', linestyle='--')
axs[0, 0].set_title('EGCH Close Price and EMAs')
axs[0, 0].set_xlabel('Date')
axs[0, 0].set_ylabel('Price')
axs[0, 0].legend()
axs[0, 0].grid(True)


# Plot FATF data in the second subplot
axs[0, 1].plot(fatf_data.index, fatf_data['close_FATF'], label='Close Price', linewidth=2)
axs[0, 1].plot(fatf_data.index, fatf_data['FATF_EMA_55'], label='EMA 55', linestyle='--')
axs[0, 1].plot(fatf_data.index, fatf_data['FATF_EMA_100'], label='EMA 100', linestyle='--')
axs[0, 1].plot(fatf_data.index, fatf_data['FATF_EMA_200'], label='EMA 200', linestyle='--')
axs[0, 1].set_title('FATF Close Price and EMAs')
axs[0, 1].set_xlabel('Date')
axs[0, 1].set_ylabel('Price')
axs[0, 1].legend()
axs[0, 1].grid(True)



# Plot FAUF data in the third subplot
axs[1, 0].plot(FAUF_data.index, FAUF_data['close_FAUF'], label='Close Price', linewidth=2)
axs[1, 0].plot(FAUF_data.index, FAUF_data['FAUF_EMA_55'], label='EMA 55', linestyle='-')
axs[1, 0].plot(FAUF_data.index, FAUF_data['FAUF_EMA_100'], label='EMA 100', linestyle='-')
axs[1, 0].plot(FAUF_data.index, FAUF_data['FAUF_EMA_200'], label='EMA 200', linestyle='-')
axs[1, 0].set_title('FAUF Close Price and EMAs')
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




