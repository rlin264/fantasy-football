from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import requests

# file path
path = r'C:\Users\Raymond\PycharmProjects\fantasyFootball\data'

# season
year = 2018

# category: passing, rushing, receiving, scrimmage, defense, kicking, returns, scoring, passing advanced,
# rushing advanced, receiving advanced, defense advanced.
category = "defense_advanced"
# url
url = "https://www.pro-football-reference.com/years/{}/{}.htm".format(year, category)
# print(requests.get( url).status_code)
html = urlopen(url)
soup = BeautifulSoup(html, features="html.parser")
# use findALL() to get the column headers

print(url)
# print(soup)

print()

headers = [th.getText() for th in soup.findAll('tr')[1].findAll('th')]
# exclude first column (rankings)
headers = headers[1:]
print(headers)
rows = soup.findAll('tr')[1:]
player_stats = [[td.getText() for td in rows[i].findAll('td')]
                for i in range(len(rows))]
stats = pd.DataFrame(player_stats, columns=headers)
print(stats)
stats.to_csv(path + "{}-{}.csv ".format(category, year))
