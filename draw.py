import sqlite3
from mpl_toolkits.basemap import Basemap
from tqdm import tqdm
from geoip2.database import Reader
import matplotlib.pyplot as plt

# Connect to the SQLite database
conn = sqlite3.connect('ip_port_database.db')
cursor = conn.cursor()

# Execute a query to fetch data
cursor.execute("SELECT * FROM ip_port_data")
data = cursor.fetchall()

# Read IP geolocation from the local GeoLite2-City database
latitudes, longitudes = [], []

#counter = 0
with Reader('GeoLite2-City.mmdb') as reader:
    for row in tqdm(data, desc="Geocoding", unit="row"):
        try:
            response = reader.city(row[1])
            lat = response.location.latitude
            lon = response.location.longitude

            # Check if lat and lon are valid numbers
            if isinstance(lat, (int, float)) and isinstance(lon, (int, float)):
                latitudes.append(lat)
                longitudes.append(lon)
            else:
                print(f"Invalid coordinates for IP {row[1]}: Latitude={lat}, Longitude={lon}")
        except Exception as e:
            print(f"Error geocoding IP {row[1]}: {e}")
#        counter += 1
#        if counter > 10:
#            break

# Plot the points on the world map
fig = plt.figure(figsize=(12, 8))
m = Basemap(projection='mill', llcrnrlat=-60, urcrnrlat=90, llcrnrlon=-180, urcrnrlon=180, resolution='c')
m.drawcoastlines()
m.drawcountries()
m.scatter(longitudes, latitudes, latlon=True, marker='o', color='blue', alpha=0.7)

# Save the map as a PNG file
plt.title('IP Locations on World Map')
plt.savefig('static/world_map.png')
#plt.show()

# Close the connection to the database
conn.close()

