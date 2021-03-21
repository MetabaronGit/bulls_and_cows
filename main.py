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


def main():
    draw_greeting()

    avaible_numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    random.shuffle(avaible_numbers)
    secret_number = avaible_numbers[:4]
    if secret_number[0] == 0:
        secret_number.append(secret_number.pop(0))

    while True:
        players_number = input()
        print(secret_number)
        print(players_number)


if __name__ == "__main__":
    main()

