fibStart = 1
a = [0] * 10
for i in range(10):
    if i == 0:
        a[i] = fibStart
    elif i == 1:
        a[i] = a[i-1]
    elif i >= 2:
        a[i] = a[i-1] + a[i-2]
print('a = ' + str(a))

maxNum = input('Enter number: ')
newList = []
for val in a:
    if val < int(maxNum):
        newList.append(val)
print('The new list is ' + str(newList))