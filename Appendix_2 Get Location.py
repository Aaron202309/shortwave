import pandas as pd
import requests
from bs4 import BeautifulSoup
import re

# Read the Excel file
data = pd.read_csv('station.csv')

# Get the station ID column data
ids = data['x']

# Create empty lists to store latitude and longitude values
latitudes = []
longitudes = []

# Loop through station IDs
for station_id in ids:
    # Build the website URL
    url = f'https://www.qrzcq.com/call/{station_id}'
    # print(url)
    
    # Send an HTTP request to the website
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Locate the <table> element with id="haminfomap"
    img_element = soup.find(id='haminfomap')

    # Regular expression pattern to extract latitude and longitude information
    pattern = r'markers=(-?\d+\.\d+),(-?\d+\.\d+)'

    # Get the HTML content of the img element
    img_html = str(img_element)

    # Use regular expression to match latitude and longitude information
    match = re.search(pattern, img_html)

    # Extract latitude and longitude information
    if match:
        latitude = match.group(1)
        longitude = match.group(2)
        latitudes.append(latitude)
        longitudes.append(longitude)
    else:
        # If latitude and longitude information not found, add None to the lists
        latitudes.append(None)
        longitudes.append(None)
        print("Not found: ", station_id)

# Add new columns for latitude and longitude to the DataFrame
data['Latitude'] = latitudes
data['Longitude'] = longitudes

# Write the updated DataFrame back to the Excel file
data.to_excel('Appendix_3 Update Station Location.xlsx', index=False)

print("Latitude and Longitude information added to file.")
