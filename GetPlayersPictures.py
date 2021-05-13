import requests
from bs4 import BeautifulSoup as bs
import Toolbox as tool


def get_htlm(url):
    soup = bs(requests.get(url).content, "html.parser")
    return str(soup)


players_list = tool.sql_query_to_list('SELECT PlayersBios_PLAYER_ID FROM Players_with_type')
i = 1
for player_id in players_list:
    soup = get_htlm('https://www.nba.com/stats/player/' + player_id + '/')
    start = soup.find('https://ak')
    if start == -1:
        continue
    end = soup.find(player_id + '.png') + len(player_id + '.png')
    url_pic = soup[start:end]

    img_data = requests.get(url_pic).content
    with open('../Players Pictures/' + player_id + '.png', 'wb') as handler:
        handler.write(img_data)
    print(str(i) + '/' + str(len(players_list)))
    i += 1

print('All pictures of players who played this year have been successfully stolen')
