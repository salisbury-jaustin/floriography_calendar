from __future__ import print_function
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import datetime
import re
import exception
import calendar
import datetime
import pickle
import os.path
import tkinter as tk
class Submit():
    ''' Submit class creates an object to store and manipulates user input data for booking wedding events '''
    # class regular expressions for input validation
    dateRegex = re.compile(r'(\d{4})-(\d{2})-(\d{2})')
    timeRegex = re.compile(r'(\d{2}):(\d{2})')
    emailRegex = re.compile('^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$')

    def __init__(self, master):
        ''' initialize object of class Submit.
        master refers to the window that is to contain an instance of the class.
        by default all values are set to NULL, getter and setter methods are used to retrieve data and assign values '''
        self.entryList = []
        self.mainEvent = {}
        self.importantDates = []
        self.errorOutput = []

        self.master = master
        self.summary = ''
        self.location = '' 
        self.description = ''
        self.timeStart = ''
        self.timeEnd = ''
        self.email = ''
        self.weddingDate = ''
        self.bookDate = ''
        
    # gets user input data from tk.entry objects and assigns values to instance variables
    def getEntries(self, e1, e2, e3, e4, e5, e6, e7, e8):
        self.summary = e1.get()
        self.location = e2.get()
        self.weddingDate = e3.get()
        self.timeStart = e4.get()
        self.timeEnd = e5.get()
        self.description = e6.get()
        self.email = e7.get()
        self.bookDate = e8.get()
    # appends self.entryList with user input values given that user input passes input validation criteria
    def setEntryList(self):
        # dateTimeStart and dateTimeEnd are method variables used combine date and time inputs into a single string
        dateTimeStart = ''
        dateTimeEnd = ''
        # method variables that store regular expression match-objects (Mo)
        weddingDateMo = self.dateRegex.search(self.weddingDate)
        timeStartMo = self.timeRegex.search(self.timeStart)
        timeEndMo = self.timeRegex.search(self.timeEnd)
        emailMo = self.emailRegex.search(self.email)
        bookDateMo = self.dateRegex.search(self.bookDate)

        # insures that self.entryList is null each time the method is called
        if self.entryList != []:
            self.entryList = []

        # append self.entryList w/ self.summary if user input values are valid
        # if input is invalid, error messages are stored in self.errorOutput
        try:
            self.entryList.append(self.summary) 
            if self.summary == '':
                raise exception.InputError
        except exception.InputError:
            # method variable containing error message
            summaryMessage = 'Event name is required. Please re-enter.'
            # append self.errorOutput with the error message
            self.errorOutput.append(summaryMessage)

        # append self.entryList w/ self.location if user input values are valid
        try:
            self.entryList.append(self.location)
            if self.location == '':
                raise exception.InputError
        except exception.InputError:
                # method variable containing error message
                locationMessage = 'Event location is required. Please re-enter.'
                # append self.errorOutput with the error message
                self.errorOutput.append(locationMessage)

        # append self.entryList with weddingDate if user input values are valid
        try:
            self.entryList.append(self.weddingDate)
            if weddingDateMo == None:
                raise exception.InputError
            elif weddingDateMo != None:  
                weddingDateList = list(weddingDateMo.groups())
                weddingDateList = [int(i) for i in weddingDateList]
                # insures month of wedding date is a value between 1 and 13
                if weddingDateList[1] <= 0 or weddingDateList[1] >= 13:
                    raise exception.InputError
                # inusures that the wedding date day is not less than zero OR greater than the No. of days in a given month
                else:
                    lastDayofMonthWedding = calendar.monthrange(weddingDateList[0], weddingDateList[1])
                    lastDayofMonthWedding = lastDayofMonthWedding[1]
                    if weddingDateList[2] <= 0 or weddingDateList[2] > lastDayofMonthWedding:
                        raise exception.InputError
        except exception.InputError:
            #method variable containing error message
            weddingDateMessage = 'Incorrect date format. Please re-enter wedding date.'
            # append self.errorOutput with the error message
            self.errorOutput.append(weddingDateMessage)

        # transforms self.timeStart to dateTimeStart
        # dateTimeStart is properly formatted to sync with google calendar
        # appends self.entryList w/ the method variable dateTimeStart
        try:
            '''method variable storing concatenation of:
            'T' to demarcate 'Time'
            self.timeStart
            timezone'''
            timeStart = 'T' + self.timeStart + ':00-06:00'
            # method variable concatenates self.weddingDate and method variable timeStart
            dateTimeStart = self.weddingDate + timeStart
            self.entryList.append(dateTimeStart)
            if timeStartMo == None:
                raise exception.InputError
            elif timeStartMo != None:
                # converts matchobject groups from tuple to list
                timeStartList = list(timeStartMo.groups())
                timeStartList = [int(i) for i in timeStartList]
                # insures time in hours is >= 0 OR less than 23 (24hr time format)
                if timeStartList[0] < 0 or timeStartList[0] > 23:
                    raise exception.InputError
                # insures time in minutes is between 0 and 59
                elif timeStartList[1] < 0 or timeStartList[1] > 59:
                    raise exception.InputError
        except exception.InputError:
            # method variable containing error message
            dateTimeStartMessage = 'Incorrect time format. Please re-enter start time.'
            # append self.errorOutput with error message
            self.errorOutput.append(dateTimeStartMessage)

        # transforms self.timeEnd to dateTimeEnd
        # dateTimeEnd is properly formatted to sync with google calendar
        # appends self.entryList w/ the method variable dateTimeEnd
        try:
            '''method variable storing concatenation of:
            'T' to demarcate 'Time'
            self.timeEnd
            timezone'''
            timeEnd = 'T' + self.timeEnd + ':00-06:00'
            # method variable concatenates self.weddingDate and method variable timeEnd
            dateTimeEnd = self.weddingDate + timeEnd
            self.entryList.append(dateTimeEnd)
            if timeEndMo == None:
                raise exception.InputError
            elif timeEndMo != None:
                # converts matchobject groups from tuple to list
                timeEndList = list(timeEndMo.groups())
                timeEndList = [int(i) for i in timeEndList]
                # insures time in hours is >= 0 OR less than 23 (24hr time format)
                if timeEndList[0] < 0 or timeEndList[0] > 23:
                    raise exception.InputError
                # insures time in minutes is between 0 and 59
                elif timeEndList[1] < 0 or timeEndList[1] > 59:
                    raise exception.InputError
                # insures end time does not come before start time
                elif timeEndList[0] < timeStartList[0]:
                    raise exception.InputError
                elif timeEndList[0] == timeStartList[0] and timeEndList[1] < timeStartList[1]:
                    raise exception.InputError
        except exception.InputError:
            # method variable containing error message
            dateTimeEndMessage = 'Incorrect time format OR end time specified was before the start time. Please re-enter end time.' 
            # append self.errorOutput with error message
            self.errorOutput.append(dateTimeEndMessage)

        # append self.entryList with self.description if user input values are valid
        try:
            self.entryList.append(self.description)
            if self.description == '':
                raise exception.InputError
        except exception.InputError:
            # method variable containing error message
            descriptionMessage = 'Event description is required. Please re-enter.'
            # append self.errorOutput with error message
            self.errorOutput.append(descriptionMessage)

        # append self.entryList with self.email if user input values are valid
        try:
            self.entryList.append(emailMo)
            if emailMo == None:
                raise exception.InputError
        except exception.InputError:
            # method variable containing error message
            emailMessage = 'Invalid email address. Please re-enter email address.'
            # append self.errorOutput with error message
            self.errorOutput.append(emailMessage)

        # append self.entryList with self.bookDate if user input values are valid
        try:
            self.entryList.append(self.bookDate)
            if bookDateMo == None:
                raise exception.InputError
            else:  
                # converst matchobject groups from tuple to list
                bookDateList = list(bookDateMo.groups())
                bookDateList = [int(i) for i in bookDateList]
                # insures date month is a value between 1 and 12 
                if bookDateList[1] <= 0 or bookDateList[1] >= 13:
                    raise exception.InputError
                # insures date day is > 0 and no greater than the number of days in a given month
                else:
                    lastDayofMonthBook = calendar.monthrange(bookDateList[0], bookDateList[1])
                    lastDayofMonthBook = lastDayofMonthBook[1]
                    if bookDateList[2] <= 0 or bookDateList[2] > lastDayofMonthBook:
                        raise exception.InputError
        except exception.InputError:
            # method variable containing error message
            bookDateMessage = 'Incorrect date format. Please re-enter date booked.'
            # appens self.errorOutput with error message
            self.errorOutput.append(bookDateMessage)

    # method gets self.entryList values
    def getEntryList(self):
        return self.entryList

    # method gets self.errorOutput values
    def getErrorOutput(self):
        return self.errorOutput

    # method sets the values of self.mainEvent using data from in self.entryList 
    def setMainEvent(self):
        self.mainEvent = {
            'summary': self.entryList[0],
            'location': self.entryList[1],
            'description': self.entryList[5],
            'start': {
                'dateTime': self.entryList[3],
                'timeZone': 'America/Chicago',
                },
            'end': {
                'dateTime': self.entryList[4],
                'timeZone': 'America/Chicago',
                },
            'attendees': [
                {'email': self.entryList[6]},
                ]
            }

    # method gets self.mainEvent values
    def getMainEvent(self):
        return self.mainEvent

    '''calculates important dates in the lead up to the main event(wedding),
    transforms self.weddingDate into a list of importatn dates and stores values in self.importantDates.
    each item in the list is a dictionary of event parameters formatted for syncing to google calendar'''
    def setImportantDates(self):
        # creates weddingDate and bookDate variables of type <class 'datetime.date'> to allow for date.timedelta() calculations
        weddingDateMo= self.dateRegex.search(self.weddingDate)
        weddingDateIntList = [int(i) for i in weddingDateMo.groups()]
        year, month, day = weddingDateIntList
        weddingDate = datetime.date(year, month, day)

        bookDateMo = self.dateRegex.search(self.bookDate)
        bookDateIntList = [int(i) for i in bookDateMo.groups()]
        year, month, day = bookDateIntList
        bookDate = datetime.date(year, month, day)
        
        # calculates a list of important dates
        importantDates = [
                ((bookDate + (weddingDate - bookDate)/2) - datetime.timedelta(weeks=2)),
                (bookDate + (weddingDate - bookDate)/2),
                (weddingDate - datetime.timedelta(days=75)),
                (weddingDate - datetime.timedelta(days=44)),
                (weddingDate - datetime.timedelta(weeks=4)),
                (weddingDate - datetime.timedelta(weeks=3))
                ]
        # converts importantDates datetime.date objects to strings using dateTimeObj.strftime()
        importantDates = [i.strftime('%Y-%m-%d') for i in importantDates]

        # list of reminders for important dates
        twoWeeksTilHalfway = 'second payment reminder for' + ' ' + self.summary
        halfWay = 'second payment due for' + ' ' + self.summary
        seventyFiveDays = 'schedule design meeting for' + ' ' + self.summary
        fortyFourDays = 'send final payment reminder for' + ' ' + self.summary 
        oneMonth = 'final payment due for' + ' ' + self.summary + ' ' + '(order flowers)'
        threeWeeks = 'send questionnaire for' + ' ' + self.summary
        reminders = [
                twoWeeksTilHalfway,
                halfWay,
                seventyFiveDays,
                fortyFourDays,
                oneMonth,
                threeWeeks
                ]
        # create a dict reminderDate{} with items from importantDates[] and reminders[]
        reminderDate = {}
        for i, x in zip(importantDates, reminders):
            reminderDate.setdefault(i, x)

        # create events for k, v in reminderDate.items() and pass to service.events() from google calender api
        # each event acts as a reminder for certain dates leading up to the event/wedding
        for k, v in reminderDate.items():
                event = {
                'summary': v,
                'start': {
                    'date': k,
                    'timeZone': 'America/Chicago',
                    },
                'end': {
                    'date': k,  
                    'timeZone': 'America/Chicago',
                    }
                }      
                self.importantDates.append(event)

    # method gets self.importantDates values 
    def getImportantDates(self):
        return self.importantDates

    # method syncs all events to a users google calendar
    def createEvents(self):
        """Shows basic usage of the Google Calendar API.
        """
        # If modifying these scopes, delete the file token.pickle.
        SCOPES = ['https://www.googleapis.com/auth/calendar']
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        # create the service variable
        service = build('calendar', 'v3', credentials=creds)

        # Call the Calendar API
        now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time

        # adds self.mainEvent to calendar
        event = service.events().insert(calendarId='primary', body=self.mainEvent).execute()
        print('Event created: %s' % (event.get('htmlLink')))

        # adds all values in self.importantDates to calendar
        for i in self.importantDates:
            event = service.events().insert(calendarId='primary', body=i).execute()
            print('Event created: %s' % (event.get('htmlLink')))

    # method for creating and syncing events to calendar
    def syncCalendar(self):
        '''combines methods used to create and sync events to google calendar.
        intended to be used as a command for a tk.Button object.
        if statement insures that there are not error messages in self.errorOutput before creating and syncing events'''
        if self.errorOutput == []:
            self.setMainEvent()
            self.setImportantDates()
            self.createEvents()
    # method for clearing Submit class variables using a tk.Button object
    def clear(self):
        self.entryList = []
        self.mainEvent = {}
        self.importantDates = []
        self.errorOutput = []

        self.summary = ''
        self.location = '' 
        self.description = ''
        self.timeStart = ''
        self.timeEnd = ''
        self.email = ''
        self.weddingDate = ''
        self.bookDate = ''
            

