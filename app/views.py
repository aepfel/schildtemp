# -*- coding: utf-8 -*-
from flask import render_template, request
from app import app, db, models

# todo
# datenbankanbindung
# 20 aktuellste messdaten holen
# ggf. time zurechtschneiden

@app.route('/')
@app.route('/index')
@app.route('/chart')
def chart():
    relstat = []
    times = []
    schnitte = []
    rel = models.Conf.query.first().relstate
    x = 128
    while (x > 0):                 # schleife, die den status der relaise in ein array mit html-rot und -gruen aendert
        if (rel >= x):
	    relstat.append('FF0000')
    	    rel = rel-x
        else:
            relstat.append('00FF00')
        x = x/2
    #temperaturgischichte holen
    #jeden 5. datensatz holen dat = models.Tempdata.query.order_by(models.Tempdata.id.desc()).filter(models.Tempdata.id%5 == 0).limit(50).all()
    dat = models.Tempdata.query.order_by(models.Tempdata.id.desc()).limit(250).all()
    z = 0
    while z < len(dat):
	#times-array mit zeitstempel des ersten von 5 datenpunkten und dem mittelwert der folgenden 4 datenpunkte befuellen
        times.append({'time':str(dat[z].timestamp.strftime("%d. %H:%M")),'data1':sum(float(item.data1) for item in dat[z:z+5])/5})
        z+=5
    #for d in dat:
    #    times.append({'time':str(d.timestamp.strftime("%d. %H:%M")),'data1':float(d.data1)})
                     #,'data2':float(d.data2)/10})
                     # for d in dat: times.append({'time':str(d.timestamp.day) + '. ' + str(d.timestamp.hour) + ':' + str(d.timestamp.minute),'data1':float(d.data1)})
    #aktuellste temperatur holen
    d = models.Tempdata.query.order_by(models.Tempdata.id.desc()).limit(1).all()
    data1 = float(d[0].data1)
    #data2 = float(d[0].data2)/10
    #min/max/median berechnen
    dat = models.Tempdata.query.order_by(models.Tempdata.id.desc()).limit(250).all()
    for d in dat: schnitte.append(float(d.data1))
    return render_template('chart.html',times = times, relstat = relstat, data1 = data1, min = min(schnitte), max = max(schnitte), med = median(schnitte))


@app.route('/config')
def config():
    s0 = models.Schalttabelle.query.first()
    if (request.args.get('t1') != None):
        tNeu = []
        rNeu = 255
        for n in range(1,25):
            tNeu.append(request.args.get('t'+str(n)))
        if (request.args.get('R1') != None): rNeu = rNeu - 128
        if (request.args.get('R2') != None): rNeu = rNeu - 64
        if (request.args.get('R3') != None): rNeu = rNeu - 32
        if (request.args.get('R4') != None): rNeu = rNeu - 16
        if (request.args.get('R5') != None): rNeu = rNeu - 8
        if (request.args.get('R6') != None): rNeu = rNeu - 4
        if (request.args.get('R7') != None): rNeu = rNeu - 2
        if (request.args.get('R8') != None): rNeu = rNeu - 1
        s0.rel = rNeu
        s0.t0 = request.args.get('t1')
        s0.t1 = request.args.get('t2')
        s0.t2 = request.args.get('t3')
        s0.t3 = request.args.get('t4')
        s0.t4 = request.args.get('t5')
        s0.t5 = request.args.get('t6')
        s0.t6 = request.args.get('t7')
        s0.t7 = request.args.get('t8')
        s0.t8 = request.args.get('t9')
        s0.t9 = request.args.get('t10')
        s0.t10 = request.args.get('t11')
        s0.t11 = request.args.get('t12')
        s0.t12 = request.args.get('t13')
        s0.t13 = request.args.get('t14')
        s0.t14 = request.args.get('t15')
        s0.t15 = request.args.get('t16')
        s0.t16 = request.args.get('t17')
        s0.t17 = request.args.get('t18')
        s0.t18 = request.args.get('t19')
        s0.t19 = request.args.get('t20')
        s0.t20 = request.args.get('t21')
        s0.t21 = request.args.get('t22')
        s0.t22 = request.args.get('t23')
        s0.t23 = request.args.get('t24')
        db.session.add(s0)
        db.session.commit()


    relstate = []
    temps = timearray(s0)
    rel = s0.rel
    x = 128
    while (x > 0):                 # schleife, die den status der relaise in ein array mit checked und '' schreibt
        if (rel >= x):
	    relstate.append('')
    	    rel = rel-x
        else:
            relstate.append('checked')
        x = x/2

    #welche schwelltemp. zu welcher uhrzeit, welcher sensor regelt welche relais
    #db erweitern
    return render_template('config.html',relstate = relstate, temps = temps)


def timearray(s1):
    st = []
    st.append(s1.t0)
    st.append(s1.t1)
    st.append(s1.t2)
    st.append(s1.t3)
    st.append(s1.t4)
    st.append(s1.t5)
    st.append(s1.t6)
    st.append(s1.t7)
    st.append(s1.t8)
    st.append(s1.t9)
    st.append(s1.t10)
    st.append(s1.t11)
    st.append(s1.t12)
    st.append(s1.t13)
    st.append(s1.t14)
    st.append(s1.t15)
    st.append(s1.t16)
    st.append(s1.t17)
    st.append(s1.t18)
    st.append(s1.t19)
    st.append(s1.t20)
    st.append(s1.t21)
    st.append(s1.t22)
    st.append(s1.t23)
    return st



@app.route('/press')
def press():
    times = []
    deltas = []
    #druckgeschichte holen
    dat = models.Pressdata.query.order_by(models.Pressdata.id.desc()).filter(models.Pressdata.id%3 == 0).limit(50).all()
    for d in dat: times.append({'time':str(d.timestamp.strftime("%d. %H:%M")),'data1':float(d.data1)})
                     #,'data2':float(d.data2)/10})
                     # for d in dat: times.append({'time':str(d.timestamp.day) + '. ' + str(d.timestamp.hour) + ':' + str(d.timestamp.minute),'data1':float(d.data1)})
    #aktuellste temperatur holen
    d = models.Pressdata.query.order_by(models.Pressdata.id.desc()).limit(1).all()
    data1 = float(d[0].data1)
    #data2 = float(d[0].data2)/10
    #del tas für den luftdruck (letzte 10/50/150 messungen)
    dat = models.Pressdata.query.order_by(models.Pressdata.id.desc()).limit(150).all()
    for d in dat: deltas.append(float(d.data1))
    delta10 = max(deltas[0:10])-min(deltas[0:10]) 
    delta50 = max(deltas[0:50])-min(deltas[0:50]) 
    delta = max(deltas)-min(deltas) 
    return render_template('press.html',times = times, data1 = data1, delta10 = delta10, delta = delta, delta50 = delta50)



def median(lst):
    lst = sorted(lst)
    if len(lst) < 1:
            return None
    if len(lst) %2 == 1:
            return lst[((len(lst)+1)/2)-1]
    else:
            return float(sum(lst[(len(lst)/2)-1:(len(lst)/2)+1]))/2.0
