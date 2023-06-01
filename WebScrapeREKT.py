"""
This script scrapes the the rekt.news leaderboard and creates an Excel file with the following fields
• Name (of exploit)
• Amount (hacked in USD)
• Date (of hack)
• Audit Status (either Unaudited or a list of audits)
• URL (rekt explanation)
"""

#1
# Import necessary libraries
import requests
from bs4 import BeautifulSoup
import csv


#2
# Create function to scrape the rekt.news leaderboard
def scrape_rekt_leaderboard(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all instances of the required data
    data_rows = soup.find_all('li')

    # Extract the data values
    extracted_data = []
    for row in data_rows:
        title_div = row.find('div', class_='leaderboard-row-title')
        details_div = row.find('div', class_='leaderboard-row-details')

        if title_div and details_div:
            name = title_div.a.text.strip()
            audit_status = title_div.span.text.strip()
            href = title_div.a['href']
            full_url = f'https://rekt.news{href}'

            details_text = details_div.text.strip()
            amount, date = details_text.split('|')

            amount = amount.strip().replace('$', '').replace(',', '')
            date = date.strip()

            extracted_data.append([name, amount, date, audit_status, full_url])

    return extracted_data


#3
# Create function to export the data into a CSV
def save_to_csv(data, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Name', 'Amount', 'Date', 'Audit Status', 'URL'])

        for row in data:
            writer.writerow(row)
            

#4
# Define variables used in functions
url = 'https://rekt.news/leaderboard/'
data = scrape_rekt_leaderboard(url)

# Save the data to a CSV file
csv_filename = 'rekt_leaderboard.csv'
save_to_csv(data, csv_filename)

print(f'Data saved to {csv_filename}')
