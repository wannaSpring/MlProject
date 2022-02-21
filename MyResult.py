from tkinter import *
import csv
from matplotlib import pyplot as plt
import pandas as pd
import numpy as np

applicationName = []
applicationAge = []
applicationGender = []
applicationHq = []
applicationFtm = []
applicationEco = []
maxQues = 0
applicantiLength = 0
activeIndex = 0
correctAnswer = []
correctCountList = []
selectedAnswer = []
result = []


def showMainWin():
    global applicationName
    global applicationAge
    global applicationGender
    global applicationHq
    global applicationFtm
    global applicationEco
    global lpltName
    global maxQues
    global applicantiLength
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

    applicantiLength = len(open("answer.csv").readlines())
    applicationName = [""] * applicantiLength
    applicationAge = [""] * applicantiLength
    applicationGender = [""] * applicantiLength
    applicationHq = [""] * applicantiLength
    applicationFtm = [""] * applicantiLength
    applicationEco = [""] * applicantiLength
    selectedAnswer = [""] * applicantiLength
    result = [""] * applicantiLength
    correctCountList = [0] * applicantiLength
    print(correctCountList)
    with open("answer.csv") as csvFile:
        csvReader = csv.reader(csvFile, delimiter=':')
        lineNo = 0

        lpltName = []
        lpltAge = []
        lpltGender = []
        for row in csvReader:
            applicationName[lineNo] = row[0]
            applicationAge[lineNo] = row[1]
            applicationGender[lineNo] = row[2]
            applicationHq[lineNo] = row[3]
            applicationFtm[lineNo] = row[4]
            applicationEco[lineNo] = row[5]


            lpltName.append(applicationName[lineNo])
            lpltAge.append(applicationAge[lineNo])
            lpltGender.append(applicationGender[lineNo])

            strAns = ""
            strResult = ""
            correctCount = 0
            isCorrect = 0
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
            print(correctCount)
            if correctCount >= 7:
                isCorrect = 1
            with open("data.csv", "a", newline="") as csvFile:
                csvWriter = csv.writer(csvFile, delimiter=',')
                csvWriter.writerow([row[1], row[2], row[3], row[4], row[5]] + [isCorrect])
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
    global activeIndex
    activeIndex -= 1
    displayResult()


def btnNextClick():
    global activeIndex
    activeIndex += 1
    displayResult()


def displayResult():
    global btnPrev
    global btnNext

    curDesc = "Applicant " + str(activeIndex + 1) + " of " + str(applicantiLength)
    curName = "Name: " + applicationName[activeIndex]
    curAge = "Age: " + applicationAge[activeIndex]
    curGender = "Gender: " + applicationGender[activeIndex]
    Label(tkw, text=curDesc, font=("Arial 12 bold"), anchor=W) \
        .place(x=50, y=50, height=25, width=300)
    Label(tkw, text=curName, font=("Arial 12 bold"), anchor=W) \
        .place(x=50, y=75, height=25, width=300)
    Label(tkw, text=curAge, font=("Arial 12 bold"), anchor=W) \
        .place(x=50, y=100, height=25, width=300)
    Label(tkw, text=curGender, font=("Arial 12 bold"), anchor=W) \
        .place(x=50, y=125, height=25, width=300)

    strHeader = "NO  SELECTED  ANSWER  RESULT"
    Label(tkw, text=strHeader, font=("Arial 10 bold"), anchor=W) \
        .place(x=50, y=150, height=25, width=300)
    startY = 175
    countCorrect = 0
    for k in range(maxQues):
        strResult = str(k + 1) + ".          " + (selectedAnswer[activeIndex])[k] + "              "
        strResult = strResult + correctAnswer[k] + "           "
        if ((result[activeIndex])[k] == "1"):
            strResult = strResult + "CORRECT"
            countCorrect += 1
        else:
            strResult = strResult + "WRONG"
        Label(tkw, text=strResult, font=("Arial 10 bold"), anchor=W) \
            .place(x=50, y=(startY + 25 * k), height=25, width=300)
    correctCountList[activeIndex] = countCorrect
    strStat = str(countCorrect) + "/" + str(maxQues)
    Label(tkw, text=strStat, anchor=W) \
        .place(x=50, y=(startY + 25 * maxQues), height=25, width=300)
    if countCorrect >= 7:
        strGrade = "Grade: PASS"
    else:
        strGrade = "Grade: FAIL"
    Label(tkw, text=strGrade, anchor=W) \
        .place(x=100, y=(startY + 25 * maxQues), height=25, width=300)

    if (activeIndex == 0):
        btnPrev["state"] = "disabled"
        btnNext["state"] = "normal"
    elif ((activeIndex + 1) == applicantiLength):
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
