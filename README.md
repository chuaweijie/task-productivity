# 90 Days Reporting Tracker
## Introduction
For expats who work in Thailand and travels a lot, the [Notification of staying in the Kingdom over 90 days](https://www.immigration.go.th/en/?page_id=1666) can be a hassle for the following scenarios.
1. You fly out of the country before the next 90 days reporting in which you will need to count your 90 days by yourself when you land in Thailand.
2. If you want to skip the hassle of the immigration department, keeping track of when can you can do the online reporting ([User Guide: Within 15 days and not less than 7 days before the due date of notification](https://extranet.immigration.go.th/fn90online/online/tm47/TM47Action.do)) could be a hassle. 

The aim of this system is to enable expats to be able to keep track of their 90 days reproting easily and to help them add the important events to their Google Calendar for reminders.

## Distincitiveness and Complexity
### Distinctiveness
1. Table-based interface - This app will display data with a table-based interface. This is quite different from the other projects. 
2. Personal tool - This is a personal tool that enables one to do things better which is quite different in terms of concept with the other projects.
3. Niche problem - Different from the other projects that we have in the course, this project solves a niche problem faced by a small group of expats in Thailand.

### Complexity
In terms of concept, the app is not complex at all. You are just having someone inputting a date into the system and the system churns out the date according to a fixed formula. That is pretty straight forward. The complexity of this project lies in its technical complexity that enabled me to become a better web developer. 

1. External API Call - I've developed a password recovery mechanism that involves the system sending an email to the user through a third party email service. This helped me to learn how to store API keys securely using environmental variables instead of just simply including it in the code. 
2. A somewhat full CI/CD process - I implemented a CI/CD process through GitHub actions. Whenever I merge code into the main branch, it will run the CI test. If it passes, then it will be deployed into my Heroku server. The reason that I said it is somewhat full is because there is a part of the code that doesn't receive coverage which will be detailed in the [Additional Information](https://github.com/chuaweijie/task-productivity/additional-information) part. 
3. Utilizing Postgresql as the DB instead of Sqlite3 - This involves undertanding how to configure Django to Postgresql and at the same time learn about psycopg2. 
4. Deploying it in Heroku - I managed to deploy it with Gunicorn together with Whitenoise to serve the static files. 
5. Using React Bootstrap and webpack - Due to the fact that I wanted to have my react code trigger a bootstrap model, I cannot seem to make it work because of React's virtual DOM so I decided to use React Booststrap. That brings another problem which is how do I include it into my project? That's when I found out about webpack and learnt how to use it.  
6. Test cases with inheritance - Used inheritance to enable writing one UI test case and running them on multiple browsers. Another thing is to use inheritance so that the test cases can share common methods. This will reduce copying and pasting.

## How to run the application
1. Sign up for mailjet to get their API key. 
2. Export the keys to your environment vairables.
```
export MAILJET_SECRET=secret_from_mailjet
export MAILJET_KEY=key_from_mailjet
```
3. Using the database_url environment variable OR create your own config file.
  - Using database_url environment variable.
    - ```export DATABASE_URL = your_database_url```
  - Creating your own config file
    - Create a new config file under ```task-productivity/capstone/```
    - change local_settings on line 129 of ```task-productivity/capstone/settings.py``` to your filename.
 4. ```python3 manage.py runserver```

## Additional Information
### Test Not Covered
1. Selenium chrome in Ubuntu somehow wouldn't detect the state changes by React. I cannot seem to find ouw how to solve this so I commented out the UI tests cases for the react part of my code. The UI part will not be covered by automated test cases.
### Different GitHub name from the project objective.
1. I originally started with a different project related to a task list but as I was working on it, the 90 days tracking is a more pressing need for myself so I switched the project direction to it. I somehow didn't manage to change the Github and Django project name.
### Link to Production Site
https://task-productivity.herokuapp.com/
