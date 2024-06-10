import os
import requests
from bs4 import BeautifulSoup
import csv
import datetime

# Define URLs
driver_url = 'https://www.formula1.com/en/results.html/2024/drivers.html'
constructor_url = 'https://www.formula1.com/en/results.html/2024/team.html'
race_url = 'https://www.formula1.com/en/results.html/2024/races.html'

# Function to scrape and write CSV
def scrape_and_write_csv(url, filename, headers):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table', class_='resultsarchive-table')
    rows = table.find_all('tr')
    
    with open(filename, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(headers)
        for row in rows:
            cells = row.find_all('td')
            if len(cells) > 0:
                csvwriter.writerow([cell.text.strip() for cell in cells[:len(headers)]])
    print(f'{filename} has been exported.')

# Scrape and write driver standings
scrape_and_write_csv(driver_url, 'driver_standings.csv', ['Position', 'Driver', 'Origin', 'Points'])

# Scrape and write constructor standings
scrape_and_write_csv(constructor_url, 'constructor_standings.csv', ['Position', 'Constructor', 'Points'])

# Scrape and write race results
scrape_and_write_csv(race_url, 'race_results.csv', ['Race', 'Date', 'Winner', 'Constructor', 'Laps', 'Time'])

# Load season schedule
season_schedule = []
try:
    with open('seasonSchedule.csv', 'r') as schedule_file:
        csvreader = csv.reader(schedule_file)
        next(csvreader)  # Skip header
        for row in csvreader:
            season_schedule.append(row)
except Exception as e:
    print(f'Error loading seasonSchedule.csv: {e}')

# Determine next race round
try:
    with open('race_results.csv', 'r') as race_results_file:
        csvreader = csv.reader(race_results_file)
        next(csvreader)  # Skip header
        race_results_count = sum(1 for _ in csvreader)
    next_round = race_results_count + 1
    next_race_location = season_schedule[next_round - 1][1]  # Assuming the location is in the second column
except Exception as e:
    print(f'Error processing race_results.csv or seasonSchedule.csv: {e}')
    next_race_location = "Unknown"

# Write next race info to file
try:
    with open('next_race.txt', 'w') as next_race_file:
        next_race_file.write(next_race_location)
    print('Next race information has been exported to next_race.txt')
except Exception as e:
    print(f'Error writing next_race.txt: {e}')

# Write timestamp
timestamp = datetime.datetime.now().strftime('%d %b %Y, %H:%M:%S')
try:
    with open('timestamp.txt', 'w') as timestamp_file:
        timestamp_file.write(timestamp)
    print('Timestamp has been exported to timestamp.txt')
except Exception as e:
    print(f'Error writing timestamp.txt: {e}')
