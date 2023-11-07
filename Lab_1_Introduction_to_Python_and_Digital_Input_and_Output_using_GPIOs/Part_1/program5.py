import sys

valList = [10, 20, 10, 40, 50, 60, 70]
valDict = {10:0, 20:1, 10:2, 40:3, 50:4, 60:5, 70:6}

indexDiff = sys.maxsize

targetVal = int(input('What is your target number? '))	#get user input for target number

smallestDiff = int(targetVal)
secondInt = 0
while secondInt < len(valList) - 1:
    firstInt = len(valList) - 1
    while firstInt > secondInt:
        total = valList[firstInt] + valList[secondInt]
        diff = abs(targetVal - total)
        if diff <= smallestDiff:
            smallestDiff = diff
            if abs(valList[firstInt] - valList[secondInt]) < indexDiff and valList[firstInt] - valList[secondInt] != 0:
                firstIndex = valDict[valList[secondInt]]
                secondIndex = valDict[valList[firstInt]]
                indexDiff = abs(valList[firstIndex] - valList[secondIndex])
        firstInt -= 1
    secondInt += 1
print("index1=" + str(firstIndex) + ", index2=" + str(secondIndex))