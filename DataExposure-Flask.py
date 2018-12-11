import requests
import pyodbc
from flask import Flask, g, render_template, abort, request
import DataValue
import json
import pandas as pd
from sqlalchemy import create_engine
import GetCredentials

User,Pass = GetCredentials.GetCreds('its me,dummy','let me in')

CONNECTION_STRING = 'Driver={ODBC Driver 17 for SQL Server};Server=cody-practice.database.windows.net,1433;Database=Cody-IRS-Data;Uid=' + User + '@cody-practice;Pwd=' + Pass + ';'

app = Flask(__name__)

@app.route("/", methods=['GET'])
def LandingPage():
    welcomeMessage = '''Welcome to my API! <br><br>
                        This API hosts IRS data for every state and zip code in the US. To query, search using these tags:<br><br>
                        <table>
                        <thead><tr><th>Item</th><th>tag</th></tr></thead>
                        <tbody>
                        <tr><td>All Data by Year</td><td>/taxdata/(year)</td></tr>
                        <tr><td>Data by State & Year</td><td>/taxdata/(year)/state/(state)</td></tr>
                        </tbody>
                        </table>'''
    return welcomeMessage

@app.before_request
def before_request():
    try:
        g.sql_conn =  pyodbc.connect(CONNECTION_STRING, autocommit=True)
    except Exception:
        abort(500, "No database connection could be established.")


@app.route("/taxdata/<string:yr>",methods=['GET'])
def GetData(yr):
    curs = g.sql_conn.cursor()
    if yr == '2016':
        query = 'select * from Tax_Data_2016'
    elif yr == '2015':
        query = 'select * from Tax_Data_2015'
    elif yr == '2014':
        query = 'select * from Tax_Data_2014'
    elif yr == '2013':
        query = 'select * from Tax_Data_2013'
    curs.execute(query)

    columns = [column[0] for column in curs.description]
    data = []

    for row in curs.fetchall():
        data.append(dict(zip(columns, row)))
    return json.dumps(data, indent=4, sort_keys=True, default=str)

@app.route("/taxdata/<string:yr>/state/<string:id>",methods=['GET'])
def GetItemID(yr,id):
    curs = g.sql_conn.cursor()
    if yr == '2016':
        curs.execute("select * from Tax_Data_2016 where STATE = ?", id)
    elif yr == '2015':
        curs.execute("select * from Tax_Data_2015 where STATE = ?", id)
    elif yr == '2014':
        curs.execute("select * from Tax_Data_2014 where STATE = ?", id)
    elif yr == '2013':
        curs.execute("select * from Tax_Data_2013 where STATE = ?", id)
    columns = [column[0] for column in curs.description]
    data = []

    for row in curs.fetchall():
        data.append(dict(zip(columns, row)))

    return json.dumps(data, indent=4, sort_keys=True, default=str)


@app.route("/taxdata/topzips/<string:state>",methods=['GET'])
def ShowHeatMap(state):
    DataValue.HeatMap2(state)
    


    return 'success', 200



if __name__ == '__main__':
    app.run(debug=True)

