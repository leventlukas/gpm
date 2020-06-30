from flask import Flask, jsonify, request
import sqlalchemy
from sqlalchemy import sql
import json
import requests
from flask_mysqldb import MySQL

app = Flask(__name__)

"""
def setup_connection():
    user = "janlevent"
    pwd = "898d4775"
    connection_string = "innoDB://"+user+":"+pwd+"@db4free.net:3306"
    engine = sqlalchemy.create_engine(connection_string, echo=False)
    connection = engine.connect()
    return engine
"""

app.config['MYSQL_USER'] = 'janlevent'
app.config['MYSQL_PASSWORD'] = '898d4775'
app.config['MYSQL_HOST'] = 'db4free.net'
app.config['MYSQL_DB'] = 'gpmesb'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

@app.route('/ping', methods=['POST'])
def ws_ping():
    print(request.json)
    return ("pong")

@app.route('/jan/ls', methods=['POST'])
def ws_jan_ls_all():
    print(request.json)
    cur = mysql.connection.cursor()
    #engine = setup_connection()
    #connection = engine.connect()

    query = 'Select * from gpu_jan'

    cur.execute(query)
    res = cur.fetchall()
    print(res)
    res = res[0]

    return jsonify(res)

@app.route('/levent/ls', methods=['POST'])
def ws_levent_ls_all():
    print(request.json)
    #engine = setup_connection()
    #connection = engine.connect()

    query = 'Select * from gpu_levent'

    res = connection.execute(query)

    return jsonify(res)

if __name__ == '__main__':
    app.run(debug=True, host = '0.0.0.0')

    ws_jan_ls_all()
