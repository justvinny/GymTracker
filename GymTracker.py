import tkinter as tk
import tkinter.ttk as ttk
import csv

tempdic = {}

def readfromcsv(lifts):

    with open('data.csv', 'r') as file:
        reader = csv.DictReader(file)
        for a in reader:
            lifts.setdefault(a['Exercise'],
                             {'Weight': a['Weight'], 'Sets': a['Sets'], 'Reps': a['Reps'],
                              'AMRAP': a['AMRAP']})


def writetocsv(lifts):

    with open('data.csv', 'w') as file:
        field = ['Exercise', 'Weight', 'Sets', 'Reps', 'AMRAP']
        writer = csv.DictWriter(file, fieldnames=field)
        writer.writeheader()

        for a, b in lifts.items():
            writer.writerow({'Exercise': a, 'Weight': b[field[1]], 'Sets': b[field[2]],
                             'Reps': b[field[3]], 'AMRAP': b[field[4]]})

def csvtolist():

    boxlist = []

    with open('data.csv', 'r') as file:
        reader = csv.DictReader(file)
        for a in reader:
            boxlist.append(a['Exercise'])

    return boxlist

#FDefining our main loop
def Main():

    root = tk.Tk()
    app = GymTracker(root)
    root.mainloop()

#Class for our main tkinter app
class GymTracker:

    def __init__(self, master):

        self.master = master
        self.config_master()
        self.frame_top()
        self.frame_bottom()

    def config_master(self):

        self.master.title('Gym Tracker')
        self.master.config(bg='black')
        self.master.geometry('400x650')

    #Making the top part of the frame for master
    def frame_top(self):

        self.frameTop = tk.Frame(self.master, bg='white')
        self.frameTop.place(relx=.1, rely=.1, relheight=.2, relwidth=.8)

        self.frame_top_widgets()

    def frame_top_widgets(self):

        templist = csvtolist()
        readfromcsv(tempdic)

        self.F_topTitle = tk.Label(self.frameTop, text='Gym Tracker', bg='white', font=('verdana',14,'bold'),
                                   anchor='n')
        self.F_topTitle.pack(fill=tk.X)

        self.F_topLabel1 = tk.Label(self.frameTop, text=' ', bg='white')
        self.F_topLabel1.pack()

        self.F_topBox = ttk.Combobox(self.frameTop, values=templist)
        self.F_topBox.current(0)
        self.F_topBox.pack()
        self.F_topBox.bind('<<ComboboxSelected>>', self.callback)

        self.F_topLabel2 = tk.Label(self.frameTop, text=' ', bg='white')
        self.F_topLabel2.pack()

    def callback(self,event):

        self.F_topLabel2.config(text='\n' + self.F_topBox.get())

        self.entryWeight.delete(0, 'end')
        self.entrySets.delete(0, 'end')
        self.entryReps.delete(0, 'end')
        self.entryAmrap.delete(0, 'end')

        self.entryWeight.insert(0, tempdic[self.F_topBox.get()]['Weight'])
        self.entrySets.insert(0, tempdic[self.F_topBox.get()]['Sets'])
        self.entryReps.insert(0, tempdic[self.F_topBox.get()]['Reps'])
        self.entryAmrap.insert(0, tempdic[self.F_topBox.get()]['AMRAP'])

    #Making the bottom part of the frame for master
    def frame_bottom(self):

        self.frameBottom = tk.Frame(self.master, bg='white')
        self.frameBottom.place(relx=.1, rely=.35, relheight=.55, relwidth=.8)
        self.F_bot_widgets()

    def F_bot_widgets(self):

        self.labelWeight = tk.Label(self.frameBottom, text='Weight', anchor='e', bg='white')
        self.labelSets = tk.Label(self.frameBottom, text='Sets', anchor='e', bg='white')
        self.labelReps = tk.Label(self.frameBottom, text='Reps', anchor='e', bg='white')
        self.labelAmrap = tk.Label(self.frameBottom, text='AMRAP', anchor='e', bg='white')
        self.entryWeight = tk.Entry(self.frameBottom, bg='white')
        self.entrySets = tk.Entry(self.frameBottom, bg='white')
        self.entryReps = tk.Entry(self.frameBottom, bg='white')
        self.entryAmrap = tk.Entry(self.frameBottom, bg='white')

        self.labelWeight.place(rely=.1, relwidth=.44, relheight=.1)
        self.labelSets.place(rely=.2, relwidth=.44, relheight=.1)
        self.labelReps.place(rely=.3, relwidth=.44, relheight=.1)
        self.labelAmrap.place(rely=.4, relwidth=.44, relheight=.1)
        self.entryWeight.place(rely=.1, relx=.45, relwidth=.25, relheight=.1)
        self.entrySets.place(rely=.2, relx=.45, relwidth=.25, relheight=.1)
        self.entryReps.place(rely=.3, relx=.45, relwidth=.25, relheight=.1)
        self.entryAmrap.place(rely=.4, relx=.45, relwidth=.25, relheight=.1)

        self.labelStatus = tk.Label(self.frameBottom, text=' ', bg='white', width=20)
        self.buttonUpdate = tk.Button(self.frameBottom, text='Update', command=self.updatedict, bg='slategrey')
        self.buttonCurrent = tk.Button(self.frameBottom, text='Current', command=self.currentbox, bg='slategrey')
        self.buttonQuit = tk.Button(self.frameBottom, text='Quit', command=self.master.destroy, bg='slategrey')

        self.labelStatus.place(rely=.7, relwidth=1, relheight=.1)
        self.buttonUpdate.place(rely=.8, relwidth=.5, relheight=.1)
        self.buttonCurrent.place(rely=.8, relx=.5, relwidth=.5,relheight=.1)
        self.buttonQuit.place(rely=.9, relwidth=1, relheight=.1)

    def updatedict(self):

        tempdic[self.F_topBox.get()]['Weight'] = self.entryWeight.get()
        tempdic[self.F_topBox.get()]['Sets'] = self.entrySets.get()
        tempdic[self.F_topBox.get()]['Reps'] = self.entryReps.get()
        tempdic[self.F_topBox.get()]['AMRAP'] = self.entryAmrap.get()

        writetocsv(tempdic)

        self.labelStatus.configure(text=(self.F_topBox.get()+' update success!'), fg='green')

    def currentbox(self):

        currentboxtext = ''

        for a1,a2 in tempdic.items():

            currentboxtext += a1 + ' - ' + a2['Weight'] + ' | ' + a2['Sets'] + ' | ' + a2['Reps'] + ' | ' + a2['AMRAP'] + '\n'

        splitthem = currentboxtext.split('\n')

        currentboxtext = ''

        for a3 in range(1,(len(splitthem))):

            currentboxtext += splitthem[a3] + ' \n'

        self.top = tk.Toplevel()
        self.top.geometry('400x650')
        self.top.configure(bg='black')

        self.topframe = tk.Frame(self.top, bg='white')
        self.topframe.place(relx=.1, rely=.1, relwidth=.8, relheight=.8)

        self.toplabel = tk.Label(self.topframe, text=currentboxtext, bg='white', anchor='s')
        self.toplabel.pack(fill=tk.X)

        self.topButton = tk.Button(self.topframe, text='Back', bg='slategrey', command=self.top.destroy)
        self.topButton.pack(side='bottom', fill=tk.X)


#Initializing our app
if __name__ == '__main__':
    Main()
