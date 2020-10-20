import tkinter
import requests
import matplotlib.pyplot as plt

AllCasesNumber = 0
CurrentDeadNumber = 0
CurrentRecoveryNumber = 0
CurrentCasesNumber = 0
Country = ""
Lamguage = ""
SettingsOpened = False

def configure():

    global Country
    global Language

    try:
        with open("config.cgf", "r") as f:
            config = f.read()
            config = config.split("\n")
            Country = config[0].split(":")[1]

    except:
        with open("config.cgf", "w") as f:
            f.write("Country:None\nLanguage:En")
            configure()

def reloadData():

    global AllCasesNumber
    global CurrentDeadNumber
    global CurrentRecoveryNumber
    global CurrentCasesNumber
    StartText = '<th scope="row"><a href="/wiki/COVID-19_pandemic_in_' + Country + '" title="COVID-19 pandemic in ' + Country + '">' + Country + '</a>'

    with requests.get("https://en.wikipedia.org/wiki/COVID-19_pandemic_by_country_and_territory") as r:
        data = r.text
        indexStart = (data.find(StartText) + len(StartText))
        data = data[indexStart:]
        indexEnd = data.find("<td><sup id=")
        data = data[:indexEnd]
        data = data.split("\n")
        print(data[6].replace("<td>", ""))
        AllCasesNumber = data[2].replace("<td>", "").replace(",", "")
        CurrentDeadNumber = data[4].replace("<td>", "").replace(",", "")
        CurrentRecoveryNumber = data[6].replace("<td>", "").replace(",", "")
        CurrentCasesNumber = int((float(AllCasesNumber) - float(CurrentDeadNumber) - float(CurrentRecoveryNumber)))
        print(AllCasesNumber, CurrentDeadNumber, CurrentRecoveryNumber)

def settingsTabClosing():

    global openSettings
    openSettings = False
    settingsTab.destroy()


def openSettings():

    global openSettings
    global settingsTab
    if openSettings != True:

        settingsTab = tkinter.Tk()
        settingsTab.protocol("WM_DELETE_WINDOW", settingsTabClosing)
        settingsTab.geometry('400x400')
        settingsTab.configure(bg = '#31363B')
        settingsTab.title("Corona Data Settings")
        settingsTab.resizable(False, False)
        openSettings = True

        LanguageIcon = tkinter.PhotoImage(file = r"img/language.png")
        CountryIcon = tkinter.PhotoImage(file = r"img/country.png")

        LanguageEntry = tkinter.Entry(settingsTab, borderwidth = 0)
        LanguageEntry.place(x = 100, y = 100)

        LanguageImg = tkinter.Label(settingsTab, image = LanguageIcon)
        LanguageImg.place(x = 200, y = 100)

def showGUI():

    root = tkinter.Tk()
    root.geometry('800x600')
    root.configure(bg = "#31363B")
    root.resizable(False, False)
    root.title("Corona Data for {}".format(Country))
    root.option_add('*Font', '3')

    CurrentCasesNumber = int((float(AllCasesNumber) - float(CurrentDeadNumber) - float(CurrentRecoveryNumber)))
    labels = ['Recovered', 'Dead', 'Ill']
    sizes = [(int(CurrentRecoveryNumber) / int(AllCasesNumber)),(int(CurrentDeadNumber) / int(AllCasesNumber)),(int(CurrentCasesNumber) / int(AllCasesNumber))]
    colors = ["green", "black", "red"]
    patches, texts = plt.pie(sizes, colors=colors)
    plt.legend(patches, labels)
    plt.axis('equal')
    plt.tight_layout()
    fig = plt.gcf()
    fig.set_size_inches(4,4)
    plt.savefig("plot.png")

    RefreshButtonIcon = tkinter.PhotoImage(file = r"img/reload.png")
    SettingsButtonIcon = tkinter.PhotoImage(file = r"img/settings.png")

    CurrentCasesIcon = tkinter.PhotoImage(file = r"img/current.png")
    DeadCasesIcon = tkinter.PhotoImage(file = r"img/dead.png")
    RecoveryCasesIcon = tkinter.PhotoImage(file = r"img/recovered.png")
    AllCasesIcon = tkinter.PhotoImage(file = r"img/all.png")
    PlotIcon = tkinter.PhotoImage(file = r"plot.png")

    CurrentCasesNumber = int((float(AllCasesNumber) - float(CurrentDeadNumber) - float(CurrentRecoveryNumber)))
    CurrentCasesLabel = tkinter.Label(root, text = "Current Cases: {}".format(CurrentCasesNumber))
    CurrentDeadLabel = tkinter.Label(root, text = "Current Deaths: {}".format(CurrentDeadNumber))
    CurrentRecoveryLabel = tkinter.Label(root, text = "Current Recoveries: {}".format(CurrentRecoveryNumber))
    AllCasesLabel = tkinter.Label(root, text = "All Cases: {}".format(AllCasesNumber))

    PlotImg= tkinter.Label(root, image = PlotIcon)
    PlotImg.place(x = 25, y = 25)
    CurrentCasesImg = tkinter.Label(root, image = CurrentCasesIcon)
    CurrentCasesImg.place(x = 700, y = 50)
    DeadCasesImg = tkinter.Label(root, image = DeadCasesIcon)
    DeadCasesImg.place(x = 700, y = 150)
    RecoveryCasesImg = tkinter.Label(root, image = RecoveryCasesIcon)
    RecoveryCasesImg.place(x = 700, y = 250)
    AllCasesImg = tkinter.Label(root, image = AllCasesIcon)
    AllCasesImg.place(x = 700, y = 350)

    RefreshButton = tkinter.Button(root, command = reloadData, image = RefreshButtonIcon, borderwidth = 0)
    RefreshButton.place(x = 700, y = 500)
    SettingsButton = tkinter.Button(root, command = openSettings, image = SettingsButtonIcon, borderwidth = 0)
    SettingsButton.place(x = 25, y = 500)

    CurrentCasesLabel.place(x = 450, y = 75)
    CurrentDeadLabel.place(x = 450, y = 175)
    CurrentRecoveryLabel.place(x = 450, y = 275)
    AllCasesLabel.place(x = 450, y = 375)

    root.mainloop()

if __name__ == "__main__":

    configure()
    reloadData()
    showGUI()
