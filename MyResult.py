from tkinter import *
import csv


stuName = []
maxQues = 0
maxStu = 0
activeStu = 0
correctAnswer = []
selectedAnswer = []
result = []


def showMainWin():
    global stuName
    global maxQues
    global maxStu
    global correctAnswer
    global selectedAnswer
    global result
    global btnPrev
    global btnNext

    maxQues = len(open("questions.txt").readlines()) - 1
    correctAnswer = [""] * maxQues
    with open("questions.txt") as csvFile:
        csvReader = csv.reader(csvFile, delimiter=':')
        lineNo = 0
        for row in csvReader:
            if (lineNo > 0):
                correctAnswer[lineNo-1] = row[1]
            lineNo += 1

    maxStu = len(open("answer.txt").readlines())
    stuName = [""] * maxStu
    selectedAnswer = [""] * maxStu
    result = [""] * maxStu
    with open("answer.txt") as csvFile:
        csvReader = csv.reader(csvFile, delimiter=':')
        lineNo = 0
        for row in csvReader:
            stuName[lineNo] = row[0]
            strAns = ""
            strResult = ""
            for ans in range(maxQues):
                strAns = strAns +  row[ans+1]
                if (row[ans+1] == correctAnswer[ans]):
                    strResult = strResult + "1"
                else:
                    strResult = strResult + "0"
            selectedAnswer[lineNo] = strAns
            result[lineNo] = strResult
            lineNo += 1

    btnPrev = Button(tkw, text="Prev", command=btnPrevClick)
    btnPrev.place(x=25, y=575, height=25, width=75)
    btnQuit = Button(tkw, text="Quit", command=btnQuitClick)
    btnQuit.place(x=150, y=575, height=25, width=100)
    btnNext = Button(tkw, text="Next", command=btnNextClick)
    btnNext.place(x=300, y=575, height=25, width=75)
    btnPrev["state"] = "disabled"
    btnNext["state"] = "normal"
    cvs.pack()
    displayResult()


def btnPrevClick():
    global activeStu

    activeStu-=1
    displayResult()


def btnNextClick():
    global activeStu

    activeStu+=1
    displayResult()


def displayResult():
    global btnPrev
    global btnNext

    curStuDesc = "Student " + str(activeStu+1) + " of " + str(maxStu)
    curStuName = "NAME : " + stuName[activeStu]
    Label(tkw, text=curStuDesc, font=("Arial 12 bold"))\
        .place(x=50, y=50, height=25, width=300)
    Label(tkw, text=curStuName, font=("Arial 12 bold"))\
        .place(x=50, y=75, height=25, width=300)

    strHeader = "NO  SELECTED  ANSWER  RESULT"
    Label(tkw, text=strHeader, font=("Arial 10 bold"), anchor=W) \
        .place(x=50, y=125, height=25, width=300)
    startY = 150
    countCorrect = 0
    for k in range(maxQues):
        strResult = str(k+1) + ".          " + (selectedAnswer[activeStu])[k] + "              "
        strResult = strResult + correctAnswer[k] + "           "
        if ((result[activeStu])[k] == "1"):
            strResult = strResult + "CORRECT"
            countCorrect+=1
        else:
            strResult = strResult + "WRONG"
        Label(tkw, text=strResult, font=("Arial 10 bold"), anchor=W)\
            .place(x=50, y=(startY + 25 * k), height=25, width=300)
    strStat = str(countCorrect) + "/" + str(maxQues)
    Label(tkw, text=strStat, anchor=W)\
        .place(x=50, y=(startY + 25 * maxQues), height=25, width=300)

    if (activeStu == 0):
        btnPrev["state"] = "disabled"
        btnNext["state"] = "normal"
    elif ((activeStu + 1) == maxStu):
        btnPrev["state"] = "normal"
        btnNext["state"] = "disabled"
    else:
        btnPrev["state"] = "normal"
        btnNext["state"] = "normal"
    cvs.pack()


def btnQuitClick():
    exit()


tkw = Tk()
tkw.title("Test Result")
cvs = Canvas(tkw, width=400, height=600)
showMainWin()
tkw.mainloop()