# Personal Assistant APP

Personal Assistant is a Django application that allows you to store and manage a registered user's contacts, posts, and files. It is also possible to aggregate news and weather forecasts.

## Features

- User authentication and authorization
- Upload and download files
- Create, delete and edit descriptions of downloaded files
- Schedule a file review time
- Create, delete and edit contacts
- Schedule a file review time
- Notify about the time of a contact's birthday
- Create, delete and edit notes
- Random quote API
- Aggregate news on selected topics

## Setup

To run the Personal Assistant on your local system, you will need to install several prerequisites and then set up the application. Follow the instructions below to get started.

### Prerequisites

Before installing the application, make sure you have the following software installed:

- [Git](https://git-scm.com/) - Version control system for cloning the repository.
- [Python](https://www.python.org/) - Programming language required for running the Django microservice.

### Set up variables

for Ubuntu Add to file .bashrc strings
```
export EMAIL_PERSONAL_ASSISTANT="________________________________@gmail.com"
export EMAIL_PERSONAL_ASSISTANT_PASSWORD="_______________________"
export DJANGO_SECRET_KEY="_______________________________________"
export TELEGRAM_TOKEN="___________________________"
export TELEGRAM_CHAT="____________________________"
export PA_DATA_BASE="________"
export PA_DB_USER="__________"
export PA_DB_PASSWORD="__________"
export PA_HOST="localhost"
export PA_DB_PORT="5432"
```
and run `source ~/.bashrc`

for Windows run comands
```
setx EMAIL_PERSONAL_ASSISTANT="__________________________________@gmail.com"
setx EMAIL_PERSONAL_ASSISTANT_PASSWORD="____________________________"
setx DJANGO_SECRET_KEY="________________________________________"
setx TELEGRAM_TOKEN="___________________________"
setx TELEGRAM_CHAT="____________________________"
setx PA_DATA_BASE="________"
setx PA_DB_USER="__________"
setx PA_DB_PASSWORD="__________"
setx PA_HOST="localhost"
setx PA_DB_PORT="5432"
```

### To run on a local machine

- for Ubuntu/Linux - run `./first_run.sh`
- for Windows - run `first_run.bat`

### Enjoy if you can:)

other files for Ubuntu/linx:
r.sh - start send reminder birthdays
s.sh - quick local start
start.sh - quick server start

files for server start:
railway.json, Procfile