from tkinter import *
import csv
from matplotlib import pyplot as plt
import pandas as pd
import numpy as np

stuName = []
stuAge = []
stuGender = []
maxQues = 0
maxStu = 0
activeStu = 0
correctAnswer = []
correctCountList = []
selectedAnswer = []
result = []


def showMainWin():
    global stuName
    global stuAge
    global stuGender
    global lpltName
    global maxQues
    global maxStu
    global correctAnswer
    global correctCountList
    global selectedAnswer
    global result
    global btnPrev
    global btnNext
    global btnGraph
    global btnStats

    maxQues = len(open("questions.csv").readlines()) - 1
    correctAnswer = [""] * maxQues
    with open("questions.csv") as csvFile:
        csvReader = csv.reader(csvFile, delimiter=':')
        lineNo = 0
        for row in csvReader:
            if (lineNo > 0):
                correctAnswer[lineNo - 1] = row[1]
            lineNo += 1

    maxStu = len(open("answer.csv").readlines())
    stuName = [""] * maxStu
    stuAge = [""] * maxStu
    stuGender = [""] * maxStu
    selectedAnswer = [""] * maxStu
    result = [""] * maxStu
    correctCountList = [""] * maxStu
    with open("answer.csv") as csvFile:
        csvReader = csv.reader(csvFile, delimiter=':')
        lineNo = 0

        lpltName = []
        lpltAge = []
        lpltGender = []

        for row in csvReader:
            stuName[lineNo] = row[0]
            stuAge[lineNo] = row[1]
            stuGender[lineNo] = row[2]

            lpltName.append(stuName[lineNo])
            lpltAge.append(stuAge[lineNo])
            lpltGender.append(stuGender[lineNo])

            strAns = ""
            strResult = ""
            correctCount = 0
            for ans in range(maxQues):
                strAns = strAns + row[ans + 6]
                if (row[ans + 6] == correctAnswer[ans]):
                    strResult = strResult + "1"
                    correctCount += 1
                else:
                    strResult = strResult + "0"
            selectedAnswer[lineNo] = strAns
            correctCountList[lineNo] = correctCount
            result[lineNo] = strResult
            lineNo += 1
    btnPrev = Button(tkw, text="Prev", command=btnPrevClick)
    btnPrev.place(x=25, y=575, height=25, width=75)
    btnQuit = Button(tkw, text="Quit", command=btnQuitClick)
    btnQuit.place(x=150, y=575, height=25, width=100)
    btnNext = Button(tkw, text="Next", command=btnNextClick)
    btnNext.place(x=300, y=575, height=25, width=75)
    btnGraph = Button(tkw, text="Graph", command=btnGraphClick)
    btnGraph.place(x=280, y=525, height=25, width=100)
    btnPrev["state"] = "disabled"
    btnNext["state"] = "normal"
    cvs.pack()
    displayResult()


def btnPrevClick():
    global activeStu

    activeStu -= 1
    displayResult()


def btnNextClick():
    global activeStu
    activeStu += 1
    displayResult()


def displayResult():
    global btnPrev
    global btnNext

    curStuDesc = "Student " + str(activeStu + 1) + " of " + str(maxStu)
    curStuName = "Name: " + stuName[activeStu]
    curStuAge = "Age: " + stuAge[activeStu]
    curStuGender = "Gender: " + stuGender[activeStu]
    Label(tkw, text=curStuDesc, font=("Arial 12 bold"), anchor=W) \
        .place(x=50, y=50, height=25, width=300)
    Label(tkw, text=curStuName, font=("Arial 12 bold"), anchor=W) \
        .place(x=50, y=75, height=25, width=300)
    Label(tkw, text=curStuAge, font=("Arial 12 bold"), anchor=W) \
        .place(x=50, y=100, height=25, width=300)
    Label(tkw, text=curStuGender, font=("Arial 12 bold"), anchor=W) \
        .place(x=50, y=125, height=25, width=300)

    strHeader = "NO  SELECTED  ANSWER  RESULT"
    Label(tkw, text=strHeader, font=("Arial 10 bold"), anchor=W) \
        .place(x=50, y=150, height=25, width=300)
    startY = 175
    countCorrect = 0
    for k in range(maxQues):
        strResult = str(k + 1) + ".          " + (selectedAnswer[activeStu])[k] + "              "
        strResult = strResult + correctAnswer[k] + "           "
        if ((result[activeStu])[k] == "1"):
            strResult = strResult + "CORRECT"
            countCorrect += 1
        else:
            strResult = strResult + "WRONG"
        Label(tkw, text=strResult, font=("Arial 10 bold"), anchor=W) \
            .place(x=50, y=(startY + 25 * k), height=25, width=300)
    correctCountList[activeStu] = countCorrect
    strStat = str(countCorrect) + "/" + str(maxQues)
    Label(tkw, text=strStat, anchor=W) \
        .place(x=50, y=(startY + 25 * maxQues), height=25, width=300)
    if countCorrect >= 8:
        strGrade = "Grade: PASS"
    else:
        strGrade = "Grade: FAIL"
    Label(tkw, text=strGrade, anchor=W) \
        .place(x=100, y=(startY + 25 * maxQues), height=25, width=300)

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


def btnGraphClick():
    average = np.mean(correctCountList)
    max = np.max(correctCountList)
    min = np.min(correctCountList)
    plt.subplot(2, 1, 1)
    plt.title("Quiz Marks")
    plt.xlabel("Name")
    plt.ylabel("Score")
    plt.ylim(0, 11)
    plt.plot(lpltName, correctCountList, "rs-")
    plt.subplot(2, 1, 2)
    plt.xlabel("Gender")
    plt.ylim(0, 11)
    plt.bar(["Average", "max", "min"], [average, max, min], color="blue")
    plt.show()

def btnQuitClick():
    exit()


tkw = Tk()
tkw.title("English Test Result")
cvs = Canvas(tkw, width=400, height=600)
showMainWin()
tkw.mainloop()
