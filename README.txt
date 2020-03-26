Abstract
	The following program was created to automate adding wedding events to a florists google calendar. You say, "sounds pretty unnecessary, Austin." I agree. However, there is also a set of other important dates leading up to the wedding event itself that must be calculated and added to the event. Thus the need to automate the process.

	*The file contains 6 items:
		* README.txt
		* credentials.json
		* query.py
		* event.py
		* main.py
		* installPackages.py

	*credentials.json stores the credentials for my own instance of google calendar api so that the user can
		access it and run the program
	*I compartmentalized the project into scripts that perform specific functions 
		heirarchy:
			main 
				event
					query
	*query.py defines a function that queries the user for input regarding wedding date parameters and stores
		those values
	*event.py retrieves those values to calculate and create all the events to be added to a google calendar
	*main.py calls the google calendar api, prompts user to authorize read-write access to their google calendar,
		and then adds the events to the calendar
Required Packages
	To install required packages run:
	  $ pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib pyinputplus
	OR
	run the installPackages.py script
Run
	In order to execute the program simply run main.py
	If you want to observe the functionality and output of query.py and event.py, running them individually
		will execute their function(s) and print their output to the console 
	The authorization credentials will be stored in a file called 'token.pickle' and subsequent executions of the 		     program will not require the user to authorize access
Documentation:
	Google Calendar API:
		https://developers.google.com/calendar/quickstart/python
		https://developers.google.com/calendar/create-events
