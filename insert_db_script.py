import sys
import sqlite3
import json

def insert_into_db(json_file_path):
    # Create or connect to the SQLite database
    conn = sqlite3.connect('car_data.db')
    cursor = conn.cursor()

    # Read the JSON data from the file
    with open(json_file_path, 'r') as json_file:
        data = json.load(json_file)

    # Extract the records list from the JSON data
    records = data.get('records', [])

    # Loop through the records and insert or update them in the Cars table
    scrape_timestamp = data.get('timestamp_start', '')

    for record in records:
        car_id = record['id']

        # Check if a record with the same id exists in the database
        cursor.execute('SELECT * FROM Cars WHERE id = ?', (car_id,))
        existing_record = cursor.fetchone()

        if existing_record:
            # Update the existing record with new data
            cursor.execute('''
            UPDATE Cars
            SET scrape_timestamp = ?, updated_at = ?, name = ?, price = ?, mileage = ?, annual_insurance = ?, availability = ?, condition = ?
            WHERE id = ?;
            ''', (scrape_timestamp, record['updated_at'], record['name'], record['price'], record['mileage'], record['annual_insurance'], record['availability'], record['condition'], car_id))
        else:
           # Insert the new record into the database
            cursor.execute('''
            INSERT INTO Cars (id, scrape_timestamp, created_at, updated_at, model, make, name, description, price_currency, price, body_type, source, current_location, drive, mileage, mileage_unit, color, annual_insurance_currency, annual_insurance, year_of_manufacture, thumbnail, availability, purchase_status, condition, duty_and_clearance_fee_currency, duty_and_clearance_fee, estimated_arrival_days, is_published, slug, agent_whatsapp_contact)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
            ''', (car_id, scrape_timestamp, record['created_at'], record['updated_at'], record['model']['name'], record['model']['make']['name'], record['name'], record['description'], record['price_currency'], record['price'], record['body_type'], record['source'], record['current_location'], record['drive'], record['mileage'], record['mileage_unit'], record['color'], record['annual_insurance_currency'], record['annual_insurance'], record['year_of_manufacture'], record['thumbnail'], record['availability'], record['purchase_status'], record['condition'], record['duty_and_clearance_fee_currency'], record['duty_and_clearance_fee'], record['estimated_arrival_days'], record['is_published'], record['slug'], record['agent_whatsapp_contact']))

            # # Insert the new record into the database
            # cursor.execute('''
            # INSERT INTO Cars (id, scrape_timestamp, created_at, updated_at, name, description, price_currency, price, body_type, source, current_location, drive, mileage, mileage_unit, color, annual_insurance_currency, annual_insurance, year_of_manufacture, thumbnail, availability, purchase_status, condition, duty_and_clearance_fee_currency, duty_and_clearance_fee, estimated_arrival_days, is_published, slug, agent_whatsapp_contact)
            # VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
            # ''', (car_id, scrape_timestamp, record['created_at'], record['updated_at'], record['name'], record['description'], record['price_currency'], record['price'], record['body_type'], record['source'], record['current_location'], record['drive'], record['mileage'], record['mileage_unit'], record['color'], record['annual_insurance_currency'], record['annual_insurance'], record['year_of_manufacture'], record['thumbnail'], record['availability'], record['purchase_status'], record['condition'], record['duty_and_clearance_fee_currency'], record['duty_and_clearance_fee'], record['estimated_arrival_days'], record['is_published'], record['slug'], record['agent_whatsapp_contact']))

        # Record historical price data
        cursor.execute('''
        INSERT INTO HistoricalPrices (car_id, price_currency, price, date)
        VALUES (?, ?, ?, ?);
        ''', (car_id, record['price_currency'], record['price'], scrape_timestamp))

        # Record historical annual insurance data
        cursor.execute('''
        INSERT INTO HistoricalAnnualInsurance (car_id, annual_insurance_currency, annual_insurance, date)
        VALUES (?, ?, ?, ?);
        ''', (car_id, record['annual_insurance_currency'], record['annual_insurance'], scrape_timestamp))

        # Record historical mileage data
        cursor.execute('''
        INSERT INTO HistoricalMileage (car_id, mileage, mileage_unit, date)
        VALUES (?, ?, ?, ?);
        ''', (car_id, record['mileage'], record['mileage_unit'], scrape_timestamp))

        # Record historical availability data
        cursor.execute('''
        INSERT INTO HistoricalAvailability (car_id, availability, date)
        VALUES (?, ?, ?);
        ''', (car_id, record['availability'], scrape_timestamp))

        # Record historical condition data
        cursor.execute('''
        INSERT INTO HistoricalCondition (car_id, condition, date)
        VALUES (?, ?, ?);
        ''', (car_id, record['condition'], scrape_timestamp))

    # Commit the changes and close the database connection
    conn.commit()
    conn.close()

    print("Data from JSON file inserted into the database.")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python insert_into_db.py <json_file_path>")
        sys.exit(1)

    json_file_path = sys.argv[1]  # Get the JSON file path from the command-line arguments
    insert_into_db(json_file_path)
