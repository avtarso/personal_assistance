@ECHO OFF

@REM ===========================================================

SETLOCAL

ECHO:
SET /p choice=Do you want to set environment variables? (y/n) [y]:

IF [%choice%]==[] SET choice=y
SET or_=
IF %choice%==y SET or_=true
IF %choice%==Y SET or_=true
IF DEFINED or_ ( GOTO :SETENV ) ELSE ( GOTO :SKIPSETENV )

:SETENV

ECHO:
ECHO *** If you want to skip some environment variables just press Enter ***
ECHO:

SET /p _EMAIL_PERSONAL_ASSISTANT=EMAIL_PERSONAL_ASSISTANT:
IF NOT [%_EMAIL_PERSONAL_ASSISTANT%]==[] SETX EMAIL_PERSONAL_ASSISTANT %_EMAIL_PERSONAL_ASSISTANT%

SET /p _EMAIL_PERSONAL_ASSISTANT_PASSWORD=EMAIL_PERSONAL_ASSISTANT_PASSWORD:
IF NOT [%_EMAIL_PERSONAL_ASSISTANT_PASSWORD%]==[] SETX EMAIL_PERSONAL_ASSISTANT_PASSWORD %_EMAIL_PERSONAL_ASSISTANT_PASSWORD%

SET /p _DJANGO_SECRET_KEY=DJANGO_SECRET_KEY:
IF NOT [%_DJANGO_SECRET_KEY%]==[] SETX DJANGO_SECRET_KEY %_DJANGO_SECRET_KEY%

SET /p _PA_DB_HOST=PA_DB_HOST:
IF NOT [%_PA_DB_HOST%]==[] SETX PA_DB_HOST %_PA_DB_HOST%

SET /p _PA_DB_PORT=PA_DB_PORT:
IF NOT [%_PA_DB_PORT%]==[] SETX PA_DB_PORT %_PA_DB_PORT%

SET /p _PA_DB_USER=PA_DB_USER:
IF NOT [%_PA_DB_USER%]==[] SETX PA_DB_USER %_PA_DB_USER%

SET /p _PA_DB_PASSWORD=PA_DB_PASSWORD:
IF NOT [%_PA_DB_PASSWORD%]==[] SETX PA_DB_PASSWORD %_PA_DB_PASSWORD%

SET /p _PA_DATA_BASE=PA_DATA_BASE:
IF NOT [%_PA_DATA_BASE%]==[] SETX PA_DATA_BASE %_PA_DATA_BASE%

SET /p _TELEGRAM_TOKEN=TELEGRAM_TOKEN:
IF NOT [%_TELEGRAM_TOKEN%]==[] SETX TELEGRAM_TOKEN %_TELEGRAM_TOKEN%

SET /p _TELEGRAM_CHAT=TELEGRAM_CHAT:
IF NOT [%_TELEGRAM_CHAT%]==[] SETX TELEGRAM_CHAT %_TELEGRAM_CHAT%

ENDLOCAL

:SKIPSETENV

@REM ===========================================================

ECHO:
ECHO Do you want to install postgres in docker?
ECHO *** Docker must be running at this time ***
ECHO:
ECHO If yes, the following command will be executed:
ECHO docker run --name postgres -p 5432:5432 -e POSTGRES_PASSWORD=postgres -d postgres
ECHO:

SETLOCAL

SET /p choice=Please make your choice (y/n) [y]:
IF [%choice%]==[] SET choice=y
SET or_=
IF %choice%==y SET or_=true
IF %choice%==Y SET or_=true
IF DEFINED or_ ( GOTO :RUNDOCKER ) ELSE ( GOTO :SKIPDOCKER )

:RUNDOCKER

docker run --name postgres -p 5432:5432 -e POSTGRES_PASSWORD=postgres -d postgres

ENDLOCAL

:SKIPDOCKER

@REM ===========================================================

ECHO === Create virtual environment...
PING 127.0.0.1 -n 2 > NUL
python -m venv paenv
ECHO === Done

@REM ===========================================================

ECHO === Activate virtual environment...
PING 127.0.0.1 -n 2 > NUL
.\paenv\Scripts\activate && first_run_next.bat
ECHO === Done

@REM ===========================================================