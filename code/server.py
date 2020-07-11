from flask import Flask, jsonify, request
import sqlalchemy
from sqlalchemy import sql
import json
import requests
from flask_mysqldb import MySQL
import ast

app = Flask(__name__)

"""
def setup_connection():
    user = "janlevent"
    pwd = "arschmin"
    connection_string = "innoDB://"+user+":"+pwd+"@localhost:3306"
    engine = sqlalchemy.create_engine(connection_string, echo=False)
    connection = engine.connect()
    return engine
"""

app.config['MYSQL_USER'] = 'janlevent'
app.config['MYSQL_PASSWORD'] = 'arschmin'
app.config['MYSQL_HOST'] = 'mysql'
app.config['MYSQL_DB'] = 'test'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

@app.route('/ping', methods=['POST'])
def ws_ping():
    print(request.json)
    return ("pong")

#############################
# Jan
#############################
@app.route('/jan/ls/event', methods=['POST'])
def ws_jan_ls_event():

    query = 'Select * from event_data'

    cur = mysql.connection.cursor()
    cur.execute(query)
    res = cur.fetchall()

    return jsonify(res)

@app.route('/jan/ls/location', methods=['POST'])
def ws_jan_ls_location():

    query = 'Select * from location_data'

    cur = mysql.connection.cursor()
    cur.execute(query)
    res = cur.fetchall()

    return jsonify(res)


@app.route('/jan/ls', methods=['POST'])
def ws_jan_ls_all():

    query = 'Select * from jan_data'

    cur = mysql.connection.cursor()
    cur.execute(query)
    res = cur.fetchall()

    return jsonify(res)


@app.route('/jan/add', methods=['POST'])
def ws_jan_add():
    print(request)
    print(request.data)
    print(request.json)
    print(request.files)
    r_body = request.data.decode('utf-8')
    print(r_body)
    r_body = json.loads(r_body)
    print(r_body)

    anrede = str(r_body['anrede'])
    nname = str(r_body['nname'])
    vname = str(r_body['vname'])
    hobby = str(r_body['hobby'])
    email = str(r_body['email'])
    bl = str(r_body['bl'])
    invited = r_body['invited']

    query = f'INSERT INTO jan_data (anrede, nname, vname, hobby, email, bl, invited) VALUES ("{anrede}", "{nname}", "{vname}", "{hobby}", "{email}", "{bl}", {invited})'
    print(query)
    cur = mysql.connection.cursor()
    cur.execute(query)
    mysql.connection.commit()
    res = cur.fetchall()
    
    return jsonify(res)

@app.route('/jan/dateadd', methods=['POST'])
def ws_jan_dateadd():
    print(request)
    print(request.data)
    print(request.json)
    print(request.files)
    r_body = request.data.decode('utf-8')
    print(r_body)
    r_body = json.loads(r_body)
    print(r_body)

    stadt = str(r_body['stadt'])
    location = str(r_body['location'])
    decision = r_body['decision']
    date1 = str(r_body['date1'])
    date2 = str(r_body['date2'])
    date3 = str(r_body['date3'])

    query = f'INSERT INTO event_data (stadt, location, decision, date1, date2, date3) VALUES ("{stadt}", "{location}", {decision}, "{date1}", "{date2}", "{date3}")'
    print(query)
    cur = mysql.connection.cursor()
    cur.execute(query)
    mysql.connection.commit()
    res = cur.fetchall()
    
    return jsonify(res)
#############################
# Levent
#############################

@app.route('/levent/get/bestand', methods=['POST'])
def ws_levent_ls_garnrollen():
    print("test")
    print(request.data)
    r_body = request.data.decode('utf-8')
    print(r_body)
    r_body = json.loads(r_body)
    
    typ = str(r_body['typ'])
    farbe = str(r_body['farbe'])

    query = f'Select * from Garnrollen where Typ = "{typ}" and Farbe = "{farbe}"'
    cur = mysql.connection.cursor()
    cur.execute(query)
    res = cur.fetchall()
    print(res)
    print(res[0])
    return jsonify(res[0])

@app.route('/levent/get/prod', methods=['POST'])
def ws_levent_ls_prod():
    r_body = request.data.decode('utf-8')
    r_body = json.loads(r_body)
    result = []
    print(r_body)
    
    for element in r_body:
        if (element['typ'] != None):
            typ = str(element['typ'])
            farbe = str(element['farbe'])
            query = f'Select SUM(vLaenge) FROM Garnrollen WHERE Typ = "{typ}" AND Farbe = "{farbe}"'
            cur = mysql.connection.cursor()
            cur.execute(query)
            res = cur.fetchall()
            print(res)
            result.append(dict(
                sLng = int(res[0]['SUM(vLaenge)'])
            ))
            print(result)
    
    return jsonify(result)

@app.route('/levent/reserve/prod', methods=['POST'])
def ws_levent_reserve_products():
    print(request.data)
    r_body = request.data.decode('utf-8')

    r_body = json.loads(r_body)
    result = []
    bNr = r_body['id']
    print(r_body['prod'])
    
    for product in r_body['prod']:
        print(product)
        if product['typ'] != None:
            typ = str(product['typ'])
            farbe = str(product['farbe'])
            lng = int(product['laenge'])
            pId = 0
            query = f'SELECT * from Garnrollen WHERE Typ = "{typ}" AND Farbe = "{farbe}"'
            cur = mysql.connection.cursor()
            cur.execute(query)
            res = cur.fetchall()
            for item in res:
                print(item)
                if pId == 0:
                    print(int(item['vLaenge']))
                    print(lng)
                    if int(item['vLaenge']) >= lng:
                        laenge = int(item['vLaenge']) - lng
                        pId = item['ProduktID']
                        query1 = f'UPDATE Garnrollen SET vLaenge = {laenge} WHERE ProduktID = {pId}'
                        print(query1)
                        preis = item['Preis']
                        query2 = f'INSERT INTO BestellungProdukte (Bestellnummer, Laenge, Preis, Typ, Farbe, ProduktID) VALUES ("{bNr}",{lng},{preis},"{typ}","{farbe}", {pId})'
                        print(query2)
                        cur = mysql.connection.cursor()
                        cur.execute(query1)
                        cur.execute(query2)
                        res = cur.fetchall()
        mysql.connection.commit()
        result.append(pId)

    return jsonify(result)

@app.route('/levent/put/bezBest', methods=['POST'])
def ws_levent_put_bezugsbestellung():
    r_body = request.data.decode('utf-8')
    print(type(r_body))
    r_body = json.loads(r_body)
    print(r_body)
    print(type(r_body))
    bNr = r_body['id']
    
    cur = mysql.connection.cursor()
    for product in r_body['prod']:
        typ = str(product['typ'])
        farbe = str(product['farbe'])
        blng = int(product['laenge'])
        query = f'SELECT Laenge from LieferantenProdukte WHERE Typ = "{typ}" AND Farbe = "{farbe}"'
        cur.execute(query)
        res = cur.fetchall()
        print(res)
        lng = res[0]['Laenge']
        vlng = lng - blng
        query = f'SELECT ProduktID FROM test.Garnrollen ORDER BY ProduktID DESC'
        cur.execute(query)
        res = cur.fetchall()
        print(res)
        pId = int(res[0]['ProduktID']) +1
        query = f'INSERT INTO Garnrollen (Typ, Farbe, Preis, Laenge, vLaenge, vFlg, BezugsID) VALUES ("{typ}", "{farbe}", 2, {lng}, {vlng}, 0, 1)'
        cur.execute(query)
        query = f'INSERT INTO BestellungProdukte (Bestellnummer, Laenge, Preis, Typ, Farbe, ProduktID) VALUES ("{bNr}",{blng},2 ,"{typ}","{farbe}", {pId})'
        cur.execute(query)
        mysql.connection.commit()
    return 'success'

@app.route('/levent/put/bestelleingang', methods=['POST'])
def ws_levent_put_bestelleingang():
    r_body = request.data.decode('utf-8')
    print(type(r_body))
    r_body = json.loads(r_body)
    bNr = r_body['id']

    cur = mysql.connection.cursor()
    query = f'Select ProduktID from BestellungProdukte WHERE Bestellnummer = "{bNr}"'
    cur.execute(query)
    res = cur.fetchall()
    print(res)
    for garn in res:
        pId = garn['ProduktID']
        query = f'UPDATE Garnrollen SET vFlg = 1 WHERE ProduktID = {pId}'
        cur.execute(query)
    mysql.connection.commit()
    return 'success'

@app.route('/levent/put/kundenbestellung', methods=['POST'])
def ws_levent_put_kundenbestellung():
    r_body = request.data.decode('utf-8')
    print(type(r_body))
    r_body = json.loads(r_body)
    bNr = r_body['id']

    cur = mysql.connection.cursor()
    query = f'Select ProduktID, Laenge from BestellungProdukte WHERE Bestellnummer = "{bNr}"'
    cur.execute(query)
    res = cur.fetchall()
    print(res)
    for garn in res:
        lng = int(garn['Laenge'])
        pId = garn['ProduktID']
        query = f'Select Laenge from Garnrollen WHERE ProduktID = {pId}'
        cur.execute(query)
        res = cur.fetchall()
        res = res[0]
        print(res)
        nlng = int(res['Laenge']) - lng
        query = f'UPDATE Garnrollen SET Laenge = {nlng} WHERE ProduktID = {pId}'
        cur.execute(query)
    mysql.connection.commit()
    return 'success'

if __name__ == '__main__':
    app.run(debug=True, host = '0.0.0.0')
