This app automates the sending of report files to clients using their emails.
it schedules the sending every day at 10:30.

To use this app; 
1 - Create a virtual environment with virtualenv
2 - Put the app folder at the same level of the environment folder
3 - Activate the environment
4 - Run pip install -r requirements.txt to install the dependencies
5 - Open the email_automation.py, specify the path to the report files and the log file and run it 


We use the sandbox app to test the emails please create an account and put the given USERNAME AND PASSWORD in a .env like this

USERNAME = "given_username"
PASSWORD = "given_password"

put the .env file at the same level of the other files