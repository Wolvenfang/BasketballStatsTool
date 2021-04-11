import constants
import copy
import os


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def menu():
    commands = ["Display Team Stats", "Help", "Quit"]
    for index, item in enumerate(commands, start=1):
        print("{}) {}".format(index, item))
    print()


def team_menu():
    for index, item in enumerate(constants.TEAMS, start=1):
        print("{}) {}".format(index, item))
    print()


def welcome():
    app_name = "BASKETBALL TEAM STATS TOOL"
    print("•" * len(app_name))
    print(app_name)
    print("•" * len(app_name), end="\n\n\n")
    print("◉" * 10, "MENU", "◉" * 10, end="\n\n")


class TeamStats:
    def __init__(self, team_name, players):
        self.team_name = team_name
        self.players = players

    def __str__(self):
        player_name_list = []
        guardian_name_list = []
        total_team_height = 0
        for team_player in self.players:
            player_name_list.append(team_player.name)
            for guardian in team_player.guardians:
                guardian_name_list.append(guardian)
            total_team_height += team_player.height

        comma = ', '
        return "Team Name: {0}\nPlayer Count: {1}\nHeight Average: {2}\nPlayers: {3}\nGuardians: {4}" \
            .format(self.team_name,
                    str(len(self.players)),
                    total_team_height / len(self.players),
                    comma.join(player_name_list),
                    comma.join(guardian_name_list))


class Player:
    def __init__(self, player_name, player_guardians, player_experience, player_height):
        self.name = player_name
        self.guardians = player_guardians
        self.experience = player_experience
        self.height = player_height

    def __str__(self):
        return "Player name: {0}\nIs experienced: {1}\nHeight: {2}\nGuardians: {3}\n" \
            .format(self.name,
                    str(self.experience),
                    str(self.height),
                    self.guardians)


def to_boolean(str1):
    if str1 == "YES":
        return True
    return False


def to_int_height(str1):
    result = ""
    for character in str1:
        if character.isnumeric():
            result = result + character

    return int(result)


def deep_clone_players(players):
    players_clone = []
    for player in players:
        player = Player(player['name'],
                        player['guardians'].split(" and "),
                        to_boolean(player['experience']),
                        to_int_height(player['height']))
        players_clone.append(player)
    return players_clone


# The first item are experienced players and the second are the inexperienced players.
def get_players_for_team(num_players_team, div_player_exp):
    result = []
    take_exp = True
    i = 0
    while i != num_players_team:
        if take_exp:
            result.append(div_player_exp[0].pop())
            take_exp = False
            i += 1
        else:
            result.append(div_player_exp[1].pop())
            take_exp = True
            i += 1
    return result


def balance_teams(teams, players):
    num_players_team = len(players) / len(teams)
    div_player_exp = [[], []]  # The first item are experienced players and the second are the inexperienced players.
    for player_of_team in players:
        if player_of_team.experience:
            div_player_exp[0].append(player_of_team)
        else:
            div_player_exp[1].append(player_of_team)

    result = []
    for item in teams:
        player_of_teams = get_players_for_team(num_players_team, div_player_exp)
        team_stats = TeamStats(item, player_of_teams)
        result.append(team_stats)

    return result


def display_team(index, teams):
    print(teams[int(index) - 1])


def main():
    teams = copy.deepcopy(constants.TEAMS)
    all_players = deep_clone_players(constants.PLAYERS)
    team_results = balance_teams(teams, all_players)

    while True:
        menu()
        command = input("Please enter the number for the COMMAND that you want >   ")
        print()
        if command == '1':
            team_menu()
            invalid_option = True
            option = input("Please enter the number for the OPTION that you want >   ")
            while invalid_option:
                try:
                    if 1 <= int(option) <= len(teams):
                        invalid_option = False
                    else:
                        print("Invalid Option")
                        option = input("Please enter the number for the OPTION that you want >   ")
                except ValueError:
                    print("That isn't a valid number. Please try again.")
                    option = input("Please enter the number for the OPTION that you want >   ")

            display_team(option, team_results)
            print()
            pass
        elif command == '2':
            print('Display Team Stats will display a submenu to choose which team stats to display')
            print('Read above and below this line for the actions of the MENU options.')
            print('Quit will end the program.')
            print()
            continue
        elif command == '3':
            print("Good bye.\n\n")
            break
        else:
            print("\nThat is not a valid option. Please try again. \n")
            continue


if __name__ == "__main__":
    clear_screen()
    welcome()
    main()
