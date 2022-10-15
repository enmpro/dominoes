import random

random.seed()

stock_list = []
computer_set = []
player_set = []
snake = []
com_double = 0
play_double = 0
com_check = True
play_check = True
snake_count = 0
turn = False
winner_com = False
winner_play = False
eight_number = False
zero, one, two, three, four, five, six = 0, 0, 0, 0, 0, 0, 0
number_list = {}
maximum = 0


def display():
    print("======================================================================")
    print(f"Stock size: {len(stock_list)}")
    print(f"Computer pieces: {len(computer_set)}")
    print("")
    if len(snake) < 7:
        print(*snake, sep="")
    else:
        print(f"{snake[0]}{snake[1]}{snake[2]}...{snake[-3]}{snake[-2]}{snake[-1]}")
    print("")
    print("Your pieces:")
    for num in range(len(player_set)):
        print(f"{num + 1}:{player_set[num]}")


# count all the numbers listed in the computer hand and on the field
def count_numbers(a_list):
    global zero, one, two, three, four, five, six
    global number_list
    for dominos in a_list:
        for number in dominos:
            if number == 0:
                zero += 1
            elif number == 1:
                one += 1
            elif number == 2:
                two += 1
            elif number == 3:
                three += 1
            elif number == 4:
                four += 1
            elif number == 5:
                five += 1
            elif number == 6:
                six += 1

    number_list = {
        0: zero,
        1: one,
        2: two,
        3: three,
        4: four,
        5: five,
        6: six
    }


# calculate the domino of the highest score
def calculate_choice(ai_choice):
    global maximum, domino_chosen
    for dominos in ai_choice:
        num1 = dominos[0]
        num2 = dominos[1]
        max_check = 0
        for x in number_list:
            if num1 == x:
                max_check += number_list[x]
            elif num2 == x:
                max_check += number_list[x]
        if max_check > maximum:
            domino_chosen = dominos
            maximum = max_check
    return domino_chosen


# makes the dominos
for num1 in range(7):
    for num2 in range(num1, 7):
        stock_list.append([num1, num2])

# computer hand
while com_check:
    for _ in range(7):
        choice = random.choice(stock_list)
        computer_set.append(choice)
        stock_list.remove(choice)

    for domino in computer_set:
        if domino[0] == domino[1]:
            com_double += 1

    if com_double > 1:
        com_check = False
    else:
        stock_list.extend(computer_set)
        computer_set = []
        continue

# player hand
while play_check:
    for _ in range(7):
        choice = random.choice(stock_list)
        player_set.append(choice)
        stock_list.remove(choice)

    for domino in player_set:
        if domino[0] == domino[1]:
            play_double += 1

    if play_double > 1:
        play_check = False
    else:
        stock_list.extend(player_set)
        player_set = []
        continue

computer_set.sort(reverse=True)
player_set.sort(reverse=True)
copy_com_set = computer_set.copy()

# calculates who goes first
for domino1 in computer_set:
    if domino1[0] == domino1[1]:
        for domino2 in player_set:
            if domino2[0] == domino2[1]:
                turn = domino1 > domino2
                if turn is True:
                    snake_count += 1
                    snake = [domino1]
                    computer_set.remove(domino1)
                    break
                else:
                    snake_count += 1
                    snake = [domino2]
                    player_set.remove(domino2)
                    break
    if snake_count > 0:
        break

while winner_com is False and winner_play is False:
    display()
    print("")

    if turn is True:
        print("Status: It's your turn to make a move. Enter your command.")
    while turn is True:
        try:
            player_turn = int(input())
            if 0 < player_turn <= len(player_set):
                if player_set[player_turn - 1][0] == snake[-1][1]:
                    piece_add = player_set[player_turn - 1]
                    snake.append(piece_add)
                    player_set.remove(piece_add)
                    turn = False
                    break
                elif player_set[player_turn - 1][1] == snake[-1][1]:
                    piece_add = player_set[player_turn - 1]
                    piece_add.reverse()
                    snake.append(piece_add)
                    player_set.remove(piece_add)
                    turn = False
                    break
                else:
                    print("Illegal move. Please try again.")
            elif 0 > player_turn >= -len(player_set):
                if player_set[abs(player_turn) - 1][1] == snake[0][0]:
                    piece_add = player_set[abs(player_turn) - 1]
                    snake.insert(0, piece_add)
                    player_set.remove(piece_add)
                    turn = False
                    break
                elif player_set[abs(player_turn) - 1][0] == snake[0][0]:
                    piece_add = player_set[abs(player_turn) - 1]
                    piece_add.reverse()
                    snake.insert(0, piece_add)
                    player_set.remove(piece_add)
                    turn = False
                    break
                else:
                    print("Illegal move. Please try again.")
            elif player_turn == 0:
                piece_add = random.choice(stock_list)
                player_set.append(piece_add)
                stock_list.remove(piece_add)
                turn = False
                break
            elif player_turn > len(player_set) or player_turn < -len(player_set):
                print("Invalid input. Please try again.")
        except ValueError:
            print("Invalid input. Please try again.")

    else:
        player_turn = input("Status: Computer is about to make a move. Press Enter to continue...\n")
        copy_com_set = computer_set.copy()
        while turn is False:
            count_numbers(snake)
            count_numbers(computer_set)

            for computer_choice in range(-1, 1):
                piece_add = calculate_choice(copy_com_set)
                if computer_choice == -1:
                    if piece_add[1] == snake[0][0]:
                        snake.insert(0, piece_add)
                        computer_set.remove(piece_add)
                        maximum = 0
                        turn = True
                        break
                    elif piece_add[0] == snake[0][0]:
                        piece_add.reverse()
                        snake.insert(0, piece_add)
                        computer_set.remove(piece_add)
                        maximum = 0
                        turn = True
                        break
                    elif (piece_add[1] != snake[0][0] or piece_add[0] != snake[0][0]) and piece_add in copy_com_set and len(copy_com_set) > 0:
                        copy_com_set.remove(piece_add)
                        maximum = 0
                        continue
                elif computer_choice == 0:
                    if piece_add[0] == snake[-1][1]:
                        snake.append(piece_add)
                        computer_set.remove(piece_add)
                        maximum = 0
                        turn = True
                        break
                    elif piece_add[1] == snake[-1][1]:
                        piece_add.reverse()
                        snake.append(piece_add)
                        computer_set.remove(piece_add)
                        maximum = 0
                        turn = True
                        break
                    elif (piece_add[0] != snake[-1][1] or piece_add[1] != snake[-1][1]) and piece_add in copy_com_set and len(copy_com_set) > 0:
                        copy_com_set.remove(piece_add)
                        maximum = 0
                        continue
            if len(copy_com_set) < 1:
                piece_add = random.choice(stock_list)
                computer_set.append(piece_add)
                stock_list.remove(piece_add)
                turn = True
                break

            zero, one, two, three, four, five, six = 0, 0, 0, 0, 0, 0, 0

    if len(computer_set) < 1 and len(player_set) > 0:
        display()
        print("")
        print("Status: The game is over. The computer won!")
        exit()
    elif len(player_set) < 1 and len(computer_set) > 0:
        display()
        print("")
        print("Status: The game is over. You won!")
        exit()

    # calculates if number repeated 8 times at each end of domino
    counter = 0
    repeated_number = 0
    for x in range(1, 7):
        for domino in snake:
            counter = counter + domino.count(x)

        if counter != 8:
            counter = 0
        else:
            repeated_number = x
            eight_number = True

    if eight_number is True and snake[0][0] == repeated_number == snake[-1][-1]:
        display()
        print("")
        print("Status: The game is over. It's a draw!")
    elif len(stock_list) < 1:
        display()
        print("")
        print("Status: The game is over. It's a draw!")
        exit()
