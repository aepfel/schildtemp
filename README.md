# schildtemp
Terrarium "management"


updater.py 
wird entweder einmal pro minute (o.ae.) per cronjob
gestartet und liest die zu schaltenden relaise 
daten aus der db und schaltet die relaise oder 
laeuft immer im bg und holt die wartezeit und
die zu schaltende relaisedaten aus der db
nutzt pyro um relaise auszerhalb der venv zu schalten.

run.py
startet flask-webserver/renderer zugriff über http://IP:6580/chart

app/view.py
erzeugt aus angeforderter seite und templates die angezeigte seite

app/models.py
beschreibung der datenbank

verwendete flask-anleitung:
http://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world

initialisierung:

./db_create.py && ./db_migrate.py && ./db_init.py
