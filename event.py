# documentation at https://developers.google.com/calendar/quickstart/python

import datetime
import re
import calendar
import query

# add event to calendar
# uses the return value from query() to insert values into event{}
# documentation at https://developers.google.com/calendar/create-events

def createEvent():
    eventList = query.query()
    event = {
            'summary': eventList[0],
            'location': eventList[1],
            'description': eventList[2],
            'start': {
                'dateTime': eventList[3],
                'timeZone': 'America/Chicago',
                },
            'end': {
                'dateTime': eventList[4],
                'timeZone': 'America/Chicago',
                },
            'attendees': [
                {'email': eventList[5]},
                ]
            }
    eventDictList = []
    eventDictList.append(event)
    print(eventDictList)
    # use of dateRegex allows for grouping date strings 'yyyy-mm-dd' into year, month, and day groups
    dateRegex = re.compile(r'(\d{4})-(\d{2})-(\d{2})')

    # creates weddingDate and bookDate variables of type <class 'datetime.date'> to allow for date.timedelta() calculations
    moWeddingDate = dateRegex.search(eventList[6])
    weddingDateIntList = [int(i) for i in moWeddingDate.groups()]
    year, month, day = weddingDateIntList
    weddingDate = datetime.date(year, month, day)

    moBookDate = dateRegex.search(eventList[7])
    bookDateIntList = [int(i) for i in moBookDate.groups()]
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
    twoWeeksTilHalfway = 'second payment reminder for' + ' ' + eventList[0]
    halfWay = 'second payment due for' + ' ' + eventList[0]
    seventyFiveDays = 'schedule design meeting for' + ' ' + eventList[0]
    fortyFourDays = 'send final payment reminder for' + ' ' + eventList[0]
    oneMonth = 'final payment due for' + ' ' + eventList[0] + ' ' + '(order flowers)'
    threeWeeks = 'send questionnaire for' + ' ' + eventList[0]
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
            eventDictList.append(event)
    
    return eventDictList
