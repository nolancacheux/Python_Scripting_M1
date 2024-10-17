import requests
from bs4 import BeautifulSoup

# URL of Geoffrey Hinton's Wikipedia page
url = "https://en.wikipedia.org/wiki/Geoffrey_Hinton"

# Send a GET request to the URL
response = requests.get(url)

# Parse the HTML content of the page
soup = BeautifulSoup(response.content, 'html.parser')

# Extract the title of the page
title = soup.find('h1', {'id': 'firstHeading'}).text
print(f"Title: {title}")

# Extract the first paragraph of the page
first_paragraph = soup.find('p').text
print(f"First paragraph: {first_paragraph}")

# Extract all the headings in the page
headings = soup.find_all(['h2', 'h3'])
for heading in headings:
    print(f"Heading: {heading.text.strip()}")

# Save the entire page content to a file
with open('geoffrey_hinton_wikipedia.html', 'w', encoding='utf-8') as file:
    file.write(soup.prettify())