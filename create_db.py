import sqlite3


def create_db():
    # Create or connect to the SQLite database
    conn = sqlite3.connect('car_data.db')
    cursor = conn.cursor()

    # Create the Cars table with the scrape_timestamp field
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Cars (
        id INTEGER PRIMARY KEY,
        created_at DATETIME,
        updated_at DATETIME,
        scrape_timestamp DATETIME,
        model TEXT,
        make TEXT,
        name TEXT,
        description TEXT,
        price_currency TEXT,
        price REAL,
        body_type TEXT,
        source TEXT,
        current_location TEXT,
        drive TEXT,
        mileage INTEGER,
        mileage_unit TEXT,
        color TEXT,
        annual_insurance_currency TEXT,
        annual_insurance REAL,
        year_of_manufacture INTEGER,
        thumbnail TEXT,
        availability TEXT,
        purchase_status TEXT,
        condition TEXT,
        duty_and_clearance_fee_currency TEXT,
        duty_and_clearance_fee REAL,
        estimated_arrival_days INTEGER,
        is_published BOOLEAN,
        slug TEXT,
        agent_whatsapp_contact TEXT
    );
    ''')


    # Create the CarModel table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS CarModel (
        id INTEGER PRIMARY KEY,
        car_id INTEGER,
        model_id INTEGER,
        name TEXT,
        FOREIGN KEY (car_id) REFERENCES Cars (id)
    );
    ''')

    # Create the CarMake table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS CarMake (
        id INTEGER PRIMARY KEY,
        model_id INTEGER,
        make_id INTEGER,
        name TEXT,
        FOREIGN KEY (model_id) REFERENCES CarModel (id)
    );
    ''')

    # Create the HistoricalPrices table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS HistoricalPrices (
        id INTEGER PRIMARY KEY,
        car_id INTEGER,
        price_currency TEXT,
        price REAL,
        date DATETIME,
        FOREIGN KEY (car_id) REFERENCES Cars (id)
    );
    ''')

    # Create the HistoricalMileage table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS HistoricalMileage (
        id INTEGER PRIMARY KEY,
        car_id INTEGER,
        mileage INTEGER,
        mileage_unit TEXT,
        date DATETIME,
        FOREIGN KEY (car_id) REFERENCES Cars (id)
    );
    ''')

    # Create the HistoricalAnnualInsurance table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS HistoricalAnnualInsurance (
        id INTEGER PRIMARY KEY,
        car_id INTEGER,
        annual_insurance_currency TEXT,
        annual_insurance REAL,
        date DATETIME,
        FOREIGN KEY (car_id) REFERENCES Cars (id)
    );
    ''')

    # Create the HistoricalAvailability table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS HistoricalAvailability (
        id INTEGER PRIMARY KEY,
        car_id INTEGER,
        availability TEXT,
        date DATETIME,
        FOREIGN KEY (car_id) REFERENCES Cars (id)
    );
    ''')

    # Create the HistoricalCondition table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS HistoricalCondition (
        id INTEGER PRIMARY KEY,
        car_id INTEGER,
        condition TEXT,
        date DATETIME,
        FOREIGN KEY (car_id) REFERENCES Cars (id)
    );
    ''')

    # Commit changes and close the database connection
    conn.commit()
    conn.close()

    print("Database and tables created successfully.")


if __name__ == "__main__":
    create_db()