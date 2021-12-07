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
    if (user_option != '1' or user_option != '2' or user_option != '3' or user_option != '4'):
        print('\nPlease enter a number (1 through 4): ')

    if (user_option == '1'):
        print('\nYou have selected option 1: Retrieve current statistics for a particular player.')
        print(scraper.get_player_stats())
        print(NHLScraper.get_player_stats(scraper))
        scraper.get_all_player_ids()
        break

    # elif (user_option == '2'):
    #     print('\nYou have selected option 2: Retrieve the stats of all players matching a regex.')
    # elif (user_option == '3'):
    #     print('\nYou have selected option 3: Retrieve the top 10 scorers in the NHL right now.')
    # elif (user_option == '4'):
    #     print('''\nYou have selected option 4: Retrieve the top 10 scorers in the NHL right now,
    #                                 from a certain country.''')
