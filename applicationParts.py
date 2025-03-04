import tkinter as tk
from helperFunctions import packInSquare

class GUI:

    defaultSudoku = [5,3,0,0,7,0,0,0,0,
                     6,0,0,1,9,5,0,0,0,
                     0,9,8,0,0,0,0,6,0,
                     8,0,0,0,6,0,0,0,3,
                     4,0,0,8,0,3,0,0,1,
                     7,0,0,0,2,0,0,0,6,
                     0,6,0,0,0,0,2,8,0,
                     0,0,0,4,1,9,0,0,5,
                     0,0,0,0,8,0,0,7,9]

    def __init__(self):
        #generates two separateFrames for input values and control
        entryFrame = tk.Frame()
        entryFrame.pack()
        buttonFrame = tk.Frame()
        buttonFrame.pack()
        #generates list with 81 single entry fields
        #generates 9x9 square in frame
        self.__entries = [tk.Entry(master=entryFrame, width=5) for i in range(81)]
        packInSquare(self.__entries, 9, 3)
        #generates list with 3 buttons and packs them side-by-side
        self.__buttons = [tk.Button(master=buttonFrame, text="Set default"), tk.Button(master=buttonFrame, text="Solve sudoku"),
                    tk.Button(master= buttonFrame, text="Reset")]
    
        for button in self.__buttons:
            button.pack(side=tk.LEFT, padx = 5)
        #Label with iterationCounter
        self.label = tk.Label()
        self.label.pack()
        #inserts the default sudoku Values
        self.setGrid()
    
    
    def setGrid(self, values = defaultSudoku):
        
        for i in range(len(values)):
            #remove old entries
            self.__entries[i].delete(0,tk.END)
            #0 is only for internal use, entry field is empty
            if values[i] == 0:
                continue
            self.__entries[i].insert(index=0, string=values[i])

    def deleteGrid(self):
         [entry.delete(0, tk.END) for entry in self.__entries]

    @property
    def entries(self):
        return self.__entries
    
    @property
    def buttons(self):
        return self.__buttons    

class EventHandler:

    def __init__(self, gui : GUI):
        self.gui = gui
        self.__entries = gui.entries
        self.__buttons = gui.buttons

        self.__buttons[0].bind("<Button-1>", self.setDefault)
        self.__buttons[1].bind("<Button-1>", self.solveSudoku)
        self.__buttons[2].bind("<Button-1>", self.delete)

    def delete(self, event):
        self.gui.deleteGrid()

    def setDefault(self, event):
        self.gui.setGrid()

    def solveSudoku(self, event):
        #to solve sudoku generates object of logic class
        logic = Logic(self.__entries)
        #removes old entries (otherwise the new entry would be added to the old one)
        self.gui.deleteGrid()
        #assign each entry field the solved value
        self.gui.setGrid(logic.solveSudoku())
        #Label shows numb of interations
        self.gui.label.config(text= f"Iterations: {logic.iterationCounter}")

class Logic:
    #init of Logic class generates two list both containing
    #the values of the sudoku: one is to solve, control is
    #to check which value was fixed from the input
    def __init__(self, entries : list):
        self.sudokuValues = []
        self.controlValues = []

        self.__iterationCounter = 0

        for entry in entries:
            input = entry.get()
            #as entry input is string, empty string represents 0
            if input == "":
                self.sudokuValues.append(0)
                self.controlValues.append(0)
                continue

            self.sudokuValues.append(int(input))
            self.controlValues.append(int(input))

    def solveSudoku(self):
        #solve sudoku starts at index 0 and goes through the value list
        #moveAndFincrement() increases each value for empty field(0),
        #checks if its correct and does potential corrections recursively
        index = 0
        
        while (index <81):
            index = self.moveAndIncrement(index)
        #returns solved suldoku
        return self.sudokuValues
    
    def moveAndIncrement(self, index : int):

        self.__iterationCounter +=1
        #if number is present in the control array
        #skip the position and returns next index
        if (self.controlValues[index] != 0):
            index +=1
            return index

        #increments the value of the active textfield
        #starting from 0 
        self.sudokuValues[index] += 1
        
        #if 1-9 didn't matched (value larger than nine)
        #correction mechanism is started 
        if (self.sudokuValues[index] > 9):
            #sets actual value again to zero
            self.sudokuValues[index] = 0
            #index is diminished by one
            index -= 1
            #diminishes index until non occupied 
            #controlfield is reached
            while(self.controlValues[index] != 0):
                index -= 1

            #recursively calls the function until
            #next possible number is found
            index = self.moveAndIncrement(index)

        #if it matches conditions (each number once a row/column/3x3 grid)
        #index is increased by one, continuing with next field
        if(self.checkConditions(index)):
            index += 1
        #otherwise restarting the cycle with the same textField
        return index
    
    def checkConditions(self, index : int):
        value = self.sudokuValues[index]
        return self.checkRow(index) and self.checkColumn(index) and self.checkSquare(index) and value != 0
    
    def checkRow(self, index : int):
        #rows are 9 next values of 0, 9, 18, 27, 36, 45, 54, 63, 72
        start = index//9*9
        end = start + 9

        row = self.sudokuValues[start:end]

        return row.count(row[index%9]) <= 1
    
    def checkColumn(self, index: int):
        start = index%9
        column = [self.sudokuValues[i*9+start] for i in range(9)]
        
        return column.count(self.sudokuValues[index]) <= 1
    
    def checkSquare(self, index : int):
        #checks the 3x3 grid, where the respective value is located
        row = index % 9 // 3
        column = index // 9 // 3
        squareValues = []
        #for loop to add respective grid values to check list
        for i in range(3):
            for j in range(3):
                currentIndex = (row * 3) + i + (column * 3 + j) * 9
                squareValues.append(self.sudokuValues[currentIndex])

        return squareValues.count(self.sudokuValues[index]) <= 1
    
    @property
    def iterationCounter(self):
        return self.__iterationCounter



    
        
 