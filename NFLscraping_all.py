from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import time
from tqdm import tqdm

def scrape():
    # file path
    path = r'C:\Users\Raymond\PycharmProjects\fantasyFootball\data'

    # season
    year = 2018

    # category: passing, rushing, receiving, scrimmage, defense, kicking, returns, scoring, passing advanced,
    # rushing advanced, receiving advanced, defense advanced.
    # categories = ["passing", "rushing", "receiving", "scrimmage", "defense", "kicking", "returns", "scoring", "scoring",
    #               "passing_advanced", "rushing_advanced", "receiving_advanced", "defense_advanced"]
    categories = ["passing_advanced", "rushing_advanced", "receiving_advanced", "defense_advanced"]

    # category
    for category in categories:
        # season
        for year in tqdm(range(2018, 2019)):
            time.sleep(1)
            # url
            url = "https://www.pro-football-reference.com/years/{}/{}.htm".format(year, category)
            html = urlopen(url)
            soup = BeautifulSoup(html, features="html.parser")

            # category row
            row = 0
            if category in (
                    "rushing", "defense", "kicking", "scrimmage", "returns", "rushing_advanced", "defense_advanced"):
                row = 1
            headers = [th.getText() for th in soup.findAll('tr', limit=2)[row].findAll('th')]
            # exclude first column (rankings)
            headers = headers[1:]

            rows = soup.findAll('tr')[1:]
            player_stats = [[td.getText() for td in rows[i].findAll('td')]
                            for i in range(len(rows))]
            stats = pd.DataFrame(player_stats, columns=headers)
            # print(stats)
            stats.to_csv(path + "\\" + "{}-{}.csv ".format(category, year))


if __name__ == "__main__":
    scrape()
