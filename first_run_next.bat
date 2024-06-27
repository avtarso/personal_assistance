@ECHO OFF

@REM ===========================================================

ECHO === Installing required dependencies...
PING 127.0.0.1 -n 2 > NUL
pip install -r requirements.txt
ECHO === Done

@REM ===========================================================

ECHO === Go to the project folder
PING 127.0.0.1 -n 2 > NUL
CD pa

@REM ===========================================================

ECHO === Creating and applying migrations...
PING 127.0.0.1 -n 2 > NUL
python manage.py makemigrations
python manage.py migrate
ECHO === Done

@REM ===========================================================

ECHO === Creating test records...
PING 127.0.0.1 -n 2 > NUL
python fill.py
ECHO === Done

@REM ===========================================================

ECHO === Killing processes using the port 8000...
PING 127.0.0.1 -n 2 > NUL

SETLOCAL

FOR /F "tokens=5" %%T IN ('netstat -a -n -o ^| FINDSTR ":8000"') DO (SET /A ProcessId=%%T)
IF [%ProcessId%]==[] GOTO :NOPROCESS

ECHO ProcessId to kill = %ProcessId%
TASKKILL /F /T /PID %ProcessId%

ENDLOCAL

:NOPROCESS

ECHO === Done

@REM ===========================================================

ECHO === Starting the server Django...
PING 127.0.0.1 -n 2 > NUL
python manage.py runserver
ECHO === Done

@REM ===========================================================