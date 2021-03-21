import random
SEPARATOR = "-" * 47

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


def win_message(played_turns: int) -> None:
    print("Correct, you've guessed the right number")
    print(f"in {played_turns} guess", end="")
    if played_turns > 1:
        print("es!")
    else:
        print("!")


def main():
    played_turns = 0
    draw_greeting()

    avaible_numbers = list("0123456789")
    random.shuffle(avaible_numbers)
    secret_number = avaible_numbers[:4]
    if secret_number[0] == "0":
        secret_number.append(secret_number.pop(0))

    while True:
        players_number = input()
        if check_input(players_number):
            played_turns += 1
            message = check_secret(players_number, secret_number)
            if not message:
                win_message(played_turns)
                print(SEPARATOR)
                exit()
            else:
                print(message)
                print(secret_number)
                print(SEPARATOR)


if __name__ == "__main__":
    main()

