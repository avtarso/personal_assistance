# personal.assistant.project

This Django application allows you to store and manage the user's contacts, records and files. It is also possible to aggregate news and weather forecast


1. To start, first of all, it is necessary to have and install variables

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

2. To run on a local machine
- for for Ubuntu/Linux - run `./first_run.sh`
- fo Windows - run `first_run.bat` and `first_run_next.bat`

3. Enjoy if you can:)


other files for Ubuntu/linx:
r.sh - start send reminder birthdays
s.sh - quick local start
start.sh - quick server start

files for server start:
railway.json, Procfile