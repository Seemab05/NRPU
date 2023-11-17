import tabula
import os
import csv
import datetime
import pandas as pd
import openpyxl
import xlrd
import warnings
warnings.filterwarnings("ignore")
# Date range inputs
# start_date = datetime.datetime(2015, 12, 9)
# end_date = datetime.datetime(2016, 1, 13)


start_date = datetime.datetime(2021, 4, 9)
end_date = datetime.datetime(2023, 5, 12)


def extract_value_from_xls(xls_file):
    try:
        # Open the XLS file using xlrd
        workbook = xlrd.open_workbook(xls_file)
        sheet = workbook.sheet_by_index(0)
        # print(sheet.cell_value(4, 4)) #(4,4) for before 2016 and (4,5) for after 2021
        # Check if cell F5 contains "(Amount in"
        # if sheet.cell_value(4, 4).startswith("(Amount in"): #before 2016
        if sheet.cell_value(4, 5).startswith("(Amount in"): #after 2021
            # Find the row with "Total:" at the end of the file
            total_row = -1  # Initialize with a default value
            for row in range(sheet.nrows):
                if sheet.cell_value(row, 0) == 'Total:':
                    total_row = row
                    print(total_row)
                    break
            
            # Check if the "Total:" row was found
            if total_row == -1:
                print("Error: 'Total:' row not found in the XLS file")
                return None
            
            # Get the value for the "Open Interest" column (amount in rupees)
            # open_interest_rupees = sheet.cell_value(total_row, 4) #before 2016
            open_interest_rupees = sheet.cell_value(total_row, 5) #after 2021
            
            return open_interest_rupees
        
        # Cell F5 does not contain the expected string, return None
        return "not a valid file"
    
    except xlrd.biffh.XLRDError as e:
        print(f"Unsupported format or corrupt file: {e}")
        return None


def extract_value_from_pdf(pdf_file_path):
    try:
        # Extract tables from the PDF file
        tables = tabula.read_pdf(pdf_file_path, pages='all')

        if tables:
            # Get the last table
            last_table = tables[-1]
            # Access the third value in the last row of the last table
            if len(last_table) > 0 and len(last_table.iloc[-1]) > 2:
                # return last_table.iloc[-1][4] #before 2016
                return last_table.iloc[-1][5] #after 2021
    except Exception as e:
        print(f"Error occurred during PDF extraction: {e}")
    return None



folder_path = 'C:/Users/Dell/Desktop/downloads'  # Provide the path to the folder containing the files
csv_file_path = 'open_interest.csv'  # Provide the path to the existing CSV file


# Check if the CSV file exists
if os.path.isfile(csv_file_path):
    # Check if the CSV file is empty (has no contents)
    with open(csv_file_path, 'r') as file:
        csv_reader = csv.reader(file)
        if not any(row for row in csv_reader):
            # Add the header row to the CSV file
            with open(csv_file_path, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Date', 'open_interest'])
        else:
            print("CSV file already has data.")
else:
    # Create the CSV file with the header
    with open(csv_file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Date', 'open_interest'])


# Iterate through the range of dates
current_date = start_date
while current_date <= end_date:
    date_string = current_date.strftime('%Y-%m-%d')
    pdf_file_path = os.path.join(folder_path, f'{date_string}.pdf')
    xls_file_path = os.path.join(folder_path, f'{date_string}.xls')

    if os.path.isfile(xls_file_path):
        # Extract the value from the XLS file
        result = extract_value_from_xls(xls_file_path)
        print("Result extracted from XLS FILE: ",date_string," ", result )
        if result == "not a valid file":
            current_date += datetime.timedelta(days=1)
            continue 
        elif result is not None:
            # Check if the date already exists in the CSV file
            date_exists = False
            with open(csv_file_path, 'r') as file:
                csv_reader = csv.reader(file)
                for row in csv_reader:
                    if len(row) > 0 and row[0] == date_string:
                        date_exists = True
                        break

            # Append the date and file name to the CSV file if it doesn't already exist
            if not date_exists:
                with open(csv_file_path, 'a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([date_string, result])
            else:
                print(f"Date {date_string} already exists in the CSV file")
        elif os.path.isfile(pdf_file_path):
                # Extract the value from the PDF file
                result = extract_value_from_pdf(pdf_file_path)
                print("Result extracted from PDF FILE: ",date_string," ", result)
                if result is not None:
                    # Check if the date already exists in the CSV file
                    date_exists = False
                    with open(csv_file_path, 'r') as file:
                        csv_reader = csv.reader(file)
                        for row in csv_reader:
                            if len(row) > 0 and row[0] == date_string:
                                date_exists = True
                                break
        else:
            print(f"No open interest value found for {date_string}")
            # Continue to the next iteration of the loop
            current_date += datetime.timedelta(days=1)
            continue  # Skip the rest of the code in the current iteration


    current_date += datetime.timedelta(days=1)

print("Process completed.")


# import pandas as pd
# data_xls = pd.read_excel('your_workbook.xls', 'Sheet1', index_col=None)
# data_xls.to_csv('your_csv.csv', encoding='utf-8')