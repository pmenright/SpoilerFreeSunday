import os
import requests
from bs4 import BeautifulSoup
import csv
import datetime

# Constants for cell indices (magic numbers)
DRIVER_CELL_INDICES = [0, 1, 2, 3, 4]
CONSTRUCTOR_CELL_INDICES = [0, 1, 2]
RACE_CELL_INDICES = [0, 1, 2, 3, 5]

# Get the current year
current_year = datetime.datetime.now().year

# URLs with dynamic year
driver_url = f'https://www.formula1.com/en/results/{current_year}/drivers'
constructor_url = f'https://www.formula1.com/en/results/{current_year}/team'
race_url = f'https://www.formula1.com/en/results/{current_year}/races'

def scrape_and_write_csv(url, filename, headers, cell_indices):
    """
    Scrapes a table from the given URL and writes it to a CSV file.

    :param url: URL of the webpage to scrape.
    :param filename: Name of the CSV file to save the data.
    :param headers: List of headers for the CSV file.
    :param cell_indices: List of indices to extract data from the table's cells.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an exception for HTTP errors
    except requests.exceptions.RequestException as e:
        print(f"Failed to retrieve URL: {url}, Error: {e}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table', class_='f1-table-with-data')
    if table is None:
        print(f"Error: Could not find the table with class 'f1-table-with-data' on {url}")
        return

    rows = table.find_all('tr')
    
    try:
        with open(filename, 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(headers)
            for row in rows:
                cells = row.find_all('td')
                if len(cells) > 0:
                    row_data = [cells[i].text.strip() if i < len(cells) else '' for i in cell_indices]
                    csvwriter.writerow(row_data)
        print(f'{filename} has been exported.')
    except IOError as e:
        print(f"Error writing to file {filename}: {e}")

# Define tasks
tasks = [
    (driver_url, 'driver_standings.csv', ['Position', 'Driver', 'Nationality', 'Team', 'Points'], DRIVER_CELL_INDICES),
    (constructor_url, 'constructor_standings.csv', ['Position', 'Constructor', 'Points'], CONSTRUCTOR_CELL_INDICES),
    (race_url, 'race_results.csv', ['Race', 'Date', 'Winner', 'Constructor', 'Time'], RACE_CELL_INDICES)
]

# Execute scraping tasks
for task in tasks:
    scrape_and_write_csv(*task)

# Load race results to count entries
race_results = []
try:
    with open('race_results.csv', 'r') as race_file:
        csvreader = csv.reader(race_file)
        race_results = list(csvreader)
        print(f"Total races recorded: {len(race_results) - 1}")  # Exclude header row
except FileNotFoundError:
    print("race_results.csv file not found.")
except IOError as e:
    print(f"Error reading file race_results.csv: {e}")


# Count the number of races
round_number = len(race_results) + 1

# Load season schedule
season_schedule = []
try:

# /mnt/data/seasonSchedule.csv

    with open('seasonSchedule.csv', 'r') as schedule_file:
        csvreader = csv.reader(schedule_file)
        next(csvreader)  # Skip header
        for row in csvreader:
            season_schedule.append(row)
except Exception as e:
    print(f'Error loading seasonSchedule.csv: {e}')

# Determine next race location
try:
    next_race_location = season_schedule[round_number - 1][1]  # Assuming the location is in the second column
    with open('next_race.txt', 'w') as next_race_file:
        next_race_file.write(next_race_location)
    print('Next race information has been exported to next_race.txt')
except Exception as e:
    print(f'Error determining next race location: {e}')

# Write timestamp
timestamp = datetime.datetime.now().strftime('%d %b %Y, %H:%M:%S')
try:
    with open('timestamp.txt', 'w') as timestamp_file:
        timestamp_file.write(timestamp)
    print('Timestamp has been exported to timestamp.txt')
except Exception as e:
    print(f'Error writing timestamp.txt: {e}')
