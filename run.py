from nhl_scraper import *


scraper = NHLScraper()

print('Welcome to the NHL Scraper! Here are some options:')

while True:

    print('''
        1) Retrieve current statistics for a particular player.
        2) Retrieve the stats of all players matching a regex.
        3) Retrieve the top 10 scorers in the NHL right now.
        4) Retrieve the top 10 scorers in the NHL right now,
            from a certain country.''')

    user_option = input('\nEnter (1,2,3, or 4): ')

    if (user_option != '1' and user_option != '2' and user_option != '3' and user_option != '4'):
        print('\nPlease enter a number (1 through 4): ')

    scraper.initialize_player_info()

    if (user_option == '1'):
        print('\nYou have selected option 1: Retrieve current statistics for a particular player.')
        user_player_name = input('Enter the name of the player: ')

        try:
            scraper.get_player_stats(user_player_name)
        except:
            print('Not among currently active players.')
        break

    elif (user_option == '2'):
        print('\nYou have selected option 2: Retrieve the stats of all players matching a regex.')
        user_regex = input('Enter the desired regular expression: ')

        player_regex_list = list()

        user_regex_player = Player()
        player_regex_list = user_regex_player.get_players_stats_regex(user_regex)

        for p in player_regex_list:
            scraper.get_player_stats(p)

        break

    # elif (user_option == '3'):
    #     print('\nYou have selected option 3: Retrieve the top 10 scorers in the NHL right now.')
    # elif (user_option == '4'):
    #     print('''\nYou have selected option 4: Retrieve the top 10 scorers in the NHL right now,
    #                                 from a certain country.''')
