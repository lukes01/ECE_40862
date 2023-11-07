import random
num = random.randint(0,10)t
for attempt in range(3):
    guess = int(input('Enter your guess: '))
    if guess == num:
        print('You win!')
        break
if guess != num:
    print('You lose!')
    