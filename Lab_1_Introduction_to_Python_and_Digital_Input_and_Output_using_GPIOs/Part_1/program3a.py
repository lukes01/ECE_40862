length = input('How many Fibonacci numbers would you like to generate? ')
fibLen = int(length)
fibStart = 1
fibSeq = [0] * fibLen
i = 0
while i < fibLen:
    if i == 0:
        fibSeq[i] = fibStart
    elif i == 1:
        fibSeq[i] = fibSeq[i-1]
    elif i >= 2:
        fibSeq[i] = fibSeq[i-1] + fibSeq[i-2]
    i += 1
print('The Fibonacci Sequence is: ' + str(fibSeq))