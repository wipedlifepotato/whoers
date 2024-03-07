import sqlite3
from mpl_toolkits.basemap import Basemap
from geopy.geocoders import Nominatim
import matplotlib.pyplot as plt
from tqdm import tqdm

# Connect to the SQLite database
conn = sqlite3.connect('ip_port_database.db')
cursor = conn.cursor()

# Execute a query to fetch data
cursor.execute("SELECT * FROM ip_port_data")
data = cursor.fetchall()

# Geocode cities to get latitude and longitude
latitudes, longitudes = [], []

counter = 0
geolocator = Nominatim(user_agent="my_geocoder")
for row in tqdm(data, desc="Geocoding", unit="row"):
    location = geolocator.geocode(f"{row[4]}, {row[3]}")
    if location:
        latitudes.append(location.latitude)
        longitudes.append(location.longitude)
    counter += 1
    if counter > 10: break
# Plot the points on the world map
fig = plt.figure(figsize=(12, 8))
m = Basemap(projection='mill', llcrnrlat=-60, urcrnrlat=90, llcrnrlon=-180, urcrnrlon=180, resolution='c')
m.drawcoastlines()
m.drawcountries()
m.scatter(longitudes, latitudes, latlon=True, marker='o', color='blue', alpha=0.7)

# Save the map as a PNG file
plt.title('IP Locations on World Map')
plt.savefig('world_map.png')
plt.show()

# Close the connection to the database
conn.close()

