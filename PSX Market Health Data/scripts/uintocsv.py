import os
import csv
from datetime import datetime

def read_csv_files(start_date, end_date, folder_path):
    result = []
    
    # Iterate over files in the folder
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.csv'):
            file_path = os.path.join(folder_path, file_name)
            
            # Extract the date from the file name
            file_date_str = os.path.splitext(file_name)[0]
            
            try:
                file_date = datetime.strptime(file_date_str, '%Y-%m-%d').date()
            except ValueError:
                print(f"Ignoring file with invalid date format: {file_name}")
                continue
            
            print(file_date)
            
            # Check if the file date is within the specified range
            if start_date <= file_date <= end_date:
                with open(file_path, 'r') as file:
                    reader = csv.DictReader(file)
                    rows = list(reader)
                    
                    # Check if the file has only a header and no values
                    if len(rows) <= 1:
                        print(f"No values in the file for date: {file_date}")
                        continue
                    
                    # Check if the sum is present in the last line for each column
                    if 'Trade Value' in rows[-1] and 'UIN Settlement Value ' in rows[-1]:
                    #     trade_sum = parse_float(rows[-1]['Trade Value'])
                    #     uin_sum = parse_float(rows[-1]['UIN Settlement Value '])
                    # else:
                        # Calculate the sum for each column
                        trade_sum = sum(parse_float(row['Trade Value']) for row in rows)
                        uin_sum = sum(parse_float(row['UIN Settlement Value ']) for row in rows)
                    
                    # Calculate the UIN percentage
                    uin_pct = uin_sum / trade_sum
                    print("UIN TRADE VALUE SUM:", trade_sum)
                    print("UIN SETTLEMENT VALUE SUM:", uin_sum)
                    print("UIN PCT:", uin_pct)
                    
                    # Append the result
                    result.append((file_date, uin_pct, trade_sum))
    
    return result

def parse_float(value):
    value = value.strip().replace(',', '')
    if value == '-':
        value = ''
    if value.strip() == '':
        return 0.0
    return float(value)

def write_result_to_csv(result, output_path):
    with open(output_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Date', 'UIN Percentage', 'Trade Value Sum'])
        
        for row in result:
            writer.writerow(row)

# Specify the start and end dates in the desired format
start_date = datetime.strptime('2021-04-09', '%Y-%m-%d').date()
end_date = datetime.strptime('2023-05-12', '%Y-%m-%d').date()

# Specify the folder path where the CSV files are located
folder_path = 'C:/Users/Dell/Desktop/downloads_uin'

# Specify the output file path
output_path = 'C:/Users/Dell/Desktop/downloads_uin/output1.csv'

# Read the CSV files and calculate the sums and UIN percentages
result = read_csv_files(start_date, end_date, folder_path)

# Write the result to a new CSV file
write_result_to_csv(result, output_path)
