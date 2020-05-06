# INF360 - Programming in Python
# Austin Salisbury (James)
# Final Project

Abstract
	The following program was created to automate adding wedding events to a florists google calendar. You say, "sounds pretty unnecessary, Austin." I agree. However, there is also a set of other important dates leading up to the wedding event itself that must be calculated and added to the calendar. Thus the need to automate the process.

	*The file contains 5 items:
		* README.txt
		* credentials.json
		* install.py
		* exception.py
		* submit.py
		* main.py

	*credentials.json stores the credentials for my own instance of google calendar api so that the user can
		access it and run the program
		those values
	*submit.py retrieves user values to calculate and create all the events to be added to a google calendar
	*main.py is a tkinter gui which allows the user to install/update dependencies, queries the user for input,
		and submits the data, i.e., adds events to google calendar. 
Required Packages
	To install required packages run:
	  $ pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib 
	OR
	click the 'install/upgrade' button on the programs main window	
Run
	In order to execute the program simply run main.py
	The program will open a web browser and user will have to grant authorization to the program
	The authorization credentials will be stored in a file called 'token.pickle' and subsequent executions of the 		     program will not require the user to authorize access
Documentation:
	Google Calendar API:
		https://developers.google.com/calendar/quickstart/python
		https://developers.google.com/calendar/create-events
