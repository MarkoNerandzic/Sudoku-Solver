#-------------------------------------------------------------------------------
# Name:
# Purpose:
#
# Author:       Marko Nerandzic
#
# Created:      13/06/2013
# Copyright:    (c) Marko Nerandzic 2013
# Licence:      This work is licensed under the Creative Commons Attribution-
#               NonCommercial-NoDerivs 3.0 Unported License. To view a copy of
#               this license, visit http://creativecommons.org/licenses/by-nd/3.0/.
#-------------------------------------------------------------------------------

def main():
    grid = []

    counter = 0
    counter2 = 0

    while counter < 9:
        grid.append([])
        counter2 = 0
        while counter2 < 9:
            grid[counter].append([False, [0]])
            counter2 += 1
        counter += 1

    inputFile = open('sudokuInput.txt')

    counter = 0

    for line in inputFile:
        if counter < 9:
            line = line[:-1]
            counter2 = 0
            while counter2 < 9:
                if line[counter2] != ' ':
                    grid[counter2][counter][0] = True
                    grid[counter2][counter][1] = [int(line[counter2])]
                else:
                    grid[counter2][counter][1] = [1,2,3,4,5,6,7,8,9] #Since the first element in the third array is already set to False
                counter2 += 1
            counter += 1

    print "Starting Puzzle:"
    printGrid(grid)

    noFurtherMoves = False
    solved = False
    counter4 = 0
    while not solved and not noFurtherMoves:
        solved = checkGridForSolved(grid)
        noFurtherMoves = True #This will be disproven later if a move can be made

        lastGridChecked = 0
        while lastGridChecked < 9:
            counter = 0
            counter2 = 0
            notAvailableNumbersInGrid = []  #Finds all the numbers already taken in the square (the 3 by 3 square)
            while counter < 3:
                while counter2 < 3:
                    if grid[counter2 + (lastGridChecked % 3) * 3][counter + (lastGridChecked /3) * 3][0]:
                        notAvailableNumbersInGrid.append(grid[counter2 + (lastGridChecked % 3)* 3][counter + (lastGridChecked /3)* 3][1][0])#Finds available numbers
                    counter2 += 1
                counter += 1
                counter2 = 0
            availableNumbersInGrid = [] #Finds the available numbers
            counter = 1
            while counter <= 9:
                if not (counter in notAvailableNumbersInGrid):
                    availableNumbersInGrid.append(counter)
                counter += 1
            counter = 0
            counter2 = 0
            while counter < 3:
                while counter2 < 3:
                    if not grid[counter2 + (lastGridChecked % 3) * 3][counter + (lastGridChecked /3) * 3][0]:
                        grid[counter2 + (lastGridChecked % 3)* 3][counter + (lastGridChecked /3) * 3][1] = availableNumbersInGrid[:]#Initializes each not determined spot with list of availabe number in square
                    counter2 += 1
                counter += 1
                counter2 = 0
            lastGridChecked += 1

        counter = 0
        while counter < 9:
            notAvailableNumbersInRow = [] #Finds the numbers that are not available in this row
            counter2 = 0
            while counter2 < 9:
                if grid[counter2][counter][0]:
                    notAvailableNumbersInRow.append(grid[counter2][counter][1][0])
                counter2 += 1

            availableNumbersInRow = [] #Finds the numbers that are available in this row
            counter2 = 1
            while counter2 <= 9:
                if not(counter2 in notAvailableNumbersInRow):
                    availableNumbersInRow.append(counter2)
                counter2 += 1

            counter2 = 0    #Basically preforms an AND operation with the original list and the available numbers list and keeps what's in both lists
            while counter2 < 9:
                if not grid[counter2][counter][0]:
                    counter3 = 0
                    while counter3 < len(grid[counter2][counter][1]):
                        if not grid[counter2][counter][1][counter3] in availableNumbersInRow:
                            grid[counter2][counter][1].pop(counter3)
                            counter3 -= 1   #Since the current element being checked is popped, if we want to check the enxt, the counter has to remain the same
                        counter3 += 1
                counter2 += 1
            counter += 1

        counter = 0
        while counter < 9:
            notAvailableNumbersInColumn = []
            counter2 = 0
            while counter2 < 9:
                if grid[counter][counter2][0]:
                    notAvailableNumbersInColumn.append(grid[counter][counter2][1][0])
                counter2 += 1

            availableNumbersInColumn = []
            counter2 = 1
            while counter2 <= 9:
                if not (counter2 in notAvailableNumbersInColumn):
                    availableNumbersInColumn.append(counter2)
                counter2 += 1

            counter2 = 0
            while counter2 < 9:
                if not grid[counter][counter2][0]:
                    counter3 = 0
                    while counter3 < len(grid[counter][counter2][1]):
                        if not grid[counter][counter2][1][counter3] in availableNumbersInColumn:
                            grid[counter][counter2][1].pop(counter3)
                            counter3 -= 1
                        counter3 += 1
                counter2 += 1
            counter += 1

        counter = 0 #Checks if any single square has only one possible value to store inside of it
        counter2 = 0
        while counter < 9:
            while counter2 < 9:
                if not grid[counter2][counter][0] and len(grid[counter2][counter][1]) == 1:
                    noFurtherMoves = False
                    grid[counter2][counter][0] = True
                counter2 += 1
            counter += 1
            counter2 = 0
        if noFurtherMoves:
            counter = 0
            while counter < 9:
                amountOfNumbersInRow = [0,0,0,0,0,0,0,0,0]
                counter2 = 0
                while counter2 < 9:                         #Figure out how many square can hold each remaining number
                    if grid[counter2][counter][0]:
                        amountOfNumbersInRow[grid[counter2][counter][1][0] - 1] = 0
                    else:
                        for element in grid[counter2][counter][1]:
                            amountOfNumbersInRow[element - 1] += 1
                    counter2 += 1
                counter2 = 0
                while counter2 < 9:
                    if amountOfNumbersInRow[counter2] == 1: #If there is only one square that can hold that number
                        counter3 = 0
                        while counter3 < 9:
                            if (counter2 + 1) in grid[counter3][counter][1]:    #Find that square
                                grid[counter3][counter][1] = [counter2 + 1]
                                grid[counter3][counter][0] = True               #Make set it to that number
                                noFurtherMoves = False
                            counter3 += 1
                    counter2 += 1
                counter += 1

        if noFurtherMoves:
            counter = 0
            while counter < 9:
                amountOfNumbersInColumn = [0,0,0,0,0,0,0,0,0]
                counter2 = 0
                while counter2 < 9:
                    if grid[counter][counter2][0]:
                        amountOfNumbersInColumn[grid[counter][counter2][1][0]-1] = 0
                    else:
                        for element in grid[counter][counter2][1]:
                            amountOfNumbersInColumn[element -1] += 1
                    counter2 += 1
                counter2 = 0
                while counter2 < 9:
                    if amountOfNumbersInColumn[counter2] == 1:
                        counter3 = 0
                        while counter3 < 9:
                            if (counter2 + 1) in grid[counter][counter3][1]:
                                grid[counter][counter3][1] = [counter2 + 1]
                                grid[counter][counter3][0] = True
                                noFurtherMoves = False
                            counter3 += 1
                    counter2 += 1
                counter += 1

        if noFurtherMoves:
            lastGridChecked = 0
            while lastGridChecked < 9:
                counter = 0
                amountOfNumbersInGrid = [0,0,0,0,0,0,0,0,0]
                while counter < 3:
                    counter2 = 0
                    while counter2 < 3:
                        if grid[counter + (lastGridChecked % 3) * 3][counter2 + (lastGridChecked / 3) * 3][0]:
                            amountOfNumbersInColumn[grid[counter + (lastGridChecked % 3) * 3][counter2 + (lastGridChecked / 3) * 3][1][0] - 1] = 0
                        else:
                            for element in grid[counter + (lastGridChecked % 3) * 3][counter2 + (lastGridChecked / 3) * 3][1]:
                                amountOfNumbersInGrid[element - 1] += 1
                        counter2 += 1
                    counter += 1
                counter = 0
                while counter < 9:
                    if amountOfNumbersInGrid[counter] == 1:
                        counter2 = 0
                        while counter2 < 3:
                            counter3 = 0
                            while counter3 < 3:
                                if (counter + 1) in grid[counter2 + (lastGridChecked % 3) * 3][counter3 + (lastGridChecked / 3) * 3][1]:
                                    grid[counter2 + (lastGridChecked % 3) * 3][counter3 + (lastGridChecked / 3) * 3][1] = [counter + 1]
                                    grid[counter2 + (lastGridChecked % 3) * 3][counter3 + (lastGridChecked / 3) * 3][0] = True
                                    noFurtherMoves = False
                                counter3 += 1
                            counter2 += 1
                    counter += 1
                lastGridChecked += 1
        counter4 += 1

    if solved:
        print "Finished Puzzle:"
        printGrid(grid)
    elif noFurtherMoves:
        print "This puzzle is impossible to solve!"

    pass

def checkGridForSolved(grid):
    counter = 0
    counter2 = 0
    allFilledIn = True
    while allFilledIn and counter < 9:
        counter2 = 0
        while allFilledIn and counter2 < 9:
            allFilledIn = grid[counter][counter2][0] #Doing it this way should stop it at the first False since both loops have it being true as a condition
            counter2 += 1
        counter += 1
    return allFilledIn

def printGrid(grid):
    counter = 0     #Prints the results
    counter2 = 0
    while counter < 9:
        counter2 = 0
        while counter2 < 9:
            if grid[counter2][counter][0]:
                print grid[counter2][counter][1][0],
            else:
                print ' ',
            counter2 += 1
        print ''
        counter += 1

if __name__ == '__main__':
    main()
