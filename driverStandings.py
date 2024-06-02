import requests
from bs4 import BeautifulSoup
import csv
import datetime

# URL of the website to scrape for driver standings
driver_url = 'https://www.formula1.com/en/results.html/2024/drivers.html'
# URL of the website to scrape for constructor standings
constructor_url = 'https://www.formula1.com/en/results.html/2024/team.html'
# URL of the website to scrape for race results
race_url = 'https://www.formula1.com/en/results.html/2024/races.html'

# Send a GET request to the driver standings URL
response_driver = requests.get(driver_url)
# Parse the HTML content of the driver standings page
soup_driver = BeautifulSoup(response_driver.text, 'html.parser')
# Find the table containing the driver standings
driver_table = soup_driver.find('table', class_='resultsarchive-table')
# Find all rows in the driver standings table
driver_rows = driver_table.find_all('tr')

# Send a GET request to the constructor standings URL
response_constructor = requests.get(constructor_url)
# Parse the HTML content of the constructor standings page
soup_constructor = BeautifulSoup(response_constructor.text, 'html.parser')
# Find the table containing the constructor standings
constructor_table = soup_constructor.find('table', class_='resultsarchive-table')
# Find all rows in the constructor standings table
constructor_rows = constructor_table.find_all('tr')

# Send a GET request to the race results URL
response_race = requests.get(race_url)
# Parse the HTML content of the race results page
soup_race = BeautifulSoup(response_race.text, 'html.parser')
# Find the table containing the race results
race_table = soup_race.find('table', class_='resultsarchive-table')
# Find all rows in the race results table
race_rows = race_table.find_all('tr')

# Create and open a CSV file to write the driver standings data
with open('driver_standings.csv', 'w', newline='') as driver_csvfile:
    driver_csvwriter = csv.writer(driver_csvfile)
    driver_csvwriter.writerow(['Position', 'Driver', 'Origin', 'Points'])  # Write the header row
    # Write driver standings data to CSV
    for row in driver_rows:
        cells = row.find_all('td')
        if len(cells) > 0:
            position = cells[1].text.strip()
            driver_name = cells[2].text.strip()
            origin = cells[3].text.strip()
            points = cells[5].text.strip()
            driver_csvwriter.writerow([position, driver_name, origin, points])
print('Driver standings data has been exported to driver_standings.csv')

# Create and open a CSV file to write the constructor standings data
with open('constructor_standings.csv', 'w', newline='') as constructor_csvfile:
    constructor_csvwriter = csv.writer(constructor_csvfile)
    constructor_csvwriter.writerow(['Position', 'Constructor', 'Points'])  # Write the header row
    # Write constructor standings data to CSV
    for row in constructor_rows:
        cells = row.find_all('td')
        if len(cells) > 0:
            position = cells[1].text.strip()
            constructor_name = cells[2].text.strip()
            points = cells[3].text.strip()
            constructor_csvwriter.writerow([position, constructor_name, points])
print('Constructor standings data has been exported to constructor_standings.csv')

# Create and open a CSV file to write the race results data
with open('race_results.csv', 'w', newline='') as race_csvfile:
    race_csvwriter = csv.writer(race_csvfile)
    race_csvwriter.writerow(['Race', 'Date', 'Winner', 'Constructor', 'Laps', 'Time'])  # Write the header row
    # Write race results data to CSV
    for row in race_rows:
        cells = row.find_all('td')
        if len(cells) > 0:
            grand_prix = cells[1].text.strip()
            date = cells[2].text.strip()
            winner = cells[3].text.strip()
            constructor = cells[4].text.strip()
            laps = cells[5].text.strip()
            time = cells[6].text.strip()
            race_csvwriter.writerow([grand_prix, date, winner, constructor, laps, time])
print('Race results data has been exported to race_results.csv')

# Create and open a .txt file to write the timestamp
timestamp = datetime.datetime.now().strftime('%d %b %Y, %H:%M:%S')
with open('timestamp.txt', 'w') as timestamp_file:
    timestamp_file.write(timestamp)

print('Timestamp has been exported to timestamp.txt')