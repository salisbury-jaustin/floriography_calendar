''' query.py contains a single function: query()
    query() is to be called as a module by the script: event.py
    The query.py can be run by itself for the purpose of debugging
'''

import datetime
import re
import calendar
import pyinputplus as pyip

# query() takes user-input regarding wedding event details and returns a list called eventList
def query():

    # creates regex for date and time for preventing date/time input formatting errors
    dateRegex = re.compile(r'(\d{4})-(\d{2})-(\d{2})')
    timeRegex = re.compile(r'(\d{2}):(\d{2})')

    # user queries for event, location, description, wedding date, start and end time, email, and date booked
    # are defined below
    #
    # query for event name w/ input validation
    while True:
        print('Event:')
        summary = input()

        # if loop checks for input, input is required
        if summary == '':
            print('Event summary is required. Please Re-enter.')
            continue
        else:
            break

    # query for event location w/ input validation
    while True:
        print('Location:')
        location = input()
        
        # if loop checks for input, input is required
        if location == '':
            print('Event location is required. Please Re-enter.')
            continue
        else:
            break

    # query for event description w/ input validation
    while True:
        print('Description:')
        description = input()

        # if loop checks input, input is required
        if description == '':
            print('Event description is required. Please Re-enter.')
            continue
        else:
            break

    # query for wedding date w/ input validation
    while True:
        print('Wedding Date (yyyy-mm-dd):')
        weddingDate = input()

        # create date match object using dateRegex
        dateMo = dateRegex.search(weddingDate)
        
        # if loop checks for correct formatting of user input for wedding date
        if dateMo == None:
            print('Incorrect Format, Please Re-enter Wedding Date.')
            continue
        else:  
            # convert dateMo tuple to list
            dateList = list(dateMo.groups())

            # convert dateList values to integers
            dateList = [int(i) for i in dateList]

            if dateList[1] <= 0 or dateList[1] >= 13:
                print('Incorrect Format, Please Re-enter Wedding Date.')
                continue
            else:
                # create last day of month variable
                lastDayofMonth = calendar.monthrange(dateList[0], dateList[1])
                lastDayofMonth = lastDayofMonth[1]

                if dateList[2] <= 0 or dateList[2] > lastDayofMonth:
                    print('Incorrect Format, Please Re-enter Wedding Date.')
                    continue
                else:
                    break

    # query for start time w/ input validation 
    while True:
        print('Start Time (hh:mm 24hr format):')
        timeStart = input()

        # create start time match object using timeRegex
        timeStartMo = timeRegex.search(timeStart)

        # if loop checks for correct formatting of user input for start time
        if timeStartMo == None:
            print('Incorrect Format, Please Re-enter start time.')
            continue
        elif timeStartMo != None:
            # convert startTimeMo tuple to list
            timeStartList = list(timeStartMo.groups())
            # convert startTimeList values to integers
            timeStartList = [int(i) for i in timeStartList]
            if timeStartList[0] < 0 or timeStartList[0] > 23:
                print('Incorrect Format, Please Re-enter start time.')
                continue
            elif timeStartList[1] < 0 or timeStartList[1] > 59:
                print('Incorrect Format, Please Re-enter start time.')
                continue
            else:
                break

    # formats timeStart for input into google calendar api
    timeStart = 'T' + timeStart + ':00-06:00'
    dateTimeStart = weddingDate + timeStart

    # query for end time w/ input error prevention 
    while True:
        print ('End Time (hh:mm 24hr format):')
        timeEnd = input()

        # create end time match object using timeRegex
        timeEndMo = timeRegex.search(timeEnd)

        # if loop checks for correct formatting of user input for end time AND if end time is before start time 
        if timeEndMo == None:
            print('Incorrect Format: Please Re-enter end time.')
            continue
        elif timeEndMo != None:
            # convert endTimeMo tuple to list
            timeEndList = list(timeEndMo.groups())
            # convert endTimeList values to integers
            timeEndList = [int(i) for i in timeEndList]
            if timeEndList[0] < 0 or timeEndList[0] > 23:
                print('Incorrect Format. Please Re-enter end time.')
                continue
            elif timeEndList[1] < 0 or timeEndList[1] > 59:
                print('Incorrect Format. Please Re-enter end time.')
                continue
            elif timeEndList[0] < timeStartList[0]:
                print('Event end time cannot come before start time. Please re-enter end time.')
                continue
            elif timeEndList[0] == timeStartList[0] and timeEndList[1] < timeStartList[1]:
                print('Event end time cannot come before start time. Please re-enter end time.')
                continue
            else:
                break
    # formats timeEnd for input into google calendar api
    timeEnd = 'T' + timeEnd + ':00-06:00'
    dateTimeEnd = weddingDate + timeEnd

    # query for email address with input validation
    # used to pyinputplus because I was too lazy to make my own input validation for emails
    print('Email Address:')
    email = pyip.inputEmail(prompt='Email Address:')

    # query for book date with input validation
    while True:
        print('Book Date (yyyy-mm-dd):')
        bookDate = input()

        # create date match object using dateRegex
        dateMo = dateRegex.search(bookDate)
        
        # if loop checks for correct formatting of user input for wedding date
        if dateMo == None:
            print('Incorrect Format, Please Re-enter date booked.')
            continue
        else:  
            # convert dateMo tuple to list
            dateList = list(dateMo.groups())

            # convert dateList values to integers
            dateList = [int(i) for i in dateList]

            if dateList[1] <= 0 or dateList[1] >= 13:
                print('Incorrect Format, Please Re-enter date booked.')
                continue
            else:
                # create last day of month variable
                lastDayofMonth = calendar.monthrange(dateList[0], dateList[1])
                lastDayofMonth = lastDayofMonth[1]

                if dateList[2] <= 0 or dateList[2] > lastDayofMonth:
                    print('Incorrect Format, Please Re-enter date booked.')
                    continue
                else:
                    break


    # create list of queries and return eventList 
    eventList = [summary, location, description, dateTimeStart, dateTimeEnd, email, weddingDate, bookDate]
    return eventList

# allows query.py to be run for the purposes of debugging 
if __name__ == '__main__':
    print(query())
