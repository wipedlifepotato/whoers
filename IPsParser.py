import sqlite3
import geoip2.database

def create_table(cursor):
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ip_port_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ip TEXT NOT NULL,
            port INTEGER NOT NULL,
            country TEXT,
            city TEXT
        )
    ''')
    # Ensure an index on the combination of IP and PORT for faster lookup
    cursor.execute('CREATE UNIQUE INDEX IF NOT EXISTS idx_ip_port ON ip_port_data (ip, port)')

def read_file_and_insert_into_db(file_path, cursor, geoip_reader):
    with open(file_path, 'r') as file:
        for line in file:
            try:
                ip, port = line.strip().split(':')
                response = geoip_reader.city(ip)
                country = response.country.name
                city = response.city.name
                cursor.execute('INSERT OR IGNORE INTO ip_port_data (ip, port, country, city) VALUES (?, ?, ?, ?)',
                               (ip, int(port), country, city))
            except ValueError:
                print(f"Skipping invalid line: {line.strip()}")
            except Exception as e:
                print(f"Error processing IP {ip}: {str(e)}")

def parse(file_path):
    #file_path = f #= 'your_file.txt'  # Replace with the actual path to your .txt file
    db_path = 'ip_port_database.db'
    geoip_database_path = './GeoLite2-City.mmdb'  # Replace with the actual path to the GeoIP database

    # Connect to SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create table if it doesn't exist
    create_table(cursor)

    # Open GeoIP database
    geoip_reader = geoip2.database.Reader(geoip_database_path)

    # Read the file and insert data into the database
    read_file_and_insert_into_db(file_path, cursor, geoip_reader)

    # Commit changes and close the connection
    conn.commit()
    conn.close()

    # Close GeoIP reader
    geoip_reader.close()

if __name__ == "__main__":
    parse('ips.txt')

