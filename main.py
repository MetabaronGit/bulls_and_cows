import random
import time
import os

SEPARATOR = "-" * 47
MAX_PLAYERS_IN_HIGH_SCORE = 5


def draw_greeting() -> None:
    print(SEPARATOR)
    print("Hi there!")
    print(SEPARATOR)
    print("I've generated a random 4 digit number for you.")
    print("Let's play a bulls and cows game.")
    print(SEPARATOR)
    print("Enter a number:")
    print(SEPARATOR)


def check_input(players_number: str) -> bool:
    result = False
    if not players_number.isdecimal():
        print("All characters must be decimals!")
    elif len(players_number) != 4:
        print("You must input just 4 numbers!")
    elif players_number[0] == "0":
        print("First number must not be 0!")
    elif len(set(players_number)) != 4:
        print("Decimals in number must be unique!")
    else:
        result = True
    return result


def check_secret(players_number: str, secret_number: list) -> str:
    bulls, cows = 0, 0
    result = ""

    for i, number in enumerate(players_number):
        if number == secret_number[i]:
            bulls += 1
        elif number in secret_number:
            cows += 1

    if bulls != 4:
        result = f"{bulls} bull"
        if bulls > 1:
            result += "s"
        result += f", {cows} cow"
        if cows > 1:
            result += "s"

    return result


def win_message(played_turns: int, total_time: float) -> str:
    time_format = time.strftime("%H:%M:%S", time.gmtime(total_time))
    print("Correct, you've guessed the right number")
    print(f"in {played_turns} guess", end="")
    if played_turns > 1:
        print("es!", end="")
    else:
        print("!", end="")
    print(f" Your time was {time_format}.")
    return time_format


def get_high_score() -> dict:
    result = dict()
    filename = "high_score.txt"
    if os.path.exists(filename):
        with open(filename, "r") as file:
            table_values = file.readlines()
            for i, line in enumerate(table_values):
                line = line.strip("\n").split(",")
                result[i] = dict(player=str(line[0]), guesses=str(line[1]), time=str(line[2]))
    return result


def draw_high_score(high_score_table: dict) -> None:
    if high_score_table:
        # High Score table header
        inner_separator = "+" + "-" * (len(SEPARATOR) - 23) + "+---------+----------+"
        print("+" + "-" * (len(SEPARATOR) - 2) + "+")
        print("|" + "{0:^{1}}".format("High Score", len(SEPARATOR) - 2) + "|")
        print("+" + "-" * (len(SEPARATOR) - 2) + "+")
        print("|" + "{:^{}}".format("player", len(SEPARATOR) - 23) + "| guesses |   time   |")
        print(inner_separator)

        # High Score table players
        counter = 0
        while counter < MAX_PLAYERS_IN_HIGH_SCORE and counter < len(high_score_table):
            print("|{:^{}}".format(high_score_table[counter]["player"], len(SEPARATOR) - 23) +
                  "|{:^9}".format(high_score_table[counter]["guesses"]) +
                  "|{:^10}|".format(high_score_table[counter]["time"]))
            counter += 1
        print(inner_separator)
    else:
        print("Still no players in High Score Table.")


def check_high_score(high_score_table: dict, played_turns: int, time_format: str) -> dict:
    counter = 0
    player_order = 0

    # check order
    if high_score_table:
        while counter < len(high_score_table):
            if played_turns <= int(high_score_table[counter]["guesses"]):
                if time_format < high_score_table[counter]["time"]:
                    player_order = counter
                    break
                else:
                    player_order = counter +1
                    break
            counter += 1

    # new record
    if player_order < MAX_PLAYERS_IN_HIGH_SCORE:
        print("Congratulations!")
        print("You have new record.")
        name = input("Enter your name: ")
        high_score_table = actualize_high_score(high_score_table, player_order, name, played_turns, time_format)

    return high_score_table


def actualize_high_score(old_high_score_table: dict, new_player_order: int, player_name: str, guesses: int, time: str) -> dict:
    counter = 0
    work_list = []
    result = dict()
    if old_high_score_table:
        while counter < MAX_PLAYERS_IN_HIGH_SCORE and counter < len(old_high_score_table):
            if new_player_order == counter:
                work_list.append(dict(player=player_name, guesses=guesses, time=time))

            work_list.append(old_high_score_table[counter])
            counter += 1
    else:
        work_list.append(dict(player=player_name, guesses=guesses, time=time))

    # create new high score table
    for i, item in enumerate(work_list):
        result[i] = work_list[i]

    return result


def save_high_score(high_score_table: dict) -> None:
    if high_score_table:
        counter = 0
        with open("high_score.txt", "w") as file:
            while counter < MAX_PLAYERS_IN_HIGH_SCORE and counter < len(high_score_table):
                line = f"{high_score_table[counter]['player']},{high_score_table[counter]['guesses']},{high_score_table[counter]['time']}"
                file.write(line + "\n")
                counter += 1


def main():
    played_turns = 0
    draw_greeting()
    high_score_table = get_high_score()

    # game setup
    avaible_numbers = list("0123456789")
    random.shuffle(avaible_numbers)
    secret_number = avaible_numbers[:4]
    if secret_number[0] == "0":
        secret_number.append(secret_number.pop(0))
    start_time = time.time()

    while True:
        players_number = input()
        if check_input(players_number):
            played_turns += 1
            message = check_secret(players_number, secret_number)
            if not message:
                total_time = time.time() - start_time
                time_format = win_message(played_turns, total_time)
                print(SEPARATOR)
                break
            else:
                print(message)
                print(SEPARATOR)

    print("Game over.")

    high_score_table = check_high_score(high_score_table, played_turns, time_format)
    draw_high_score(high_score_table)
    save_high_score(high_score_table)


if __name__ == "__main__":
    main()

