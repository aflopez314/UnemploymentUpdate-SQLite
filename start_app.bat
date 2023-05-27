ECHO Starting Python Application

:: Create Environment
py -3 -m venv .venv

:: Activate Environment
CALL .venv\Scripts\activate

:: Install flask and other modules required for the application
pip install Flask
pip install Jinja2
pip install pandas
pip install sqlite3


:: Set flask application
set FLASK_APP=unemploymentUpdate.py
set FLASK_ENV=development

:: Start application and open to localhost webpage
start "chrome.exe" http://127.0.0.1:5000/
flask run


PAUSE