import pandas as pd
import requests

# Load the CSV file
file_path = 'Examplar Prospects List.csv'
df = pd.read_csv(file_path)

# Assuming the website links are in column 'F'
websites = df.iloc[:, 5]  # Adjust the column index as necessary

# Initialize a list to store the status of each website
status_list = []

for url in websites:
    print(f"Checking {url}...")
    try:
        response = requests.get(url, timeout=10)
        if 200 <= response.status_code < 300:
            status = 'Online'
        else:
            status = 'Offline or Error'
    except requests.RequestException as e:
        status = f'Error - {e}'
    
    print(f"Status: {status}")
    status_list.append(status)

# Add the status back to the dataframe and save to a new CSV file
df['Website Status'] = status_list
df.to_csv('website_status_checked.csv', index=False)
