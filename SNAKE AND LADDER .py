import random
def roll_dice():
    return random.randint(1,6)
def GAME():
    player1_score=0
    player2_score=0
    while True:
        while True:
            choice=input("Player 1,press 1 to roll the dice!\n")
            if choice=='1':
                player1roll=roll_dice()
                print(f"Player 1 rolled:{player1roll}")
                if player1_score+player1roll>21:
                    print("ROLL NOT COUNTED")
                else:
                    player1_score+=player1roll
                break
            else:
                print("ERROR! Please press 1 to roll")
        if player1_score==21:
            print("Player 1 WINS!")
            break
        while True:
            choice=input("Player 2,press 2 to roll the dice!\n")
            if choice=='2':
                player2roll=roll_dice()
                print(f"Player 2 rolled:{player2roll}")
                if player2_score+player2roll>21:
                    print("ROLL NOT COUNTED")
                else:
                    player2_score+=player2roll
                break
            else:
                print("ERROR! Please press 2 to roll")
        if player2_score==21:
            print("Player 2 WINS!")
            break
        print(f"Score-Player1:{player1_score},Player2:{player2_score}\n")
GAME()
        
