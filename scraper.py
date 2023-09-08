import os
import json
import requests
import pandas as pd
from urllib.parse import urlparse
import urllib.parse
from tqdm import tqdm
from datetime import datetime
from insert_db_script import insert_into_db
from create_db import create_db

from requests import Session

session = requests.Session()

def get_domain(url):
    parsed_url = urlparse(url)
    domain = parsed_url.scheme + "://" + parsed_url.netloc
    return domain

def scraper():

    # Fetch vehicle makes data from the given URL
    makes_url = "https://dashboard.kaiandkaro.com/api/v1/vehicle-makes/"
    response = session.get(makes_url)
    makes_data = response.json()

    # Extract model_make options from the makes_data response
    model_make_options = [make["name"] for make in makes_data]

    dealer_name = "Kai & Karo"
    dealer_website = "https://www.kaiandkaro.com"
    dealer_domain = get_domain(dealer_website)

    car_info_list = []

    start_time = datetime.now()  # Record the start time

    for model_make in model_make_options:
        # Encode the model_make string
        encoded_model_make = urllib.parse.quote(model_make)

        page = 1
        while True:
            url = f"https://www.kaiandkaro.com/_next/data/V59c9TMNrmk5nnPVhikd4/vehicles.json?model__make__name={encoded_model_make}&page={page}"
            print(url)

            response = session.get(url)
            try:
                data = response.json()
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON for {url}: {e}")
                continue  # Skip this iteration and move to the next

            if not data.get('pageProps', {}).get('vehicles'):
                break

            car_data = data['pageProps']['vehicles']

            for car in tqdm(car_data, desc=f"Retrieving {model_make} vehicles"):
                car_info_list.append(car)

            page += 1

    end_time = datetime.now()  # Record the end time
    duration = end_time - start_time

    # Create a dictionary with the desired structure
    output_data = {
        "timestamp_start": start_time.isoformat(),
        "timestamp_end": end_time.isoformat(),
        "duration_hhmmss": str(duration),
        "record_count": len(car_info_list),
        "records": car_info_list
    }

    # Generate a timestamp for the filename
    timestamp_str = start_time.strftime("%Y%m%d%H%M%S")

     # Create the 'json_data' folder if it doesn't exist
    json_data_folder = 'json_data'
    if not os.path.exists(json_data_folder):
        os.makedirs(json_data_folder)

    # Define the JSON file path including the 'json_data' folder
    json_filename = os.path.join(json_data_folder, f'car_records_{timestamp_str}.json')

    # Write the dictionary to a JSON file with the timestamp-appended filename
    with open(json_filename, 'w') as json_file:
        json.dump(output_data, json_file, indent=4)

    print(f"JSON data with timestamp and scrape duration written to {json_filename}")

    # Extract data from the 'records' field and convert it to a pandas DataFrame
    records_data = output_data["records"]
    records_df = pd.DataFrame(records_data)

     # Create the 'csv_data' folder if it doesn't exist
    csv_data_folder = 'csv_data'
    if not os.path.exists(csv_data_folder):
        os.makedirs(csv_data_folder)

    # Define the CSV file path including the 'csv_data' folder
    csv_filename = os.path.join(csv_data_folder, f'car_info_{timestamp_str}.csv')

    # Write the 'records' data to a CSV file with the timestamp-appended filename
    records_df.to_csv(csv_filename, index=False)

    print(f"CSV data from 'records' field written to {csv_filename}")

    return json_filename  # Return the generated JSON file path

if __name__ == "__main__":
    json_file_path = scraper()  # Call the scraper function and get the JSON file path

    create_db()

    insert_into_db(json_file_path)

    print("Database insertion script executed.")
