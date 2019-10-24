from bs4 import BeautifulSoup
import requests
import pandas as pd


# def score(row1):
#     s = 0.0
#     # print(row1)
#     s += row1[('Passing', 'Yds')]/25.0
#     s += row1[('Passing', 'TD')]*4
#     s += row1[('Passing', 'Int')]*-2
#     s += row1[('Rushing', 'Yds')]/10.0
#     s += row1[('Rushing', 'TD')]*6
#     s += row1[('Scoring', '2PM')]*2
#     s += (row1[('Fumbles', 'Fmb')] - row1[('Fumbles', 'FR')])*-2
#     # s += row1[('Fumbles', 'TD')]*6
#     # print(s)
#     return s

url = 'https://www.pro-football-reference.com'
year = 2018
maxp = 10

# grab fantasy players
r = requests.get(url + '/years/' + str(year) + '/fantasy.htm')
soup = BeautifulSoup(r.content, 'html.parser')
parsed_table = soup.find_all('table')[0]

df = []

# first 2 rows are col headers
for i, row in enumerate(parsed_table.find_all('tr')[2:]):
    if i % 10 == 0: print(i, end=' ')
    if i >= maxp:
        print('\nComplete.')
        break

    # try:
    dat = row.find('td', attrs={'data-stat': 'player'})
    name = dat.a.get_text()
    stub = dat.a.get('href')
    stub1 = stub
    # stub = stub[:-4] + '/fantasy/' + str(year)
    stub = stub[:-4] + '/gamelog/' + str(year)
    pos = row.find('td', attrs={'data-stat': 'fantasy_pos'}).get_text()
    if pos != "QB":
        continue

    # grab this players stats
    tdf = pd.read_html(url + stub)[0]

    # Drop QB receives
    tdf = tdf.drop('Receiving', axis=1, level=0)
    # Drop last row
    tdf.drop(tdf.tail(1).index, inplace=True)
    tdf = tdf.fillna(0)
    # print(tdf.loc[:, [('Passing', 'Yds'), ('Passing', 'TD'), ('Passing', 'Int'), ('Rushing', 'Yds'), ('Rushing', 'TD'), ('Scoring', '2PM'), ('Fumbles', 'Fmb'), ('Rushing', 'FR'), ('Fumbles', 'TD')]])
    # tdf[('FPoints', 'FPoints')] = tdf.apply(lambda row1: score(row1), axis=1)

    stub1 = stub1[:-4] + '/fantasy/' + str(year)
    tdf1 = pd.read_html(url + stub1)[0]
    tdf1.columns = tdf1.columns.get_level_values(-1)
    tdf1 = tdf1.iloc[:, [-3]]

    tdf['FPoints'] = tdf1
    tdf['Name'] = name
    tdf['Position'] = pos
    tdf['Season'] = year
    # print(tdf)

    df.append(tdf)
    # except:
    #     pass

df = pd.concat(df)
df.head()
df.to_csv('gamelog2018.csv')