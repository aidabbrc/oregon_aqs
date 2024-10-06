import requests
import pandas as pd
import time
import json
import csv

# Load credentials from a JSON file
def load_credentials():
    with open('credentials.json', 'r') as f:
        credentials = json.load(f)
    return credentials['email'], credentials['api_key']

# Function to fetch air quality data for a single parameter
def fetch_aqs_data(email, api_key, param_code, state_code, year):
    base_url = 'https://aqs.epa.gov/data/api/sampleData/byState'
    bdate = f'{year}0101'
    edate = f'{year}1231'
    url = f'{base_url}?email={email}&key={api_key}&param={param_code}&bdate={bdate}&edate={edate}&state={state_code}'
    
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        return data.get('Data', [])
    else:
        print(f"Error fetching data for parameter {param_code} in {year}: {response.status_code}")
        return []

# Function to iterate over parameters and fetch data for each
def get_aqs_data_for_all_parameters(parameter_list, state_code, start_year, end_year):
    email, api_key = load_credentials()
    
    all_data = []

    for param_code in parameter_list:
        for year in range(start_year, end_year + 1):
            print(f"Fetching data for parameter {param_code} for year {year}...")
            data = fetch_aqs_data(email, api_key, param_code, state_code, year)
            if data:
                all_data.extend(data)
            
            # Pause to avoid hitting API limits
            time.sleep(1)
    
    return all_data

# Function to save data into CSV
def save_to_csv(data, filename):
    if data:
        df = pd.DataFrame(data)
        df.to_csv(filename, index=False)
        print(f"Data saved to {filename}.")
    else:
        print("No data to save.")

# Function to load the cleaned valid parameter codes from the CSV
def load_parameters_from_csv(csv_file):
    df = pd.read_csv(csv_file)
    return df['Parameter Code'].tolist()

# Main function
def main():
    # Constants
    state_code = '41'  # Oregon state code
    start_year = 2020
    end_year = 2020
    parameter_list_csv = 'parameterlist.csv'  # Your cleaned list of valid codes
    output_file = 'oregon_aqs_data.csv'
    
    # Load the cleaned parameter codes from the CSV
    parameter_list = load_parameters_from_csv(parameter_list_csv)
    
    # Fetch data for all valid parameters and save to CSV
    data = get_aqs_data_for_all_parameters(parameter_list, state_code, start_year, end_year)
    save_to_csv(data, output_file)

if __name__ == "__main__":
    main()
