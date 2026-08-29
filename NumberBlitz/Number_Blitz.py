import random
name=input("Enter Your Name:")
print("-----------Welcome to the number guessing game----------")
print("Rules\n1.You have to guess a number between 1 to 100\n2.if the number you choose is also choosen by the computer you win\n3.if the number is incorrect the computer will tell you that the choosen number is higher or lower than your number\n4.You will get 7 chances to guess the number \n5.If you failed to guess the nummber in given chances you will lose")
a=input("start the game(y/n)")
while a=="y" or a=="Y":
    print("-----------All the best-----------\n----------- Enjoy the game----------")
    b=random.randint(1,100)
    won=False
    attempts = 0
    while attempts < 7:
        unumber = int(input("Enter Your Number: "))

        if unumber < 1 or unumber > 100:
            print("Please select a number between 1 to 100")
            continue  # doesn't count as a used chance

        attempts += 1
        remaining = 7 - attempts

        if unumber == b:
            print("-----------", name, "won the game---------")
            won = True
            break
        elif unumber > b:
            print("wrong entry the no. is lower than", unumber, "\nYou have", remaining, "chances left")
        else:
            print("wrong entry the no. is higher than", unumber, "\nYou have", remaining, "chances left")

    if won == False:
        print("----------You Lose-----------\nThe correct number was", b)

    a=input("do you want to play more(y/n)")

if a=="n" or a=="N":
    print("Thanks for playing",name)
else:                                #To check a
    print("invalid input")