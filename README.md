# personal.assistant.project

python3 -m venv paenv
source paenv/bin/activate

pip install -r requirements.txt

pre-commit install
pre-commit autoupdate
pre-commit run --all-files

for Ubuntu
Add to file .bashrc strings

```
export EMAIL_PERSONAL_ASSISTANT="__________________________________@gmail.com"
export EMAIL_PERSONAL_ASSISTANT_PASSWORD="____________________________"
export DJANGO_SECRET_KEY="________________________________________"
```

and run
`source ~/.bashrc`

for Windows
run comands

```
setx EMAIL_PERSONAL_ASSISTANT="__________________________________@gmail.com"
setx EMAIL_PERSONAL_ASSISTANT_PASSWORD="____________________________"
setx DJANGO_SECRET_KEY="________________________________________"
```

or

```
setx EMAIL_PERSONAL_ASSISTANT="__________________________________@gmail.com"
setx EMAIL_PERSONAL_ASSISTANT_PASSWORD="____________________________"
setx DJANGO_SECRET_KEY="________________________________________"
```
