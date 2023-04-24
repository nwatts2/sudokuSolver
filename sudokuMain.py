from sudokuGUI import GUI
import PySimpleGUI as sg
import time

outFile = 'Puzzles/puzzleSolution.txt'
inFile = 'Puzzles/puzzle.txt'
clearFile = 'Puzzles/clearPuzzle.txt'

def puzzleRead(filePath):
    global grid, goodFile
    allowed = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '\n']

    file = open(filePath, 'r')
    grid = []
    goodFile = True

    for x in range(9):
        rowList = []
        row = file.readline()
        for i in row:
            if i != '\n' and i in allowed:
                rowList.append(int(i))
            elif i not in allowed:
                goodFile = False
                return

        if goodFile:
            grid.append(rowList)

    file.close()

def writePuzzle():
    global gui, goodEntry
    goodEntry = True
    array = ''
    for row in range(9):
        for col in range(9):
            inBox = gui.window['-key' + str(row) + str(col) + '-']
            if str(inBox.get()).isdigit() and int(inBox.get()) < 10 and int(inBox.get()) >= 0:
                array += str(inBox.get())
            elif str(inBox.get()) == '':
                array += '0'
            else:
                goodEntry = False
                return

    file = open(inFile, 'w')
    file.write('')
    file.close()

    file = open(inFile, 'a')
    i = 0
    while i < 81:
        for x in range(9):
            for y in range(9):
                file.write(array[i])
                i += 1
            file.write('\n')
    file.close()
    return

def notEmpty():
    global grid
    numZeros = 0

    for i in range(9):
        for j in range(9):
            if str(grid[i][j]) == '0':
                numZeros += 1

    if numZeros == 81:
        return False
    else:
        return True

def possible(row, column, number):
    global grid

    hStart = column // 3 * 3
    vStart = row // 3 * 3

    tempRow = []
    tempCol = []
    tempBox = []

    for i in range(9):
        tempRow.append(grid[row][i])
        tempCol.append(grid[i][column])

    for i in range(3):
        for j in range(3):
            tempBox.append(grid[vStart + i][hStart + j])

    if number in tempRow or number in tempCol or number in tempBox:
        return False
    else:
        return True

def solve():
    global grid

    for row in range(9):
        for column in range(9):
            if grid[row][column] == 0:
                for number in range(1,10):
                    if possible(row, column, number):
                        grid[row][column] = number
                        solve()
                        grid[row][column] = 0
                return
    outputSolution()

def outputSolution():
    global grid

    file = open(outFile, 'w')
    file.write('')
    file.close()

    file = open(outFile, 'a')
    for i in range(9):
        for j in range(9):
            file.write(str(grid[i][j]))
        file.write('\n')
    file.close()

def main():
    global grid, gui

    gui = GUI(inFile, outFile)

    gui.createWindow()

    while True:
        event, values = gui.window.read()
        if event == '-CLEAR-':
            gui.updateGrid(clearFile, 'LOAD')
            gui.timeText.update(value='', text_color=gui.darkBlue)
        elif event == '-LOAD_FILE-' and gui.window['-FILE_PATH-'].get() != '':
            try:
                puzzleRead(gui.window['-FILE_PATH-'].get())
            except:
                gui.timeText.update(value='Entered file does not exist. Please try again.', text_color='white')
            else:
                if goodFile:
                    gui.timeText.update(value='', text_color=gui.darkBlue)
                    gui.updateGrid(gui.window['-FILE_PATH-'].get(), 'LOAD')
                else:
                    gui.timeText.update(value='File is not in correct format. Please try again.', text_color='white')
                    gui.updateGrid(clearFile, 'LOAD')
        elif event == '-SOLVE-':
            writePuzzle()

            if goodEntry:
                puzzleRead(inFile)
                if notEmpty():
                    gui.timeText.update(value='Solving, please wait...', text_color='white')
                    gui.solveButton.update(disabled=True)
                    gui.loadFileButton.update(disabled=True)

                    startTime = time.time()

                    solve()

                    endTime = time.time()
                    computeTime = endTime - startTime

                    gui.updateGrid(outFile, 'SOLVE')

                    gui.timeText.update(value='Solve Time: {:.3f} seconds'.format(computeTime))
                    gui.solveButton.update(disabled=False)
                    gui.loadFileButton.update(disabled=False)
                else:
                    gui.timeText.update(value='Puzzle is empty. Please try again.', text_color='white')
            else:
                gui.timeText.update(value='Puzzle has invalid characters. Please try again.', text_color='white')

        elif event == sg.WIN_CLOSED:
            break

    gui.window.close()

main()