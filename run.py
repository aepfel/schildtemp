#!flask/bin/python
from app import app
#from updater import schalten
app.run(debug=True, host='0.0.0.0', port=6580)
