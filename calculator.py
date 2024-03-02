from tkinter import Tk, Label, Button, Entry
from math import sqrt, e
from matplotlib.pyplot import plot, ylabel, xlabel, show
from threading import Thread
from typing import List
from time import sleep

def createPlotWindow() -> None:
    def generateError() -> None:
        errorLabel.place(x=30,y=425)
        sleep(1.5)
        errorLabel.place(x=999,y=999)
        
    def plotData() -> None:
        data: List[float] | str = dataEntry.get()
        try:
            if len(data) == 1 or len(data) == 0: raise ValueError()
            data = data.split(',')
            for i in range(len(data)): data[i].replace(' ','')
            for i in range(len(data)): data[i] = float(data[i])
        except ValueError:
            Thread(target=generateError).start()
            return
        plot(data)
        ylabel(yEntry.get())
        xlabel(xEntry.get())
        show()
        
    plotWindow = Tk()
    plotWindow.title("graph data")
    plotWindow.geometry("500x500")
    plotWindow.resizable(height=False,width=False)
    Label(plotWindow,text="plot data",font=("Arial",35),bg="white",borderwidth=4,relief="solid").place(x=20,y=20)
    Label(plotWindow,text="enter data:",font=("Arial",25)).place(x=20,y=90)
    Label(plotWindow,text="enter X label:",font=("Arial",25)).place(x=20,y=190)
    Label(plotWindow,text="enter Y label:",font=("Arial",25)).place(x=20,y=290)
    errorLabel = Label(plotWindow,text="ERROR DETECTED!",fg="red",font=("Arial",25))
    errorLabel.place(x=999,y=999)
    dataEntry = Entry(plotWindow,font=("Arial",20),borderwidth=3,relief="solid",width=17)
    dataEntry.place(x=20,y=140)
    xEntry = Entry(plotWindow,font=("Arial",20),borderwidth=3,relief="solid",width=14)
    xEntry.place(x=20,y=240)
    yEntry = Entry(plotWindow,font=("Arial",20),borderwidth=3,relief="solid",width=14)
    yEntry.place(x=20,y=340)
    Button(plotWindow,text="submit",bg="white",font=("Arial",25),borderwidth=4,relief="solid",command=plotData).place(x=320,y=120)

    plotWindow.mainloop()

def switchMode() -> None:
    global isDark
    if isDark:
        isDark = False
        app.configure(bg = lightHex)
        buttonMode.configure(text = "🌑")
    else:
        isDark = True
        app.configure(bg = darkHex)
        buttonMode.configure(text = "☼")
    
def addElement(element: str):
    global displayString, inputString, isDisplayingValue, needsCap
    def appendStrings(disp: chr, inp: chr) -> None:
        global displayString, inputString
        displayString += disp
        inputString += inp
    if isDisplayingValue and not useAns:
        output.configure(text="")
        displayString = ""
        inputString = ""
        isDisplayingValue = False
    if element == "^": appendStrings("^", "**")
    elif element == "*": appendStrings("x",  "*")
    elif element == "(-)":
        appendStrings(" -", "-(")
        needsCap = True
    elif element == "/": appendStrings("÷", "/")
    else:
        if needsCap and element in ('-','+','*','/','^'):
            inputString+=")" 
            needsCap = False
        appendStrings(element, element)
    output.configure(text = displayString)
    output.place(x=170-len(displayString)*6.5,y=120)
    
def equals() -> None:
    global isDisplayingValue, needsCap, inputString
    if needsCap:
        inputString += ")"
        needsCap = False  
    try:
        for i, char in enumerate(displayString):
            if char in ('+','-','*','/','^') and char == displayString[i+1]: raise Exception()
        if rounding is not None:
            endResult: float | str = str(round(eval(inputString),rounding))
            output.configure(text=endResult)
            output.place(x=170-len(endResult)*6.5,y=120)
        else:
            endResult: float | str = str(eval(inputString))
            output.configure(text=endResult)
            output.place(x=170-len(endResult)*6.5,y=120)
    except Exception:
        output.configure(text="invalid response")
        output.place(x=85,y=120)
    isDisplayingValue = True

def createHexWindow() -> None:
    def generateErrorMessage(string: str) -> None:
        errorLabel.configure(text=string)
        errorLabel.place(x=350,y=30)
        sleep(1.5)
        errorLabel.place(x=999,y=999)
        
    def isValid(hexString: str, isDark: bool) -> None:
        global lightHex, darkHex
        hexString = hexString.lower()
        try:
            if hexString[0] == "#" and len(hexString) == 7:
                for i, character in enumerate(hexString):
                    if character not in ('1','2','3','4','5','6','7','8','9','0','a','b','c','d','e','f') and i != 0: raise Exception()
            else: raise Exception()
        except Exception:
            if isDark: Thread(target=generateErrorMessage,args=("Error in dark hex",)).start()
            else: Thread(target=generateErrorMessage,args=("Error in light hex",)).start()
        else:
            if isDark: darkHex = hexString
            else: lightHex = hexString
            
    hexApp = Tk()
    hexApp.resizable(width=False,height=False)
    hexApp.title("change app colours")
    hexApp.geometry("600x300")
    hexApp.configure(bg="#444444")
    Label(hexApp,text="light",borderwidth=4,relief="solid",font=("Arial",35)).place(x=30,y=90)
    Label(hexApp,text="dark",borderwidth=4,relief="solid",font=("Arial",35)).place(x=30,y=180)
    Label(hexApp,text="=",bg="#444444",font=("Arial",95)).place(x=180,y=55)
    Label(hexApp,text="=",bg="#444444",font=("Arial",95)).place(x=180,y=155)
    Label(hexApp,text="configure",font=("Arial",35),borderwidth=4,relief="solid").place(x=140,y=20)
    lightEntry = Entry(hexApp,borderwidth=4,relief="solid",font=("Arial",20),width=10)
    lightEntry.place(x=290,y=102.5)
    darkEntry = Entry(hexApp,borderwidth=4,relief="solid",font=("Arial",20),width=10)
    darkEntry.place(x=290,y=202.5)
    Button(hexApp,text='s',font=("Arial",25),borderwidth=4,relief="solid",width=3,height=1,bg="green",command=lambda: isValid(lightEntry.get(),False)).place(x=480,y=90.5)
    Button(hexApp,text='s',font=("Arial",25),borderwidth=4,relief="solid",width=3,height=1,bg="green",command=lambda: isValid(darkEntry.get(),True)).place(x=480,y=192.5)
    errorLabel = Label(hexApp,fg="red",font=("Arial",22),bg="#444444")
    errorLabel.place(x=999,y=999)

    hexApp.mainloop()

def getRounding() -> None:
    global rounding
    try:
        rounding = int(roundEntry.get())
        if rounding < 0: raise Exception()
    except: rounding = None

def clearStr() -> None:
    global displayString, inputString
    if len(displayString) != 0:
        displayString = ""
        inputString = ""
        output.configure(text=" _________ ")
        output.place(x=110,y=120)

def popLast() -> None:
    global displayString, inputString
    def popBoth(subtractDisp: int, subtractInp: int) -> None:
        global displayString, inputString
        displayString = displayString[:-subtractDisp]
        inputString = inputString[:-subtractInp]
    if len(displayString) != 0 and len(displayString) != 1:
        if (displayString[-1] == "^") or (displayString[-1] != ")" and inputString[-1] == ")"): popBoth(1,2)
        elif displayString[-1] == "t" or (displayString[-1] and displayString[-2] == " "): popBoth(2,2)
        else: popBoth(1,1)
        if len(displayString) != 0:
            output.configure(text = displayString)
            output.place(x=170-len(displayString)*6.5,y=120)
        else:
            output.configure(text=" _________ ")
            output.place(x=110,y=120)
    elif len(displayString) == 1:
        displayString = ""
        inputString = ""
        output.configure(text=" _________ ")
        output.place(x=110,y=120)

def switchAns() -> None:
    global useAns
    if useAns: useAns = False
    else: useAns = True
            
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
app.configure(bg="#F9FEE4")
app.title("calculator")
app.resizable(width=False,height=False)
app.geometry("670x1000")
Label(text=" Calculator ", font=("Arial",45), borderwidth=5, relief="solid").place(x=50,y=10)
output = Label(text=" _________ ", font=("Arial",25), relief="solid", borderwidth=3)
output.place(x=110,y=120)
Button(text="1", font=("Arial",45), width=3, height=1, borderwidth=2, relief="solid", command=lambda: addElement('1')).place(x=20,y=200)
Button(text="2", font=("Arial",45), width=3, height=1, borderwidth=2, relief="solid", command=lambda: addElement('2')).place(x=140,y=200)
Button(text="3", font=("Arial",45), width=3, height=1, borderwidth=2, relief="solid", command=lambda: addElement('3')).place(x=260,y=200)
Button(text="4", font=("Arial",45), width=3, height=1, borderwidth=2, relief="solid", command=lambda: addElement('4')).place(x=20,y=320)
Button(text="5", font=("Arial",45), width=3, height=1, borderwidth=2, relief="solid", command=lambda: addElement('5')).place(x=140,y=320)
Button(text="6", font=("Arial",45), width=3, height=1, borderwidth=2, relief="solid", command=lambda: addElement('6')).place(x=260,y=320)
Button(text="7", font=("Arial",45), width=3, height=1, borderwidth=2, relief="solid", command=lambda: addElement('7')).place(x=20,y=440)
Button(text="8", font=("Arial",45), width=3, height=1, borderwidth=2, relief="solid", command=lambda: addElement('8')).place(x=140,y=440)
Button(text="9", font=("Arial",45), width=3, height=1, borderwidth=2, relief="solid", command=lambda: addElement('9')).place(x=260,y=440)
Button(text="0", font=("Arial",45), width=3, height=1, borderwidth=2, relief="solid", command=lambda: addElement('0')).place(x=140,y=560)
Button(text="+", font=("Arial",45), width=3, height=1, borderwidth=2, relief="solid", command=lambda: addElement('+')).place(x=20,y=730)
Button(text="-", font=("Arial",45), width=3, height=1, borderwidth=2, relief="solid", command=lambda: addElement('-')).place(x=140,y=730)
Button(text="*", font=("Arial",45), width=3, height=1, borderwidth=2, relief="solid", command=lambda: addElement('*')).place(x=260,y=730)
Button(text="/", font=("Arial",45), width=3, height=1, borderwidth=2, relief="solid", command=lambda: addElement('/')).place(x=20,y=850)
Button(text="^", font=("Arial",45), width=3, height=1, borderwidth=2, relief="solid", command=lambda: addElement('^')).place(x=140,y=850)
Button(text="(", font=("Arial",45), width=3, height=1, borderwidth=2, relief="solid", command=lambda: addElement('(')).place(x=410,y=200)
Button(text=")", font=("Arial",45), width=3, height=1, borderwidth=2, relief="solid", command=lambda: addElement(')')).place(x=410,y=320)
Button(text="√", font=("Arial",45), width=3, height=1, borderwidth=2, relief="solid", command=lambda: addElement('sqrt(')).place(x=410,y=440)
Button(text="e", font=("Arial",45), width=3, height=1, borderwidth=2, relief="solid", command=lambda: addElement('e')).place(x=410,y=560)
Button(text=".", font=("Arial",45), width=3, height=1, borderwidth=2, relief="solid", command=lambda: addElement('.')).place(x=260,y=560)
Button(text="(-)", font=("Arial",45), width=3, height=1, borderwidth=2, relief="solid", command=lambda: addElement('(-)')).place(x=20,y=560)
Button(text="R", font=("Arial",45), width=3, height=1, borderwidth=2, relief="solid", command=getRounding).place(x=410,y=730)
Button(text="G", font=("Arial",45), width=3, height=1, borderwidth=2, relief="solid", command=createPlotWindow).place(x=530,y=730)
Button(text="=", font=("Arial",45), width=3, height=1, borderwidth=2, relief="solid", command=equals).place(x=260,y=850)
Button(text="c", font=("Arial",45), width=3, height=1, borderwidth=2, relief="solid", command=clearStr).place(x=530,y=200)
Button(text="<", font=("Arial",45), width=3, height=1, borderwidth=2, relief="solid", command=popLast).place(x=530,y=320)
Button(text="A", font=("Arial",45), width=3, height=1, borderwidth=2, relief="solid", command=switchAns).place(x=530,y=440)
Button(text="▨", font=("Arial",45), width=3, height=1, borderwidth=2, relief="solid", command=createHexWindow).place(x=540,y=50)
roundEntry = Entry(font=("Arial",25),borderwidth=1,relief="solid")
roundEntry.place(x=435,y=870,width=70)
buttonMode = Button(text="🌑", font=("Arial",45), width=3, height=1, borderwidth=2, relief="solid", command=switchMode)
buttonMode.place(x=410,y=50)

app.mainloop()
