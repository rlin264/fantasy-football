from bs4 import BeautifulSoup
import requests
import pandas as pd

url = 'https://www.pro-football-reference.com'
path = r'C:\Users\Raymond\PycharmProjects\fantasyFootball\data'
maxp = 300

for j in range(2008,2019):
    year = j

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

        try:
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

            # get rid of MultiIndex, just keep last row

            # tdf.columns = tdf.columns.get_level_values(-1)
            # print(tdf)
            # tdf = tdf[tdf.line_race != "receiving"]

            # fix the away/home column
            # tdf = tdf.rename(columns={'Unnamed: 4_level_2': 'Away'})
            # tdf['Away'] = [1 if r == '@' else 0 for r in tdf['Away']]

            # Drop QB receives
            tdf = tdf.drop('Receiving', axis=1, level=0)
            # Drop last row
            tdf.drop(tdf.tail(1).index, inplace=True)
            # tdf['FPoints'] = tdf.apply(lambda row: row. + row.b, axis=1, level=2)
            tdf = tdf.fillna(0)
            # add other info
            stub1 = stub1[:-4] + '/fantasy/' + str(year)
            tdf1 = pd.read_html(url + stub1)[0]
            tdf1.columns = tdf1.columns.get_level_values(-1)
            tdf1 = tdf1.iloc[:, [-3]]

            tdf['FPoints'] = tdf1
            tdf['Name'] = name
            tdf['Position'] = pos
            tdf['Season'] = year

            df.append(tdf)
        except:
            pass

    df = pd.concat(df)
    df.head()
    df.to_csv(path + "\\"+'gamelog_QB_{}.csv'.format(year))
