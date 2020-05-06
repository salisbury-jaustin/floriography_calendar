import tkinter as tk
import submit
import install
class MainWindow:
    ''' MainWindow initializes the master window and defines newWindow() method for creating subsequent toplevel windows'''
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master)
        # creates a Button which opens a new window for booking wedding events
        self.bookButton = tk.Button(self.frame, text='Book', width=25, command=self.newWindow)
        self.bookButton.pack()
        # creates a Button which installs/upgrades dependencies using the class Install
        self.depButton = tk.Button(self.frame, text='Install/Update', width=25, command=install.Install)
        self.depButton.pack()
        self.frame.pack()
    def newWindow(self):
        ''' defines behaviour of new windows '''
        self.newWindow = tk.Toplevel(self.master)
        self.app = BookWindow(self.newWindow)

class BookWindow:
    ''' BookWindow initializes a toplevel window and handles:
    user input, input validation, and syncing data to google calendar '''
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master) 
        # creates tk.Entry objects for user query and data collection
        self.e1 = makeEntry(self.master, 'Event Name: ')
        self.e1.pack()
        self.e2 = makeEntry(self.master, 'Event Location: ')
        self.e2.pack()
        self.e3 = makeEntry(self.master, 'Date: ')
        self.e3.pack()
        self.e4 = makeEntry(self.master, 'Start Time: ')
        self.e4.pack()
        self.e5 = makeEntry(self.master, 'End Time: ')
        self.e5.pack()
        self.e6 = makeEntry(self.master, 'Description: ')
        self.e6.pack()
        self.e7 = makeEntry(self.master, 'Contact Email Address: ')
        self.e7.pack()
        self.e8 = makeEntry(self.master, 'Date Booked: ')
        self.e8.pack()
        # creates an instance of class Submit to store data when the submit button is clicked
        self.submitCommand = submit.Submit(self.master)
        ''' creates a tk.button that handles:
        1. getting data from tk.entry fields
        2. storing data in Submit.entryList variable
        3. displaying user input errors to a tk.text object named self.output'
        4. calculates additional dates and syncs dates to google calendar '''
        self.submitButton = tk.Button(self.frame, text='Submit', width=25, command=lambda:[
            self.submitCommand.getEntries(self.e1, self.e2, self.e3, self.e4, self.e5, self.e6, self.e7, self.e8),
            self.submitCommand.setEntryList(),
            self.output.insert(tk.END, '\n'.join(self.submitCommand.getErrorOutput())),
            self.submitCommand.syncCalendar()])
        self.submitButton.pack()
        # creates the tk.Text object self.output for displaying user input errors
        self.output = tk.Text(self.master, width=90, height=20, wrap=tk.WORD, background='light blue')
        self.output.pack()
        # creates a tk.Button for clearing tk.entry fields and sets instance variables of self.submitCommand to NULL 
        self.clearButton = tk.Button(self.frame, text='Clear', width=25, command=lambda:[
            self.output.delete(0.0, tk.END),
            self.e1.delete(0, 'end'),
            self.e2.delete(0, 'end'),
            self.e3.delete(0, 'end'),
            self.e4.delete(0, 'end'),
            self.e5.delete(0, 'end'),
            self.e6.delete(0, 'end'),
            self.e7.delete(0, 'end'),
            self.e8.delete(0, 'end'),
            self.submitCommand.clear()])
        self.clearButton.pack()
        # quits the bookWindow
        self.quitButton = tk.Button(self.frame, text='Quit', width=25, command=self.close_windows)
        self.quitButton.pack()
        self.frame.pack()
    def close_windows(self):
        self.master.destroy()

# function for making tk.entry object initialization less verbose
def makeEntry(parent, caption):
    caption = tk.Label(parent, text=caption).pack()
    entry = tk.Entry(parent)
    entry.pack()
    return entry
# executes MainWindow loop for GUI
def main(): 
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()
# calls main() 
if __name__ == '__main__':
    main()
