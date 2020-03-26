''' run main.py to add an event to your google calendar
    main.py consists of two fucntions
        1. addEvents(eventDictList, service)
        2. main()
    main() is responsible calling credentials.json, which connects my google calendar api credentials,
        and storing your user access and refresh tokens so that main() has permissions to access and modify
        your 'primary' google calendar. Once the process is complete, main() calls addEvents() to add events
        to the calendar
    main.py makes function calls to the event.py module and event.py makes function calls to the query.py module
        the reason for creating this hierarchy (query -> event -> main) was twofold: 
            1. compartmentalize the script into the most basic functional units 
            2. easier to conceptualize, read, and debug
'''

from __future__ import print_function
import event
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']

# addEvents takes eventDictList and create a google calendar event for each index
def addEvents(eventDictList, service):
    # both eventDictList and service parameters are local variables within main()

    # service is an object of the build() module imported from googleapiclient.discovery
    # which stores your authentication information so that the calendar can be modified
    service = service

    # all the events we want to add to the calendar are stored in eventDictList.
    # by setting event = service.events().insert().execute, we are creating an event
    # in a specific calendar using the credentials in the service variable and our event dictionaries
    # that are stored in eventDictList
    for i in eventDictList:
        event = service.events().insert(calendarId='primary', body=i).execute()
        print('Event created: %s' % (event.get('htmlLink')))

def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
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

    # call function createEvent() from the event module
    listOfEvents = event.createEvent()

    # add events to calendar
    addEvents(listOfEvents, service)

if __name__ == '__main__':
    main()
