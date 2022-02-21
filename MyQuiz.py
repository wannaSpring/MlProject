import tkinter as Tk
import csv
from tkinter import messagebox
from pubsub import pub


class OtherFrame(Tk.Toplevel):
    def __init__(self, name):
        Tk.Toplevel.__init__(self)
        self.geometry("400x600")
        self.title("choose")
        self.cvs = Tk.Canvas(self, width=400, height=600)
        self.name = name
        self.maxQues = 0
        self.activeQues = 0
        self.quesType = []
        self.correctAnswer = []
        self.selectedAnswer = []
        self.quesDesc = []
        self.choice1 = []
        self.choice2 = []
        self.choice3 = []
        self.choice4 = []
        self.choice = ''
        self.picFile = []
        self.btnPrev = ''
        self.btnNext = ''
        self.activeQues = 0
        self.iconify()
        self.deiconify()

        Tk.Label(self, text="Name", fg="blue", anchor=Tk.W).place(x=0, y=0, height=25, width=50)
        Tk.Label(self, text=self.name, anchor=Tk.W).place(x=50, y=0, height=25, width=200)
        self.maxQues = len(open("questions.csv", "r").readlines()) - 1
        with open("questions.csv", "r") as csvFile:
            self.quesType = [0] * self.maxQues
            self.correctAnswer = [""] * self.maxQues
            self.selectedAnswer = [""] * self.maxQues
            self.quesDesc = [""] * self.maxQues
            self.choice1 = [""] * self.maxQues
            self.choice2 = [""] * self.maxQues
            self.choice3 = [""] * self.maxQues
            self.choice4 = [""] * self.maxQues
            self.picFile = [""] * self.maxQues
            csvReader = csv.reader(csvFile, delimiter=':')
            lineNo = 0
            for row in csvReader:
                if lineNo > 0:
                    self.quesType[lineNo - 1] = int(row[0])
                    self.correctAnswer[lineNo - 1] = row[1]
                    self.quesDesc[lineNo - 1] = row[2]
                    self.choice1[lineNo - 1] = row[3]
                    self.choice2[lineNo - 1] = row[4]
                    self.choice3[lineNo - 1] = row[5]
                    self.choice4[lineNo - 1] = row[6]
                    self.picFile[lineNo - 1] = row[7]
                lineNo += 1
        self.btnPrev = Tk.Button(self, text="Prev", command=self.btnPrevClick)
        self.btnPrev.place(x=25, y=575, height=25, width=75)
        self.btnSubmit = Tk.Button(self, text="Submit", command=self.btnSubmitClick)
        self.btnSubmit.place(x=150, y=575, height=25, width=100)
        self.btnNext = Tk.Button(self, text="Next", command=self.btnNextClick)
        self.btnNext.place(x=300, y=575, height=25, width=75)
        self.btnPrev["state"] = "disabled"
        self.btnNext["state"] = "normal"
        self.cvs.pack()
        self.displayQues()

    def btnPrevClick(self):
        self.activeQues -= 1
        self.displayQues()

    def btnNextClick(self):
        self.activeQues += 1
        self.displayQues()

    def displayQues(self):
        global btnPrev
        global btnNext
        global labImg
        global choice
        curQuesNoDesc = "QUESTION " + str(self.activeQues + 1) + " of " + str(self.maxQues)
        curQuesDesc = self.quesDesc[self.activeQues]
        Tk.Label(self, text=curQuesNoDesc, font=("Arial 12 bold")) \
            .place(x=50, y=50, height=25, width=300)
        Tk.Label(self, text=curQuesDesc, font=("Arial 10 bold"), anchor=Tk.W) \
            .place(x=50, y=75, height=50, width=300)
        self.cvs.delete("old")
        try:
            labImg
        except NameError:
            print()
        else:
            labImg.image = None
            labImg.destroy()
        picOffset = 0
        if ('img/' in self.picFile[self.activeQues]):
            picOffset = 200
            picName = self.picFile[self.activeQues].replace('img/', '')
            quesImg = Tk.PhotoImage(file="./images/" + picName)
            labImg = Tk.Label(self, image=quesImg)
            labImg.image = quesImg
            labImg.place(x=50, y=150, height=150, width=150)

        choice1Desc = "(A)  " + self.choice1[self.activeQues]
        choice2Desc = "(B)  " + self.choice2[self.activeQues]
        choice3Desc = "(C)  " + self.choice3[self.activeQues]
        choice4Desc = "(D)  " + self.choice4[self.activeQues]
        self.choice = Tk.StringVar()
        self.choice.set(None)
        if (self.selectedAnswer[self.activeQues] == "A"):
            self.choice.set("A")
        elif (self.selectedAnswer[self.activeQues] == "B"):
            self.choice.set("B")
        elif (self.selectedAnswer[self.activeQues] == "C"):
            self.choice.set("C")
        elif (self.selectedAnswer[self.activeQues] == "D"):
            self.choice.set("D")
        radChoice1 = Tk.Radiobutton(self, text=choice1Desc, variable=self.choice, value="A", command=self.choiceClick)
        radChoice1.place(x=50, y=(150 + picOffset), height=50, width=300)
        radChoice2 = Tk.Radiobutton(self, text=choice2Desc, variable=self.choice, value="B", command=self.choiceClick)
        radChoice2.place(x=50, y=(200 + picOffset), height=50, width=300)
        radChoice3 = Tk.Radiobutton(self, text=choice3Desc, variable=self.choice, value="C", command=self.choiceClick)
        radChoice3.place(x=50, y=(350 + picOffset), height=50, width=300)
        radChoice4 = Tk.Radiobutton(self, text=choice4Desc, variable=self.choice, value="D", command=self.choiceClick)
        radChoice4.place(x=50, y=(550 + picOffset), height=50, width=300)
        self.cvs.create_window(50, (150 + picOffset), window=radChoice1, tags="old", anchor=Tk.W)
        self.cvs.create_window(50, (200 + picOffset), window=radChoice2, tags="old", anchor=Tk.W)
        self.cvs.create_window(50, (250 + picOffset), window=radChoice3, tags="old", anchor=Tk.W)
        self.cvs.create_window(50, (300 + picOffset), window=radChoice4, tags="old", anchor=Tk.W)

        if (self.activeQues == 0):
            self.btnPrev["state"] = "disabled"
            self.btnNext["state"] = "normal"
        elif ((self.activeQues + 1) == self.maxQues):
            self.btnPrev["state"] = "normal"
            self.btnNext["state"] = "disabled"
        else:
            self.btnPrev["state"] = "normal"
            self.btnNext["state"] = "normal"
        self.cvs.pack()

    def choiceClick(self):
        self.selectedAnswer[self.activeQues] = self.choice.get()

    def btnSubmitClick(self):
        reply = messagebox.askquestion("Confirm", "Confirm Submitting (Y/N)?")
        if (reply == "yes"):
            self.submitAnswer()

    def submitAnswer(self):
        pub.sendMessage('submit', answer=self.selectedAnswer)


class ApplicationForm:
    def __init__(self):
        self.name = ''
        self.age = 0
        self.gender = 0
        self.highestQualifications = ''
        self.familyToMove = False
        self.economicLevel = ''


class MyApp(object):
    def __init__(self, parent):
        """Constructor"""
        self.root = parent
        self.root.title("Login")
        self.frame = Tk.Frame(parent)
        self.applicationForm = ApplicationForm()

        Tk.Label(self.root, text="Name:", fg="blue").grid(row=0, sticky=Tk.E)
        self.applicationForm.name = Tk.Entry(self.root)
        self.applicationForm.name.grid(row=0, column=1, sticky=Tk.W)

        Tk.Label(self.root, text="Age:", fg="blue").grid(row=1, sticky=Tk.E)
        self.applicationForm.age = Tk.Entry(self.root)
        self.applicationForm.age.grid(row=1, column=1, sticky=Tk.W)

        Tk.Label(self.root, text="Gender:", fg="blue").grid(row=2, sticky=Tk.E)
        radioValue = Tk.IntVar()
        rdioOne = Tk.Radiobutton(self.root, text='male', variable=radioValue, value=1)
        rdioTwo = Tk.Radiobutton(self.root, text='female', variable=radioValue, value=0)
        self.applicationForm.gender = radioValue
        rdioOne.grid(row=2, column=1)
        rdioTwo.grid(row=2, column=1, sticky=Tk.W)

        Tk.Label(self.root, text="Family want move?", fg="blue").grid(row=4, sticky=Tk.E)
        familyValue = Tk.IntVar()
        familyRdioOne = Tk.Radiobutton(self.root, text='true', variable=familyValue, value=False)
        familyRdioTwo = Tk.Radiobutton(self.root, text='false', variable=familyValue, value=True)
        self.applicationForm.familyToMove = familyValue
        familyRdioOne.grid(row=3, column=1)
        familyRdioTwo.grid(row=3, column=1, sticky=Tk.W)

        Tk.Label(self.root, text="Qualifications:", fg="blue").grid(row=3, sticky=Tk.E)
        hqValue = Tk.IntVar()
        hqRdioOne = Tk.Radiobutton(self.root, text='PhD', variable=hqValue, value=0)
        hqRdioTwo = Tk.Radiobutton(self.root, text='Undergraduate', variable=hqValue, value=1)
        hqRdioThree = Tk.Radiobutton(self.root, text='Masters', variable=hqValue, value=2)
        self.applicationForm.highestQualifications = hqValue
        hqRdioOne.grid(row=4, column=1, sticky=Tk.W, columnspan=4)
        hqRdioTwo.grid(row=4, column=1, sticky=Tk.W, padx=60, columnspan=4)
        hqRdioThree.grid(row=4, column=1, sticky=Tk.W, padx=190, columnspan=4)

        Tk.Label(self.root, text="EconomicLevel:", fg="blue").grid(row=5, sticky=Tk.E)
        eclValue = Tk.IntVar()
        eclRdioOne = Tk.Radiobutton(self.root, text='poor', variable=eclValue, value=0)
        eclRdioTwo = Tk.Radiobutton(self.root, text='normal', variable=eclValue, value=1)
        eclRdioThree = Tk.Radiobutton(self.root, text='rich', variable=eclValue, value=2)
        self.applicationForm.economicLevel = eclValue
        eclRdioOne.grid(row=5, column=1, sticky=Tk.W, columnspan=4)
        eclRdioTwo.grid(row=5, column=1, sticky=Tk.W, padx=60, columnspan=4)
        eclRdioThree.grid(row=5, column=1, sticky=Tk.W, padx=190, columnspan=4)

        Tk.Button(self.root, text="Proceed", command=self.openFrame).grid(row=8, column=1, pady=10,
                                                                          sticky=Tk.W + Tk.E + Tk.N + Tk.S)

        pub.subscribe(self.writeFile, 'submit')

    def writeFile(self, answer):
        newAnswer = [self.applicationForm.name.get(), self.applicationForm.age.get(), self.applicationForm.gender.get(),
                     self.applicationForm.highestQualifications.get(), self.applicationForm.familyToMove.get(),
                     self.applicationForm.economicLevel.get()] + answer
        with open("answer.csv", "a", newline="") as csvFile:
            csvWriter = csv.writer(csvFile, delimiter=':')
            csvWriter.writerow(newAnswer)
        exit()

    def hide(self):
        self.root.withdraw()

    def openFrame(self):
        self.hide()
        subFrame = OtherFrame(self.applicationForm.name.get())

    # ----------------------------------------------------------------------
    def onCloseOtherFrame(self, otherFrame):
        otherFrame.destroy()
        # 过会再看是否保留
        self.show()

    def show(self):
        self.root.update()
        self.root.deiconify()


if __name__ == "__main__":
    root = Tk.Tk()
    root.geometry("400x200")
    app = MyApp(root)
    root.mainloop()
