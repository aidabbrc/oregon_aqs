OVERVIEW
The Oregon AQS Air Quality project pulls air quality data from the EPA's AQS API for a list of HAPs in Oregon. 

PREREQUISITES
Python
Git
AQS API credentials. Create credentials.json replace "your_email@example.com" with your registered email for AQS, and "your_aqs_api_key" with your AQS API key.
{
  "email": "your_email@example.com",
  "api_key": "your_aqs_api_key"
}


USAGE
Run the main.py script to fetch the air quality data for Oregon from the AQS API. This will pull data for all valid air quality parameters in Oregon from 20XX to 20YY (replace years in main.py) and save it in the oregon_aqs_data.csv file.

oregon_aqs/
│
├── main.py                   # Main script to fetch data
├── getaqscodes.py             # (Obsolete) Script to check valid AQS parameter codes
├── parameterlist.csv          # List of valid AQS parameter codes for Oregon
├── credentials.json           # (gitignored) AQS API credentials
├── oregon_aqs_data.csv        # Output file containing fetched AQS data
├── requirements.txt           # Python dependencies
├── .gitignore                 # Files to ignore in version control
└── README.md                  # Project documentation (this file)

