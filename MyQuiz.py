from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import csv

name = ""
maxQues = 0
activeQues = 0
quesType = []
correctAnswer = []
selectedAnswer = []
quesDesc = []
choice1 = []
choice2 = []
choice3 = []
picFile = []


def openLoginWindow():
    global txtName

    loginWin.title("Login")
    loginWin.geometry("200x100")
    Label(loginWin, text="Name", fg="blue").grid(row=0, column=0)
    txtName = Entry(loginWin)
    txtName.grid(row=0, column=1, pady=10, padx=10)
    Button(loginWin, text="Proceed", command=showMainWin).grid(row=3, column=1, columnspan=2)


def showMainWin():
    global name
    global maxQues
    global activeQues
    global quesType
    global correctAnswer
    global selectedAnswer
    global quesDesc
    global choice1
    global choice2
    global choice3
    global choice4
    global picFile
    global btnPrev
    global btnNext
    name = txtName.get()

    activeQues = 0
    loginWin.destroy()
    tkw.iconify()
    tkw.deiconify()

    Label(tkw, text="Name", fg="blue", anchor=W).place(x=0, y=0, height=25, width=50)
    Label(tkw, text=name, anchor=W).place(x=50, y=0, height=25, width=200)
    maxQues = len(open("questions.csv", "r").readlines()) - 1
    with open("questions.csv", "r") as csvFile:
        quesType = [0] * maxQues
        correctAnswer = [""] * maxQues
        selectedAnswer = [""] * maxQues
        quesDesc = [""] * maxQues
        choice1 = [""] * maxQues
        choice2 = [""] * maxQues
        choice3 = [""] * maxQues
        choice4 = [""] * maxQues
        picFile = [""] * maxQues
        csvReader = csv.reader(csvFile, delimiter=':')
        lineNo = 0
        for row in csvReader:
            if lineNo > 0:
                quesType[lineNo - 1] = int(row[0])
                correctAnswer[lineNo - 1] = row[1]
                quesDesc[lineNo - 1] = row[2]
                choice1[lineNo - 1] = row[3]
                choice2[lineNo - 1] = row[4]
                choice3[lineNo - 1] = row[5]
                choice4[lineNo - 1] = row[6]
                picFile[lineNo - 1] = row[7]
            lineNo += 1
    btnPrev = Button(tkw, text="Prev", command=btnPrevClick)
    btnPrev.place(x=25, y=575, height=25, width=75)
    btnSubmit = Button(tkw, text="Submit", command=btnSubmitClick)
    btnSubmit.place(x=150, y=575, height=25, width=100)
    btnNext = Button(tkw, text="Next", command=btnNextClick)
    btnNext.place(x=300, y=575, height=25, width=75)
    btnPrev["state"] = "disabled"
    btnNext["state"] = "normal"
    cvs.pack()
    displayQues()


def btnPrevClick():
    global activeQues

    activeQues -= 1
    displayQues()


def btnNextClick():
    global activeQues

    activeQues += 1
    displayQues()


def displayQues():
    global btnPrev
    global btnNext
    global labImg
    global choice

    curQuesNoDesc = "QUESTION " + str(activeQues + 1) + " of " + str(maxQues)
    curQuesDesc = quesDesc[activeQues]
    Label(tkw, text=curQuesNoDesc, font=("Arial 12 bold")) \
        .place(x=50, y=50, height=25, width=300)
    Label(tkw, text=curQuesDesc, font=("Arial 10 bold"), anchor=W) \
        .place(x=50, y=75, height=50, width=300)
    cvs.delete("old")
    try:
        labImg
    except NameError:
        print()
    else:
        print(labImg)
        labImg.image = None
        labImg.destroy()
    picOffset = 0
    if ('img/' in picFile[activeQues]):
        picOffset = 200
        picName = picFile[activeQues].replace('img/', '')
        print(picName)
        quesImg = PhotoImage(file="./images/" + picName)
        labImg = ttk.Label(tkw, image=quesImg)
        labImg.image = quesImg
        labImg.place(x=50, y=150, height=150, width=150)

    choice1Desc = "(A)  " + choice1[activeQues]
    choice2Desc = "(B)  " + choice2[activeQues]
    choice3Desc = "(C)  " + choice3[activeQues]
    choice4Desc = "(D)  " + choice4[activeQues]
    choice = StringVar()
    choice.set(None)
    if (selectedAnswer[activeQues] == "A"):
        choice.set("A")
    elif (selectedAnswer[activeQues] == "B"):
        choice.set("B")
    elif (selectedAnswer[activeQues] == "C"):
        choice.set("C")
    elif (selectedAnswer[activeQues] == "D"):
        choice.set("D")
    radChoice1 = Radiobutton(tkw, text=choice1Desc, variable=choice, value="A", command=choiceClick)
    radChoice1.place(x=50, y=(150 + picOffset), height=50, width=300)
    radChoice2 = Radiobutton(tkw, text=choice2Desc, variable=choice, value="B", command=choiceClick)
    radChoice2.place(x=50, y=(200 + picOffset), height=50, width=300)
    radChoice3 = Radiobutton(tkw, text=choice3Desc, variable=choice, value="C", command=choiceClick)
    radChoice3.place(x=50, y=(350 + picOffset), height=50, width=300)
    radChoice4 = Radiobutton(tkw, text=choice4Desc, variable=choice, value="D", command=choiceClick)
    radChoice4.place(x=50, y=(550 + picOffset), height=50, width=300)
    cvs.create_window(50, (150 + picOffset), window=radChoice1, tags="old", anchor=W)
    cvs.create_window(50, (200 + picOffset), window=radChoice2, tags="old", anchor=W)
    cvs.create_window(50, (250 + picOffset), window=radChoice3, tags="old", anchor=W)
    cvs.create_window(50, (300 + picOffset), window=radChoice4, tags="old", anchor=W)

    if (activeQues == 0):
        btnPrev["state"] = "disabled"
        btnNext["state"] = "normal"
    elif ((activeQues + 1) == maxQues):
        btnPrev["state"] = "normal"
        btnNext["state"] = "disabled"
    else:
        btnPrev["state"] = "normal"
        btnNext["state"] = "normal"
    cvs.pack()


def choiceClick():
    selectedAnswer[activeQues] = choice.get()


def btnSubmitClick():
    reply = messagebox.askquestion("Confirm", "Confirm Submitting (Y/N)?")
    if (reply == "yes"):
        submitAnswer()


def submitAnswer():
    savedAnswers = [""] * (maxQues + 1)
    savedAnswers[0] = name
    with open("answer.txt", "a", newline="") as csvFile:
        csvWriter = csv.writer(csvFile, delimiter=':')
        for k in range(1, (maxQues + 1)):
            savedAnswers[k] = selectedAnswer[k - 1]
        csvWriter.writerow(savedAnswers)
    exit()


tkw = Tk()
tkw.title("Knowledge Test")
cvs = Canvas(tkw, width=400, height=600)
tkw.withdraw()

loginWin = Toplevel(tkw)
openLoginWindow()

cvs.pack()
tkw.mainloop()
