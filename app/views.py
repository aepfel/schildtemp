from flask import render_template
from app import app, db, models

# todo
# datenbankanbindung
# 20 aktuellste messdaten holen
# ggf. time zurechtschneiden

@app.route('/')
@app.route('/index')
def index():
    user = {'nickname': 'Miguel'}  # fake user
    return render_template('index.html',title='home',user=user)

@app.route('/chart')
def chart():
    relstat = []
    times = []
    rel = models.Conf.query.first().relstate
    x = 128
    while (x != 0):                 # schleife, die den status der relaise in ein array mit html-rot und -gruen aendert
        if (rel >= x):
	    relstat.append('00FF00')
    	    rel = rel-x
        else:
            relstat.append('FF0000')
        x = x/2

    dat = models.Tempdata.query.order_by(models.Tempdata.id.desc()).limit(30).all()
    for d in dat:
        times.append({'time':str(d.timestamp.day) + '. ' + str(d.timestamp.hour) + ':' + str(d.timestamp.minute)
                     ,'data1':float(d.data1)/10
                     ,'data2':float(d.data2)/10})

    #times = [ #fake array messzeiten
    #    {'time':'01:00','data1':'25','data2':'25'},
    #    {'time':'03:00','data1':'28','data2':'24'},
    #    {'time':'08:00','data1':'22','data2':'26'},
    #    {'time':'12:00','data1':'10','data2':'29'},
    #    {'time':'15:00','data1':'12','data2':'21'},
    #    {'time':'16:00','data1':'43','data2':'23'},
    #    {'time':'22:00','data1':'40','data2':'25'}
    #  ]
    d = models.Tempdata.query.order_by(models.Tempdata.id.desc()).limit(1).all()
    data1 = float(d[0].data1)/10
    data2 = float(d[0].data2)/10
    return render_template('chart.html',times = times, relstat = relstat, data1 = data1, data2 = data2)
