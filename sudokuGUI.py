import PySimpleGUI as sg

class GUI:
    def newInput(self, buttonNum):
        box = sg.Input(
            default_text="",
            s = (1,1),
            justification = 'center',
            text_color = 'white',
            background_color = self.blue,
            font = self.boxFont,
            p = ((3,3),(3,3)),
            expand_x = True,
            expand_y = True,
            key = '-key' + str(buttonNum) + '-'
        )

        return box

    def newColumn(self, col):
        column = sg.Column(
            layout = col,
            background_color = self.darkBlue,
            element_justification = 'center',
            vertical_alignment = 'center',
            p=((6, 6), (6, 6)),
            expand_x = True,
            expand_y = True,
        )

        return column

    def updateGrid(self, filename, mode):
        file = open(filename, 'r')
        i = 0
        while i < 9:
            j = 0
            while j < 9:
                x = file.read(1)
                if x != '0' and x != '\n':
                    if mode == 'LOAD':
                        self.window['-key' + str(i) + str(j) + '-'].update(value=x, background_color=self.darkBlue)
                    elif mode == 'SOLVE':
                        self.window['-key' + str(i) + str(j) + '-'].update(value=x)
                    j += 1
                elif x == '0':
                    self.window['-key' + str(i) + str(j) + '-'].update(value = '', background_color=self.blue)
                    j += 1
                elif x == '\n':
                    continue
            i += 1

    def createGrid(self):
        gridLayout = []

        for outerRow in range(3):
            bigRow = []
            for outerCol in range(3):
                box = []
                for boxRow in range(3):
                    smallRow = []
                    for boxCol in range(3):
                        smallRow.append(self.newInput(str(outerRow*3 + boxRow) + str(outerCol*3 + boxCol)))
                    box.append(smallRow)
                bigRow.append(self.newColumn(box))
            gridLayout.append(bigRow)

        return gridLayout

    def createWindow(self):
        self.header = sg.Text(
            text = 'Choose a File or Enter a Puzzle',
            font=self.headerFont,
            background_color=self.pink,
            relief = 'raised',
            border_width = 3,
            text_color='white',
            expand_x=True,
            justification='center',
            p=((10,10),(10,10)),
            key='-HEADER-'
        )

        self.filePathBox = sg.Input(
            key = '-FILE_PATH-',
            expand_x = True,
            font = self.fileFont,
            background_color=self.blue,
            text_color = 'white'
        )

        self.fileBrowse = sg.FileBrowse(
            initial_folder= 'Puzzles/',
            file_types = [("Text Files", '*.txt')],
            font=self.fileFont,
            button_color=self.darkPurple,
            key='-BROWSE-'
        )

        self.clearButton = sg.Button(
            button_text = 'Clear',
            font=self.boxFont,
            button_color=('white', self.pink),
            use_ttk_buttons=True,
            border_width=3,
            expand_x=True,
            p=((10,10),(10,10)),
            key='-CLEAR-'
        )

        self.loadFileButton = sg.Button(
            button_text = 'Load from File',
            font=self.boxFont,
            button_color=('white', self.pink),
            use_ttk_buttons=True,
            border_width=3,
            expand_x=True,
            p=((10,10),(10,10)),
            key='-LOAD_FILE-'
        )

        self.solveButton = sg.Button(
            button_text = 'Solve It!',
            font=self.boxFont,
            button_color=('white', self.pink),
            use_ttk_buttons=True,
            border_width=3,
            expand_x=True,
            p=((10,10),(10,10)),
            key='-SOLVE-'
        )

        self.timeText = sg.Text(
            text='Solving, please wait...',
            font = self.solveFont,
            text_color=self.darkBlue,
            justification='center',
            background_color=self.darkBlue,
            expand_x=True,
            p = ((3,3),(3,3)),
            key = '-TIME-',
        )

        self.layout = [
            [self.header],
            [self.filePathBox, self.fileBrowse],
            [self.createGrid()],
            [self.clearButton, self.loadFileButton, self.solveButton],
            [self.timeText]
        ]

        self.window = sg.Window(
            'Sudoku Solver',
            layout=self.layout,
            background_color = self.darkBlue,
            force_toplevel = True,
            size = (600, 800),
        )

    def __init__(self, inFile, outFile):
        self.inFile = inFile
        self.outFile = outFile

        self.darkBlue = '#0d1847'
        self.blue = '#233376'
        self.pink = '#d8544d'
        self.purple = '#412673'
        self.darkPurple = '#22035d'

        self.boxFont = ('SYSTEM_DEFAULT', 25, 'bold')
        self.headerFont = ('SYSTEM_DEFAULT', 35, 'bold')
        self.fileFont = ('SYSTEM_DEFAULT', 14)
        self.solveFont = ('SYSTEM_DEFAULT', 20, 'bold')