import requests
import pandas as pd
import time
import csv
import json

# Load credentials from a JSON file
def load_credentials():
    with open('credentials.json', 'r') as f:
        credentials = json.load(f)
    return credentials['email'], credentials['api_key']

# Function to fetch data for a parameter and check if any data exists
def check_aqs_data_for_param(email, api_key, param_code, state_code, start_year, end_year):
    base_url = 'https://aqs.epa.gov/data/api/sampleData/byState'
    
    for year in range(start_year, end_year + 1):
        bdate = f'{year}0101'
        edate = f'{year}1231'
        url = f'{base_url}?email={email}&key={api_key}&param={param_code}&bdate={bdate}&edate={edate}&state={state_code}'
        
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('Data'):  # If there's data, return True
                return True
        time.sleep(1)  # To avoid hitting API limits
    return False

# Function to get valid parameter codes
def get_valid_aqs_codes(parameter_list, state_code, start_year, end_year):
    email, api_key = load_credentials()
    valid_parameters = []

    for param_code in parameter_list:
        print(f"Checking data availability for parameter {param_code}...")
        if check_aqs_data_for_param(email, api_key, param_code, state_code, start_year, end_year):
            print(f"Data found for parameter {param_code}.")
            valid_parameters.append(param_code)
        else:
            print(f"No data for parameter {param_code}.")
    
    return valid_parameters

# Save valid parameter codes to CSV
def save_valid_parameter_codes(valid_codes, filename):
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Parameter Code'])  # Write header
        for code in valid_codes:
            writer.writerow([code])

# Load parameter codes from CSV
def load_parameters_from_csv(csv_file):
    df = pd.read_csv(csv_file)
    return df['Parameter Code'].tolist()

def main():
    state_code = '41'  # Oregon state code
    start_year = 2013
    end_year = 2023
    parameter_list_csv = 'parameterlist.csv'
    valid_parameter_codes_file = 'valid_parameter_codes.csv'

    # Load all parameter codes from the provided CSV
    parameter_list = load_parameters_from_csv(parameter_list_csv)

    # Get valid parameter codes (ones that return data)
    valid_codes = get_valid_aqs_codes(parameter_list, state_code, start_year, end_year)

    # Save the valid parameter codes to a file for future use
    save_valid_parameter_codes(valid_codes, valid_parameter_codes_file)
    print(f"Valid parameter codes saved to {valid_parameter_codes_file}.")

if __name__ == "__main__":
    main()
