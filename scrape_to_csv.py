import requests
from bs4 import BeautifulSoup as bs
import pymysql as mysql
import pandas as pd
from secrets import *
def madness_scraping():
	bball_data = []
	cols_type = ['Year int', 'Rank int', 'Team varchar(32)', 'Conf varchar(10)', 'Win_Loss varchar(10)', 'Eff_Margin float', 'Off_Eff float', 'Rank_Off_Eff int', 'Def_Eff float', 'Rank_Def_Eff int', 'Tempo float', 'Rank_Tempo int', 'Luck float', 'Rank_Luck int', 'sos float', 'Rank_SOS int', 'Avg_Opp_Off_Eff float', 'Rank_Off_Eff int', 'Avg_Opp_Def_Eff float', 'Rank_Opp_Def_Eff int', 'Non_Conf_SOS float', 'Rank_NonConf_SOS int']
	cols = ['Year', 'Rank', 'Team', 'Conf', 'Win_Loss', 'Eff_Margin', 'Off_Eff', 'Rank_Off_Eff', 'Def_Eff', 'Rank_Def_Eff', 'Tempo', 'Rank_Tempo', 'Luck', 'Rank_Luck', 'SOS', 'Rank_SOS', 'Avg_Opp_Off_Eff', 'Rank_Off_Eff', 'Avg_Opp_Def_Eff', 'Rank_Opp_Def_Eff', 'Non_Conf_SOS', 'Rank_NonConf_SOS']
	website = 'https://kenpom.com/'
	r = requests.get(website)
	links = bs(r.content, 'lxml').find('div', {'id': 'content-header'}).find('span', {'class': 'rank'}).findAll('a')
	links = links[1:-1]
	url_list = []
	for link in links:
		url_list.append(website + link.attrs.get('href'))
	url_list.append(website + 'index.php')

	for url in url_list:
		r = requests.get(url)
		soup = bs(r.content, 'lxml')
		year = soup.find('div', {'id': 'content-header'}).find('h2').text[:4]
		data_tables = soup.find('table', {'id': 'ratings-table'}).findAll('tbody')

		for table in data_tables:
			teams = table.findAll('tr')

			for team in teams:
				stats = team.findAll('td')
				team_data = [year]

				for stat in stats:
					stat_links = stat.findAll('a')
					if len(stat_links):
						stat = stat_links[0]
					stat_text = stat.text.replace('+', '')
					team_data.append(stat_text)

				if len(team_data) > 1:
					bball_data.append(team_data)
		
		print('Scrape complete for ' + year)
	df = pd.DataFrame(bball_data, columns=cols)
	
	return df, cols, cols_type


df, cols, col_types = madness_scraping()

df.to_csv('../data/Master.csv', index=False)