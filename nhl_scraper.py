from urllib.request import urlopen
import urllib.parse, urllib.error
import json
import ssl
import re

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

class NHLScraper:
    all_players = dict()
    all_p_list = list()
    players_id_name_dict = dict()

    def get_player_stats(self, user_player_name):

        for i, n in list(self.players_id_name_dict.items()):
            if(n == user_player_name):
                user_player_id = i
                break

        user_player_stats = self.all_players[(user_player_name, user_player_id)]
        player_position = user_player_stats.fetch_game_stats(user_player_id, user_player_name)

        if(player_position == False):
            print('\nNo stats amassed for the current season for', user_player_name, user_player_id)
        else:

            print('\nShowing player statistics for', user_player_name, user_player_id)

            if(player_position == 'G'):
                print('Wins:', user_player_stats.wins)
                print('Losses:', user_player_stats.losses)
                print('gAA:', user_player_stats.gAA)
                print('Shutouts', user_player_stats.shutouts)
                print('Games:', user_player_stats.games)
            else:
                print('Points:', user_player_stats.points)
                print('Goals:', user_player_stats.goals)
                print('Assists:', user_player_stats.assists)
                print('Shots:', user_player_stats.shots)
                print('Games:', user_player_stats.games)

    def initialize_player_info(self):

        print('\nLoading data, please wait...')

        teams_url = 'https://statsapi.web.nhl.com/api/v1/teams/'

        team_data = urlopen(teams_url, context=ctx).read().decode()
        allteams_js = json.loads(team_data)

        player_id_name_list = list()
        players_per_team_list = list()

        list_id_name = list()

        for team_id in allteams_js['teams']:

            roster_url = teams_url + str(team_id['id']) + '/roster'
            roster_data = urlopen(roster_url, context=ctx).read().decode()
            team_roster_js = json.loads(roster_data)

            for player in team_roster_js['roster']:
                self.players_id_name_dict[player['person']['id']] = player['person']['fullName']
                self.all_players[(player['person']['fullName'], player['person']['id'])] = Player()

            # print(list(self.players_id_name_dict.values()))
            # break
            # players_per_team = 0
        #     for player in team_roster_js['roster']:
        #         player_id_name_list.append((player['person']['id'], player['person']['fullName']))
        #         p2 = Player(player['person']['id'], player['person']['fullName'])
        #         self.all_p_list.append(((player['person']['fullName'], player['person']['id']), p2))
        #     #     players_per_team += 1
        #     # players_per_team_list.append(players_per_team)


            # players_per_team2 = 0
            # for player in team_roster_js['roster']:
            #     p = Player(player['person']['id'], player['person']['fullName'])
            #     self.all_players[player['person']['fullName']] = p
            #     players_per_team2 += 1
            #
            # players_per_team_list.append(players_per_team2)


class Player:

    player_id = int()
    player_name = str()

    position = str()

    # stats for skaters
    points = 0
    goals = 0
    assists = 0
    shots = 0
    games = 0

    # stats for goalies
    wins = 0
    losses = 0
    gAA = 0
    shutouts = 0
    games = 0


    # def __init__(self):
        # print('player constructed')
        # self.player_id = p_id
        # self.player_name = p_name
        # print(self.player_id, 'is constructed')
        # print(self.player_name, 'is constructed')

    def fetch_game_stats(self, p_id, p_name):
        self.player_id = p_id
        self.player_name = p_name

        player_url = 'https://statsapi.web.nhl.com/api/v1/people/' + str(self.player_id)
        player_data = urlopen(player_url, context=ctx).read().decode()
        player_js = json.loads(player_data)

        self.position = player_js['people'][0]['primaryPosition']['code']

        stats_url_part1 = 'https://statsapi.web.nhl.com/api/v1/'
        stats_url_part2 = '/stats?stats=statsSingleSeason&season=20212022'

        stats_url = stats_url_part1 + 'people/' + str(self.player_id) + stats_url_part2
        stats_data = urlopen(stats_url, context=ctx).read().decode()
        stats_js = json.loads(stats_data)

        if(stats_js['stats'][0]['splits'] == []):
            return False
        else:

            if(self.position == 'G'):
                self.wins = stats_js['stats'][0]['splits'][0]['stat']['wins']
                self.losses = stats_js['stats'][0]['splits'][0]['stat']['losses']
                self.gAA = stats_js['stats'][0]['splits'][0]['stat']['goalAgainstAverage']
                self.shutouts = stats_js['stats'][0]['splits'][0]['stat']['shutouts']
            else:
                self.points = stats_js['stats'][0]['splits'][0]['stat']['points']
                self.goals = stats_js['stats'][0]['splits'][0]['stat']['goals']
                self.assists = stats_js['stats'][0]['splits'][0]['stat']['assists']
                self.shots = stats_js['stats'][0]['splits'][0]['stat']['shots']

            self.games = stats_js['stats'][0]['splits'][0]['stat']['games']

            return self.position

    def get_players_stats_regex(self, regex):
        print(regex)

        p = NHLScraper()

        matching_regex = list()

        for i in list(p.players_id_name_dict.values()):
            if re.search(regex, i):
                matching_regex.append(i)

        return matching_regex
