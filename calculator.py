'''

A basic implamentation of a scientific calculator but with added support for graphs and data set formulas.
This program requires the tkinter, math, typing, time, csv, threading and re library (part of standard lib) aswell as
matplotlib (https://matplotlib.org). Matplotlib can be installed with pip via the command 'pip install matplotlib'

'''

from tkinter import Tk, Label, Button, Entry
from tkinter.filedialog import askopenfilename
from math import sqrt, e
from matplotlib.pyplot import plot, ylabel, xlabel, show
from threading import Thread
from typing import List, Dict, Tuple
from time import sleep
from csv import reader
from re import findall, search
from random import randrange

class InvalidFileExtension(Exception): pass
class DevDidSomethingFunky(Exception): pass

def createCodeDetectedWindow() -> None: #in dev
    def closeWindowOnTimer() -> None:
        sleep(randrange(4,8))
        detectedWindow.destroy()
        if randrange(0,101) > 95:
            app.destroy()
            exit()

    detectedWindow = Tk()
    detectedWindow.title("NUH UH")
    detectedWindow.geometry("1250x200")
    detectedWindow.resizable(width = False, height = False)
    Label(detectedWindow, text = "you were trying to input python code to break my program \n NUH UH!!", font = ("Arial", 35)).place(x = 20, y = 20)
    Thread(target = closeWindowOnTimer).start()

    detectedWindow.mainloop()

def isProbablyPythonCode(string: str, maxSusDetections: int) -> bool: #in dev
    countOfSuspiciousInstances: int = len(findall("[()]", string)) + len(findall("[{}]", string))
    for rule in ("if", "while", "import", "else", "yield", "for", "match", "case", "as", "from"):
        if search(rule, string): countOfSuspiciousInstances += 1
    return countOfSuspiciousInstances > maxSusDetections

def createDataCalculationWindow() -> None:
    global selectedMode
    selectedMode = "min" #type = str. cant be declared due to global
    def generateError(time: float, string: str) -> None:
        outputLabel.configure(text = "output: _______")
        errorLabel.place(x = 300, y = 370)
        errorLabel.configure(text = string)
        sleep(time)
        errorLabel.place(x = 999, y = 999)

    def sum(data: List[float]) -> float:
        endResult: float = 0
        for item in data: endResult += item
        return endResult
    
    def mean(data: List[float]) -> float:
        endResult: float = 0
        for item in data: endResult += item
        return endResult / len(data)

    def standardDeviation(data: List[float], isPopulation: bool = True) -> float:
        meanVal: float = mean(data)
        endResult: float = 0
        for item in data: endResult += (item - meanVal) ** 2
        if isPopulation: return sqrt(len(data))
        else: return sqrt((len(data) - 1))

    def mode(data: List[float]) -> float:
        counts: Dict[str, int] = {}
        for item in data:
            try: counts[str(item)] += 1
            except Exception: counts[str(item)] = 1
        topIndex: str = list(counts.keys())[0]
        for key, value in counts.items():
            if value > counts[topIndex]: topIndex = key
        return float(topIndex)

    def min(data: List[float]) -> float:
        minIndex: int = 0
        for i, item in enumerate(data):
            if item < data[minIndex]: minIndex = i
        return data[minIndex]

    def max(data: List[float]) -> float:
        maxIndex: int = 0
        for i, item in enumerate(data):
            if item > data[maxIndex]: maxIndex = i
        return data[maxIndex]

    def cleanAndConvertStringToFloat(item: str) -> float:
        endResult: str = ""
        for char in item:
            if char != ' ': endResult += char
        return float(endResult)

    def submitPostProcess(data: List[float], formula: str) -> None:
        match formula:
            case "min": outputLabel.configure(text = "output: " + str(min(data)))
            case "max": outputLabel.configure(text = "output: " + str(max(data)))
            case "mean": outputLabel.configure(text = "output: " + str(mean(data)))
            case "mode": outputLabel.configure(text = "output: " + str(mode(data)))
            case "SD": outputLabel.configure(text = "output: " + str(standardDeviation(data)))
            case "len": outputLabel.configure(text = "output: " + str(len(data)))
            case "ffs":
                #in dev
                outputLabel.configure(text = "output: min = " + str(min(data)) + " max = " + str(max(data)) + " mean = " + str(mean(data)) + " mode = " + str(mode(data)) + " SD = " + str(standardDeviation(data)))
            case _: raise DevDidSomethingFunky()

    def submitFromEntry(data: str, formula: str) -> None:
        if isProbablyPythonCode(data, 5): 
            createCodeDetectedWindow()
            return
        try:
            data = data.split(',')
            for i, item in enumerate(data):
                if item == ',': data.pop(i)
                else: data[i] = cleanAndConvertStringToFloat(item)
        except ValueError: Thread(target = generateError, args = (1.5, "invalid data")).start()
        else: submitPostProcess(data, formula)

    def submitFromCSV() -> None:
        try:
            fileName: str = askopenfilename()
            if fileName[-1] != 'v': raise InvalidFileExtension()
            file = open(fileName, 'r')
            fileContents: List[float | str] | str = next(reader(file))
            fileContents = fileContents.split(',')
            for i, item in enumerate(fileContents): 
                if item == ',': fileContents.pop(i)
                else: fileContents[i] = cleanAndConvertStringToFloat(item)
        except FileNotFoundError: Thread(start = generateError, args = (1.5, "invalid file")).start()
        except InvalidFileExtension: Thread(start = generateError, args = (2.5, "invalid file\nextension must be .csv\n")).start()
        else: submitPostProcess(data, formula)

    def changeSelectedButton(selectedButton: str) -> None:
        global buttons, selectedMode
        buttons[selectedButton].configure(bg = "green")
        keyListConstruct: List[str] = list(buttons.keys())
        keyListConstruct.remove(selectedButton)
        keyList: Tuple[str] = tuple(keyListConstruct)
        for key in keyList: buttons[key].configure(bg = "white")
        del keyList, keyListConstruct
        selectedMode = selectedButton

    dataCalculationWindow = Tk()
    dataCalculationWindow.title("calculate formulas from data")
    dataCalculationWindow.resizable(width = False, height = False)
    dataCalculationWindow.geometry("500x600")
    Label(dataCalculationWindow, text = "calculate formulas from data", bg = "white", relief = "solid", borderwidth = 3, font = ("Arial", 25)).place(x = 50, y = 20)
    dataEntry = Entry(dataCalculationWindow, relief = "solid", borderwidth = 3, font = ("Arial", 20), width = 15)
    dataEntry.place(x = 170, y = 120)
    Button(dataCalculationWindow, text = "submit", font = ("Arial", 15), bg = "white", borderwidth = 3, relief = "solid", command = lambda: submitFromEntry(dataEntry.get(),selectedMode)).place(x = 220, y = 320)
    Label(dataCalculationWindow, text = "enter data:", font = ("Arial", 15)).place(x = 65, y = 125)
    global buttons
    buttons = { #Type = Dict[str, Button]. type hints cant be used as it was declared with the global keyword first
        "min": Button(dataCalculationWindow, text = "min", borderwidth = 3, relief = "solid", bg  ="green",font = ("Arial", 15), command = lambda: changeSelectedButton("min")),
        "max": Button(dataCalculationWindow, text = "max", borderwidth = 3, relief = "solid", bg = "white",font = ("Arial", 15), command = lambda: changeSelectedButton("max")),
        "mean": Button(dataCalculationWindow, text = "mean", borderwidth = 3, relief = "solid", bg = "white",font = ("Arial", 15), command = lambda: changeSelectedButton("mean")),
        "mode": Button(dataCalculationWindow, text = "mode", borderwidth = 3, relief = "solid", bg = "white",font = ("Arial", 15), command = lambda: changeSelectedButton("mode")),
        "SD": Button(dataCalculationWindow, text = "standard Deviation", borderwidth = 3, relief = "solid", bg = "white", font = ("Arial", 15), command = lambda: changeSelectedButton("SD")),
        "len": Button(dataCalculationWindow, text = "length of data", borderwidth = 3, relief = "solid", bg = "white", font = ("Arial", 15), command = lambda: changeSelectedButton("len")),
        "ffs": Button(dataCalculationWindow, text = "five figure summary", borderwidth = 3, relief = "solid", bg = "white", font = ("Arial", 15), command = lambda: changeSelectedButton("ffs"))
    }
    for i, key in enumerate(buttons.keys()): buttons[key].place(x = 50, y = 200 + 50 * i)
    outputLabel = Label(dataCalculationWindow, text = "output: _______", font = ("Arial", 20))
    outputLabel.place(x = 180, y = 195)
    errorLabel = Label(dataCalculationWindow, text = "", font = ("Arial", 25), fg = "red")
    errorLabel.place(x = 999, y = 999)

    dataCalculationWindow.mainloop()

def createPlotWindow() -> None:
    def submit(data: List[float]) -> None:
        plot(data)
        ylabel(yEntry.get())
        xlabel(xEntry.get())
        show()

    def generateError(time: float, string: str) -> None:
        errorLabel.place(x = 300, y = 370)
        errorLabel.configure(text = string)
        sleep(time)
        errorLabel.place(x = 999, y = 999)

    def passFile() -> None:
        def convertToArrOfFloat(arr: List[str]) -> List[float]:
            try:
                for i, item in enumerate(arr):
                    endResult: str | float = ""
                    for char in item:
                        if char != ' ': endResult += char
                    arr[i] = float(endResult)
            except ValueError: return None
            else: return arr

        try: file = open(askopenfilename(title = "Open a file"), 'r')
        except FileNotFoundError: Thread(target = generateError, args = (1.25, "this file is not valid")).start()
        else:
            with file:
                fileData = convertToArrOfFloat(next(reader(file)))
                if fileData is None: Thread(target = generateError, args = (1.5, "invalid data")).start()
                else: submit(fileData)
        
    def plotData() -> None:
        data: List[float] | str = dataEntry.get()
        if isProbablyPythonCode(data, 5): return createCodeDetectedWindow()
        try:
            if len(data) == 1 or len(data) == 0: raise ValueError()
            data = data.split(',')
            for i in range(len(data)): data[i].replace(' ', '')
            for i in range(len(data)): data[i] = float(data[i])
        except ValueError: Thread(target = generateError, args = (1.25, "invalid data")).start()
        else: submit(data)
        
    plotWindow = Tk()
    plotWindow.title("graph data")
    plotWindow.geometry("500x500")
    plotWindow.resizable(height = False, width = False)
    Label(plotWindow,text = "plot data", font = ("Arial", 35), bg = "white", borderwidth = 4, relief = "solid").place(x = 20, y = 20)
    Label(plotWindow, text = "enter data:", font = ("Arial", 25)).place(x = 20, y = 90)
    Label(plotWindow, text = "enter X label:", font = ("Arial", 25)).place(x = 20,y = 190)
    Label(plotWindow, text = "enter Y label:", font = ("Arial", 25)).place(x = 20, y = 290)
    errorLabel = Label(plotWindow, text = "ERROR DETECTED!", fg = "red", font = ("Arial", 25))
    errorLabel.place(x = 999, y = 999)
    dataEntry = Entry(plotWindow, font = ("Arial", 20), borderwidth = 3, relief = "solid", width = 17)
    dataEntry.place(x = 20, y = 140)
    xEntry = Entry(plotWindow, font = ("Arial", 20), borderwidth = 3, relief = "solid", width=14)
    xEntry.place(x = 20, y = 240)
    yEntry = Entry(plotWindow, font = ("Arial", 20), borderwidth = 3, relief = "solid", width = 14)
    yEntry.place(x = 20, y = 340)
    Button(plotWindow, text = "submit", bg = "white", font = ("Arial", 25), borderwidth = 4, relief = "solid", command = plotData).place(x=320,y=120)
    Button(plotWindow, text = "read from file", font = ("Arial", 20), bg = "white", borderwidth = 2, relief = "solid", command = passFile).place(x=290,y=412.5)

    plotWindow.mainloop()

def switchMode() -> None:
    global isDark
    if isDark:
        app.configure(bg = lightHex)
        buttonMode.configure(text = "🌑")
    else:
        app.configure(bg = darkHex)
        buttonMode.configure(text = "☼")
    isDark = not isDark

def addElement(element: str):
    global displayString, inputString, isDisplayingValue, needsCap
    def appendStrings(disp: chr, inp: chr) -> None:
        global displayString, inputString
        displayString += disp
        inputString += inp
    if isDisplayingValue and not useAns:
        output.configure(text = "")
        displayString = ""
        inputString = ""
        isDisplayingValue = False
    match element:
        case '^': appendStrings("^", "**")
        case '*': appendStrings("x",  "*")
        case "(-)":
            appendStrings(" -", "-(")
            needsCap = True
        case '/': appendStrings("÷", "/")
        case _:
            if needsCap and element in ('-', '+', '*', '/', '^'):
                inputString += ")" 
                needsCap = False
            appendStrings(element, element)

    output.configure(text = displayString)
    output.place(x = 170 - len(displayString) * 6.5, y = 120)
    
def equals() -> None:
    global isDisplayingValue, needsCap, inputString
    if needsCap:
        inputString += ")"
        needsCap = False  
    try:
        for i, char in enumerate(displayString):
            if char in ('+','-','*','/','^') and char == displayString[i + 1]: raise Exception()
        if rounding is not None:
            endResult: float | str = str(round(eval(inputString), rounding))
            output.configure(text=endResult)
            output.place(x = 170 - len(endResult) * 6.5, y = 120)
        else:
            endResult: float | str = str(eval(inputString))
            output.configure(text = endResult)
            output.place(x = 170 - len(endResult) * 6.5, y = 120)
    except Exception:
        output.configure(text = "invalid response")
        output.place(x = 85, y = 120)
    isDisplayingValue = True

def createHexWindow() -> None:
    def generateErrorMessage(string: str) -> None:
        errorLabel.configure(text = string)
        errorLabel.place(x = 350, y = 30)
        sleep(1.5)
        errorLabel.place(x = 999, y = 999)
        
    def isValid(hexString: str, isDark: bool) -> None:
        global lightHex, darkHex
        hexString = hexString.lower()
        try:
            if hexString[0] == "#" and len(hexString) == 7:
                for i, character in enumerate(hexString):
                    if character not in ('1','2','3','4','5','6','7','8','9','0','a','b','c','d','e','f') and i != 0: raise Exception()
            else: raise Exception()
        except Exception:
            if isDark: Thread(target = generateErrorMessage, args = ("Error in dark hex",)).start()
            else: Thread(target = generateErrorMessage, args = ("Error in light hex",)).start()
        else:
            if isDark: darkHex = hexString
            else: lightHex = hexString
            
    hexApp = Tk()
    hexApp.resizable(width = False, height = False)
    hexApp.title("change app colours")
    hexApp.geometry("600x300")
    hexApp.configure(bg = "#444444")
    Label(hexApp, text = "light", borderwidth = 4, relief = "solid", font = ("Arial", 35)).place(x = 30, y = 90)
    Label(hexApp, text = "dark", borderwidth=4, relief = "solid", font = ("Arial", 35)).place(x = 30, y = 180)
    Label(hexApp, text = "=", bg = "#444444", font = ("Arial", 95)).place(x = 180, y = 55)
    Label(hexApp, text = "=", bg = "#444444", font = ("Arial", 95)).place(x = 180, y = 155)
    Label(hexApp, text="configure",font=("Arial",35),borderwidth=4,relief="solid").place(x=140,y=20)
    lightEntry = Entry(hexApp, borderwidth = 4, relief = "solid", font = ("Arial", 20), width = 10)
    lightEntry.place(x = 290, y = 102.5)
    darkEntry = Entry(hexApp, borderwidth = 4, relief = "solid", font = ("Arial", 20), width = 10)
    darkEntry.place(x = 290, y = 202.5)
    Button(hexApp, text = 's', font = ("Arial", 25),borderwidth=4,relief="solid",width=3,height=1,bg="green",command=lambda: isValid(lightEntry.get(),False)).place(x = 480, y = 90.5)
    Button(hexApp, text = 's', font = ("Arial", 25), borderwidth = 4, relief = "solid", width = 3, height = 1, bg = "green", command = lambda: isValid(darkEntry.get(), True)).place(x=480,y=192.5)
    errorLabel = Label(hexApp, fg = "red", font = ("Arial", 22), bg = "#444444")
    errorLabel.place(x = 999, y = 999)

    hexApp.mainloop()

def getRounding() -> None:
    global rounding
    try:
        rounding = int(roundEntry.get())
        if rounding < 0: raise ValueError()
    except ValueError: rounding = None

def clearStr() -> None:
    global displayString, inputString
    if len(displayString) != 0:
        displayString = ""
        inputString = ""
        output.configure(text = " _________ ")
        output.place(x = 110, y = 120)

def popLast() -> None:
    global displayString, inputString
    def popBoth(subtractDisp: int, subtractInp: int) -> None:
        global displayString, inputString
        displayString = displayString[:-subtractDisp]
        inputString = inputString[:-subtractInp]
    if len(displayString) != 0 and len(displayString) != 1:
        if (displayString[-1] == "^") or (displayString[-1] != ")" and inputString[-1] == ")"): popBoth(1, 2)
        elif displayString[-1] == "t" or (displayString[-1] and displayString[-2] == " "): popBoth(2, 2)
        else: popBoth(1, 1)
        if len(displayString) != 0:
            output.configure(text = displayString)
            output.place(x = 170 - len(displayString) * 6.5, y = 120)
        else:
            output.configure(text=" _________ ")
            output.place(x = 110, y = 120)
    elif len(displayString) == 1:
        displayString = ""
        inputString = ""
        output.configure(text = " _________ ")
        output.place(x = 110, y = 120)

def switchAns() -> None:
    global useAns
    useAns = not useAns
            
displayString: str = ""
inputString: str = ""
isDisplayingValue: bool = False
needsCap: bool = False
rounding: int = None
index: int = 0
lightHex: str = "#F9FEE4"
darkHex: str = "#444444"
isDark: bool = False
useAns: bool = True

app = Tk()
app.configure(bg = "#F9FEE4")
app.title("calculator")
app.resizable(width = False, height = False)
app.geometry("670x1000")
Label(text = " Calculator ", font = ("Arial", 45), borderwidth = 5, relief = "solid").place(x = 50, y = 10)
output = Label(text = " _________ ", font = ("Arial", 25), relief = "solid", borderwidth = 3)
output.place(x=110,y=120)
Button(text="1", font=("Arial",45), width=3, height=1, borderwidth=2, relief="solid", command=lambda: addElement('1')).place(x=20, y=200)
Button(text="2", font=("Arial",45), width=3, height=1, borderwidth=2, relief="solid", command=lambda: addElement('2')).place(x=140, y=200)
Button(text="3", font=("Arial",45), width=3, height=1, borderwidth=2, relief="solid", command=lambda: addElement('3')).place(x=260, y=200)
Button(text="4", font=("Arial",45), width=3, height=1, borderwidth=2, relief="solid", command=lambda: addElement('4')).place(x=20, y=320)
Button(text="5", font=("Arial",45), width=3, height=1, borderwidth=2, relief="solid", command=lambda: addElement('5')).place(x=140, y=320)
Button(text="6", font=("Arial",45), width=3, height=1, borderwidth=2, relief="solid", command=lambda: addElement('6')).place(x=260, y=320)
Button(text="7", font=("Arial",45), width=3, height=1, borderwidth=2, relief="solid", command=lambda: addElement('7')).place(x=20, y=440)
Button(text="8", font=("Arial",45), width=3, height=1, borderwidth=2, relief="solid", command=lambda: addElement('8')).place(x=140, y=440)
Button(text="9", font=("Arial",45), width=3, height=1, borderwidth=2, relief="solid", command=lambda: addElement('9')).place(x=260, y=440)
Button(text="0", font=("Arial",45), width=3, height=1, borderwidth=2, relief="solid", command=lambda: addElement('0')).place(x=140, y=560)
Button(text="+", font=("Arial",45), width=3, height=1, borderwidth=2, relief="solid", command=lambda: addElement('+')).place(x=20, y=730)
Button(text="-", font=("Arial",45), width=3, height=1, borderwidth=2, relief="solid", command=lambda: addElement('-')).place(x=140, y=730)
Button(text="*", font=("Arial",45), width=3, height=1, borderwidth=2, relief="solid", command=lambda: addElement('*')).place(x=260, y=730)
Button(text="/", font=("Arial",45), width=3, height=1, borderwidth=2, relief="solid", command=lambda: addElement('/')).place(x=20, y=850)
Button(text="^", font=("Arial",45), width=3, height=1, borderwidth=2, relief="solid", command=lambda: addElement('^')).place(x=140, y=850)
Button(text="(", font=("Arial",45), width=3, height=1, borderwidth=2, relief="solid", command=lambda: addElement('(')).place(x=410, y=200)
Button(text=")", font=("Arial",45), width=3, height=1, borderwidth=2, relief="solid", command=lambda: addElement(')')).place(x=410, y=320)
Button(text="√", font=("Arial",45), width=3, height=1, borderwidth=2, relief="solid", command=lambda: addElement('sqrt(')).place(x=410, y=440)
Button(text="e", font=("Arial",45), width=3, height=1, borderwidth=2, relief="solid", command=lambda: addElement('e')).place(x=410, y=560)
Button(text=".", font=("Arial",45), width=3, height=1, borderwidth=2, relief="solid", command=lambda: addElement('.')).place(x=260, y=560)
Button(text="(-)", font=("Arial",45), width=3, height=1, borderwidth=2, relief="solid", command=lambda: addElement('(-)')).place(x=20, y=560)
Button(text="R", font=("Arial",45), width=3, height=1, borderwidth=2, relief="solid", command=getRounding).place(x=410,y=730)
Button(text="G", font=("Arial",45), width=3, height=1, borderwidth=2, relief="solid", command=createPlotWindow).place(x=530,y=730)
Button(text="=", font=("Arial",45), width=3, height=1, borderwidth=2, relief="solid", command=equals).place(x=260,y=850)
Button(text="c", font=("Arial",45), width=3, height=1, borderwidth=2, relief="solid", command=clearStr).place(x=530,y=200)
Button(text="<", font=("Arial",45), width=3, height=1, borderwidth=2, relief="solid", command=popLast).place(x=530,y=320)
Button(text="A", font=("Arial",45), width=3, height=1, borderwidth=2, relief="solid", command=switchAns).place(x=530,y=440)
Button(text="▨", font=("Arial",45), width=3, height=1, borderwidth=2, relief="solid", command=createHexWindow).place(x=540,y=50)
Button(text="D", font=("Arial",45), width=3, height=1, borderwidth=2, relief="solid", command=createDataCalculationWindow).place(x=530,y=850)
roundEntry = Entry(font = ("Arial", 25), borderwidth = 1, relief = "solid")
roundEntry.place(x = 435, y = 860, width = 70)
buttonMode = Button(text = "🌑", font = ("Arial", 45), width = 3, height = 1, borderwidth = 2, relief = "solid", command = switchMode)
buttonMode.place(x = 410, y = 50)

app.mainloop()
exit()
