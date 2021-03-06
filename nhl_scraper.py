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
    # all_p_list = list()
    players_id_name_dict = dict()

    all_p_goals = dict()

    def get_top_scorers(self, country):

        player_goals_list = list()

        p = Player()

        for p_name,p_id in (list(self.all_players.keys()))[:20]:
            p.fetch_game_stats(p_id, p_name)
            self.all_p_goals[(p_name, p_id)] = (p.goals, p.birth_country)

        for x,y in list(self.all_p_goals.items()):
            if(country == ''):
                player_goals_list.append((y[0], x[0]))
            elif(country == y[1]):
                player_goals_list.append((y[0], x[0]))

        player_goals_list.sort(reverse=True)

        if(country == ''):
            print('Showing top 10 goal scorers in the NHL for the 2021-2022 season:\n')
        elif(len(country) > 0):
            print('Showing top 10 goal scorers in the NHL from', country, 'for the 2021-2022 season:\n')

        for i in player_goals_list[:10]:
            print(i[1]+':',i[0])

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
            else:
                print('Points:', user_player_stats.points)
                print('Goals:', user_player_stats.goals)
                print('Assists:', user_player_stats.assists)
                print('Shots:', user_player_stats.shots)

            print('Games:', user_player_stats.games)
            print('Birth Country:', user_player_stats.birth_country)

    def initialize_player_info(self):

        print('\nLoading data, please wait\n')

        teams_url = 'https://statsapi.web.nhl.com/api/v1/teams/'

        team_data = urlopen(teams_url, context=ctx).read().decode()
        allteams_js = json.loads(team_data)

        for team_id in allteams_js['teams']:

            roster_url = teams_url + str(team_id['id']) + '/roster'
            roster_data = urlopen(roster_url, context=ctx).read().decode()
            team_roster_js = json.loads(roster_data)

            for player in team_roster_js['roster']:
                self.players_id_name_dict[player['person']['id']] = player['person']['fullName']
                self.all_players[(player['person']['fullName'], player['person']['id'])] = Player()

class Player:

    player_id = int()
    player_name = str()
    birth_country = str()
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

    # def __lt__(self, other):


    def fetch_game_stats(self, p_id, p_name):
        self.player_id = p_id
        self.player_name = p_name

        player_url = 'https://statsapi.web.nhl.com/api/v1/people/' + str(self.player_id)
        player_data = urlopen(player_url, context=ctx).read().decode()
        player_js = json.loads(player_data)

        self.position = player_js['people'][0]['primaryPosition']['code']
        self.birth_country = player_js['people'][0]['birthCountry']

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
        
        p = NHLScraper()

        matching_regex = list()

        for i in list(p.players_id_name_dict.values()):
            if re.search(regex, i):
                matching_regex.append(i)

        return matching_regex
