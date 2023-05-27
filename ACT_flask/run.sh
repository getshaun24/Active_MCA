echo "Installing and configuring environment..."
python3 -q -m venv venv
source venv/bin/activate

# pip3 install -r requirements.txt
export FLASK_APP=server.py
export FLASK_DEBUG=1
flask run
