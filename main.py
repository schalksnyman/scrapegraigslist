from bs4 import BeautifulSoup
import requests
import lxml
import pandas as pd

base_url = "https://johannesburg.craigslist.org/search/sss?query=car&sort=rel"

# Send get HTTP request
page = requests.get(base_url)

# Verify we had a successful get request webpage call
if page.status_code == requests.codes.ok:

  # Get the whole webpage in beautiful soup format
  bs = BeautifulSoup(page.text, 'lxml')

  # Find the list of cars
  list_of_all_cars = bs.find('ul', class_='rows').find_all('li')

  # Hold the scraped data
  data = {
    'Date': [],
    'Price': [],
    'Title': []
  }

  # Scrape all cars in the results
  for car in list_of_all_cars:
    date = car.find('time', class_='result-date')['title']
    if date:
      data['Date'].append(date)
    else:
      data['Date'].append('none')
    price = car.find('span', class_='result-price').text
    if price:
      data['Price'].append(price)
    else:
      data['Price'].append('none')
    title = car.find('a', class_='result-title hdrlnk').text
    if title:
      data['Title'].append(title)
    else:
      data['Title'].append('none')

  table = pd.DataFrame(data, columns=['Date', 'Price', 'Title'])
  table.index = table.index + 1
  print(table)
  table.to_csv('joburg_cars_on_graigslist.csv', sep=',', index=False, encoding='utf-8')
