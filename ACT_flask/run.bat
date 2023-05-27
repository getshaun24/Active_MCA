
@REM echo "Installing and configuring environment..."

@REM call py -3 -m venv venv
@REM call .\venv\scripts\activate.bat
@REM call pip install -r requirements.txt

set FLASK_APP=app.py
set FLASK_ENV=development
set FLASK_DEBUG=True
flask run
