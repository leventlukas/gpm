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

@app.route('/jan/ls', methods=['POST'])
def ws_jan_ls_all():
    print(request.json)
    cur = mysql.connection.cursor()
    #engine = setup_connection()
    #connection = engine.connect()

    query = 'Select * from jan_data'

    cur.execute(query)
    res = cur.fetchall()

    return jsonify(res)

@app.route('/levent/ls', methods=['POST'])
def ws_levent_ls_all():
    print(request.json)
    #engine = setup_connection()
    #connection = engine.connect()

    query = 'Select * from levent_data'

    res = connection.execute(query)

    return jsonify(res)

if __name__ == '__main__':
    app.run(debug=True, host = '0.0.0.0')

    ws_jan_ls_all()
