# creates an event in a users google calendar using google calendar api
# documentation at https://developers.google.com/calendar/quickstart/python

# query returns user input as eventList
def query():
    print('Event:')
    summary = input()
    
    print('location:')
    location = input()

    print('description:')
    description = input()

    print('date (yyyy-mm-dd):')
    date = input()

    print('start time:')
    timeStart = 'T' + input() + ':00-06:00'

    dateTimeStart = date + timeStart
    
    print ('end time:')
    timeEnd = 'T' + input() + ':00-06:00'
    
    dateTimeEnd = date + timeEnd

    print('email of coordinator:')
    email = input()

    eventList = [summary, location, description, dateTimeStart, dateTimeEnd, email]
    return eventList

# add event to calendar
# uses the return value from query() to insert values into event{}
# documentation at https://developers.google.com/calendar/create-events
def createEvent():
    eventList = query()
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
            'recurrence': [],
            'attendees': [
                {'email': eventList[5]},
                ],
            'reminders': {
                'useDefault': False,
                'overrides': [],
                },
            }

    event = service.events().insert(calendarId='primary', body=event().execute())
    print('Event created: %s' % (event.get('htmlLink')))

createEvent()
