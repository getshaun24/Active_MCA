
echo "Installing and configuring environment..."

call py -3 -m venv .venv
call .\.venv\scripts\activate.bat
call pip install -r requirements.txt

set FLASK_APP=server.py
set FLASK_ENV=development
set FLASK_DEBUG=True
flask run
