from urllib.request import urlopen
import urllib.parse, urllib.error
import json
import ssl

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

teams_url = 'https://statsapi.web.nhl.com/api/v1/teams/'

class NHLScraper:
    all_players = dict()
    all_p_list = list()


    def get_player_stats(self):
        place_holder = 'Zelda'
        return place_holder

    def initialize_player_info(self):

        team_data = urlopen(teams_url, context=ctx).read().decode()
        allteams_js = json.loads(team_data)

        player_id_name_list = list()
        players_per_team_list = list()


        players_id_name_dict = dict()
        list_id_name = list()

        for team_id in allteams_js['teams']:

            roster_url = teams_url + str(team_id['id']) + '/roster'
            roster_data = urlopen(roster_url, context=ctx).read().decode()
            team_roster_js = json.loads(roster_data)

            # players_per_team = 0
            for player in team_roster_js['roster']:
                players_id_name_dict[player['person']['id']] = player['person']['fullName']
                # players_per_team += 1
                p = Player(player['person']['id'], player['person']['fullName'])
                self.all_players[(player['person']['fullName'], player['person']['id'])] = p
                # if player['person']['id'] not in self.all_players:
                #     print(player['person']['fullName'])

        print(self.all_players)

            # players_per_team = 0
        #     for player in team_roster_js['roster']:
        #         player_id_name_list.append((player['person']['id'], player['person']['fullName']))
        #         p2 = Player(player['person']['id'], player['person']['fullName'])
        #         self.all_p_list.append(((player['person']['fullName'], player['person']['id']), p2))
        #     #     players_per_team += 1
        #     # players_per_team_list.append(players_per_team)
        # print(len(players_id_name_dict))
        # print(len(self.all_players))
        # print('*******************************')
        # print(len(player_id_name_list))
        # print(len(self.all_p_list))
        # print('*******************************')
        # all_p_dict = dict(self.all_p_list)
        # print(len(all_p_dict))

            # players_per_team2 = 0
            # for player in team_roster_js['roster']:
            #     p = Player(player['person']['id'], player['person']['fullName'])
            #     self.all_players[player['person']['fullName']] = p
            #     players_per_team2 += 1
            #
            # players_per_team_list.append(players_per_team2)


            #     print(self.all_players)
            #     print(self.all_players[player['person']['fullName']].player_id)
            #     print(self.all_players[player['person']['fullName']].player_name)
            #     print(self.all_players[player['person']['fullName']].points)
            #     break
            # break

class Player:

    player_id = int()
    player_name = str()
    points = 0
    goals = 0
    assists = 0
    shots = 0
    games = 0

    def __init__(self, p_id, p_name):
        self.player_id = p_id
        self.player_name = p_name
        # print(self.player_id, 'is constructed')
        # print(self.player_name, 'is constructed')
