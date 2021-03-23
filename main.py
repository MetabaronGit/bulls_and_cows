import random
import time
import os

SEPARATOR = "-" * 47
MAX_PLAYERS_IN_HIGH_SCORE = 5


def draw_greeting() -> None:
    """
    Vypíše úvodní pozdrav

    :return: None
    """
    print(SEPARATOR)
    print("Hi there!")
    print(SEPARATOR)
    print("I've generated a random 4 digit number for you.")
    print("Let's play a bulls and cows game.")
    print(SEPARATOR)
    print("Enter a number:")
    print(SEPARATOR)


def check_input(players_number: str) -> bool:
    """
    Kontroluje správnost formátu hráčova vstupního čísla

    :param players_number: hráčovo zadané číslo
    :return: bool
    """
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
    """
    Porovnání zadaného čísla s tajným číslem a vyhodnocení bulls / cows

    :param players_number: hráčovo zadané číslo
    :param secret_number: hádané číslo
    :return: string s počty bulls / cows
    """
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


def draw_win_message(played_turns: int, total_time: float) -> str:
    """
    Vypíše gratulaci se statistikou po uhodnutí hádaného čísla.

    :param played_turns: počet kol, které hráč potřeboval
    :param total_time: celkový čas hry
    :return: string s formátovaným celkovým časem hry
    """
    time_format = time.strftime("%H:%M:%S", time.gmtime(total_time))
    print("Correct, you've guessed the right number")
    print(f"in {played_turns} guess", end="")
    if played_turns > 1:
        print("es!", end="")
    else:
        print("!", end="")
    print(f" Your time was {time_format}.")
    return time_format


def get_high_score() -> list:
    """
    Načte High Score tabulku ze souboru a vytvoří odpovídající list.

    :return: list slovníků, který reprezentuje tabulku High Score
    """
    result = list()
    filename = "high_score.txt"
    if os.path.exists(filename):
        with open(filename, "r") as file:
            for item in file.readlines():
                line = item.strip("\n").split(",")
                result.append(dict(player=str(line[0]), guesses=str(line[1]), time=str(line[2])))
    if len(result) > MAX_PLAYERS_IN_HIGH_SCORE:
        result = result[:MAX_PLAYERS_IN_HIGH_SCORE]

    return result


def draw_high_score(high_score_table: list) -> None:
    """
    Vykreslí tabulku High Score

    :param high_score_table: list s tabulkou High Score
    """
    if high_score_table:
        # High Score table header
        inner_separator = "+" + "-" * (len(SEPARATOR) - 23) + "+---------+----------+"
        print("+" + "-" * (len(SEPARATOR) - 2) + "+")
        print("|" + "{0:^{1}}".format("High Score", len(SEPARATOR) - 2) + "|")
        print("+" + "-" * (len(SEPARATOR) - 2) + "+")
        print("|" + "{:^{}}".format("player", len(SEPARATOR) - 23) + "| guesses |   time   |")
        print(inner_separator)

        # High Score table players
        for line in high_score_table:
            print("|{:^{}}".format(line["player"], len(SEPARATOR) - 23) +
                  "|{:^9}".format(line["guesses"]) +
                  "|{:^10}|".format(line["time"]))
        print(inner_separator)
    else:
        print("Still no players in High Score Table.")


def check_high_score(high_score_table: list, played_turns: int, time_format: str) -> int:
    """
    Zjistí pořadí hráče v tabulce High Score.

    :param high_score_table: Tabulka High Score
    :param played_turns: počet odehraných kol
    :param time_format: odehraný čas ve formátu hh:mm:ss
    :return: Pořadí hráče v tabulce High Score
    """
    player_order = 0

    # check order
    if high_score_table:
        for i, line in enumerate(high_score_table):
            if played_turns <= int(line["guesses"]):
                if time_format < line["time"]:
                    player_order = i
                    break
                else:
                    player_order = i + 1
                    break
    return player_order


def get_player_name() -> str:
    """
    Získá hráčovo jméno.

    :return: hráčovo jméno
    """
    print("Congratulations!")
    print("You have new record.")
    name = input("Enter your name: ")
    if len(name) > len(SEPARATOR) - 25:
        name = name[:len(SEPARATOR) - 25]
    return name


def actualize_high_score(high_score_table: list, new_player_order: int, player_name: str, guesses: int, time: str) -> list:
    """
    Vloží nový zápis do tabulky High Score

    :param high_score_table: původní tabulka High Score
    :param new_player_order: nové pořadí hráče
    :param player_name: jméno hráče
    :param guesses: počet odehraných kol
    :param time: celkový čas hry
    :return: aktualizovaná tabulka High Score
    """
    high_score_table.insert(new_player_order, dict(player=player_name, guesses=guesses, time=time))
    if len(high_score_table) > MAX_PLAYERS_IN_HIGH_SCORE:
        high_score_table.pop()

    return high_score_table


def save_high_score(high_score_table: list) -> None:
    """
    Uloží záznamy z High Score tabulky do souboru

    :param high_score_table: list tabulky High Score
    :return: None
    """
    if high_score_table:
        with open("high_score.txt", "w") as file:
            for item in high_score_table:
                line = f"{item['player']},{item['guesses']},{item['time']}"
                file.write(line + "\n")


def main():
    played_turns = 0
    draw_greeting()

    # game setup
    high_score_table = get_high_score()
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
                time_format = draw_win_message(played_turns, total_time)
                print(SEPARATOR)
                break
            else:
                print(message)
                print(secret_number) # delete!!!!
                print(SEPARATOR)

    print("Game over.\n")

    # Game result
    player_order = check_high_score(high_score_table, played_turns, time_format)
    if player_order < MAX_PLAYERS_IN_HIGH_SCORE:
        player_name = get_player_name()
        actualize_high_score(high_score_table, player_order, player_name, played_turns, time_format)
        draw_high_score(high_score_table)
        save_high_score(high_score_table)


if __name__ == "__main__":
    main()

