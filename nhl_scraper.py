import urllib.request, urllib.parse, urllib.error
import json
import ssl

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

teams_url = 'https://statsapi.web.nhl.com/api/v1/teams/'

class NHLScraper:

    def get_player_stats(self):
        place_holder = 'Zelda'
        return place_holder

    def get_all_player_ids(self):

        connection_1 = urllib.request.urlopen(teams_url, context=ctx)
        html = connection_1.read()
        data = html.decode()
        js = json.loads(data)

        roster_url_list = list()

        for team_id in js['teams']:
            roster_url_list.append(teams_url + str(team_id['id']) + '/roster')

        player_id_name_list = list()
        players_per_team_list = list()

        for team_page in roster_url_list:

            connection_2 = urllib.request.urlopen(team_page, context=ctx)
            html_2 = connection_2.read()
            data_2 = html_2.decode()
            team_roster_js = json.loads(data_2)

            players_per_team = 0
            for player in team_roster_js['roster']:
                player_id_name_list.append((player['person']['id'], player['person']['fullName']))
                players_per_team += 1
            players_per_team_list.append(players_per_team)

        print(len(player_id_name_list))
        print(sum(players_per_team_list))
