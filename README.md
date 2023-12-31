# Kai & Karo Vehicle Scraper

This is a Python script for scraping vehicle information from the Kai & Karo website (https://www.kaiandkaro.com). The script retrieves data on various car makes and models and saves it in JSON and CSV formats. Additionally, it provides a database insertion script to store the data in a database. I have used SLite for this project just for simplicity and to allow the data to be accessed within the repository.

## Prerequisites

Before running the script, ensure that you have the following prerequisites installed:

- Python 3
- Required Python libraries (found within the requirements.txt file)

## Usage

1. Clone the repository or download the script to your local machine.

2. Open a terminal and navigate to the directory where the script is located.

3. Run the following command:

```
pip install -r requirements.txt
```

This will install all required Python packages necessary to run the scraper.

4. Run the script using the following command:

```
python scraper.py
```

This will initiate the scraping process. The script will retrieve data from the Kai & Karo website, save it in JSON and CSV formats, and insert it into a SQLite database.

5. After the script has finished executing, you will see the following messages:

- "JSON data with timestamp and scrape duration written to [JSON_FILE_PATH]" (indicating where the JSON file is saved).

- "CSV data from 'records' field written to [CSV_FILE_PATH]" (indicating where the CSV file is saved).

- "Database insertion script executed." (indicating that the data has been inserted into the database).

## Output Files

The script generates the following output files:

- **JSON Data File**: This file contains the scraped vehicle information in JSON format. The filename includes a timestamp. Example filename: _car_records_20230910120000.json_.

- **CSV Data File**: This file contains the scraped vehicle information in CSV format. The filename also includes a timestamp. Example filename: _car_info_20230910120000.csv_.

## Important Notes

- The script may take some time to run, depending on the amount of data to be scraped.
- Ensure that you have a stable internet connection while running the script to fetch data from the Kai & Karo website.
- The script can be customized and extended based on your specific requirements.

## License

This script is licensed under a [Creative Commons Attribution 4.0 International License](https://creativecommons.org/licenses/by/4.0/).

You are free to:

- Share: Copy and redistribute the material in any medium or format.
- Adapt: Remix, transform, and build upon the material for any purpose, even commercially.

Under the following terms:

- Attribution: You must give appropriate credit to the original author (e.g., provide a link to this script) and indicate if changes were made. You can do this in any reasonable manner, but not in any way that suggests the author endorses you or your use.

**Disclaimer:** This script is intended for educational and informational purposes only. Use it responsibly and in accordance with the terms of use of the Kai & Karo website. Be aware of the legal and ethical considerations related to web scraping.
