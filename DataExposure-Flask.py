import requests
import pyodbc
from flask import Flask, g, render_template, abort, request, send_file, send_from_directory
import DataValue
import json
import pandas as pd
from sqlalchemy import create_engine
import GetCredentials
import os

User,Pass = GetCredentials.GetCreds('its me, dummy','let me in')

CONNECTION_STRING = 'Driver={ODBC Driver 17 for SQL Server};Server=cody-practice.database.windows.net,1433;Database=Cody-IRS-Data;Uid=' + User + '@cody-practice;Pwd=' + Pass + ';'

MyFolder = os.path.join('static')

app = Flask(__name__)
app.config['Upload_Folder'] = MyFolder

@app.after_request
def add_header(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    response.headers['Cache-Control'] = 'public, max-age = 0'
    return response



@app.route("/", methods=['GET'])
def LandingPage():
    #welcomeMessage = 
    return render_template("welcome.html")

@app.before_request
def before_request():
    try:
        g.sql_conn =  pyodbc.connect(CONNECTION_STRING, autocommit=True)
    except Exception:
        abort(500, "No database connection could be established.")


@app.route("/visuals/info",methods=['GET'])
def display():
    return render_template("visualsinfo.html")


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

@app.route("/taxdata/<string:yr>/zipcode/<string:zip>",methods=['GET'])
def GetItemZIP(yr,zip):
    curs = g.sql_conn.cursor()
    if yr == '2016':
        curs.execute("select * from Tax_Data_2016 where ZIPCODE = ?", zip)
    elif yr == '2015':
        curs.execute("select * from Tax_Data_2015 where ZIPCODE = ?", zip)
    elif yr == '2014':
        curs.execute("select * from Tax_Data_2014 where ZIPCODE = ?", zip)
    elif yr == '2013':
        curs.execute("select * from Tax_Data_2013 where ZIPCODE = ?", zip)
    columns = [column[0] for column in curs.description]
    data = []

    for row in curs.fetchall():
        data.append(dict(zip(columns, row)))

    return json.dumps(data, indent=4, sort_keys=True, default=str)


@app.route("/taxdata/byzip/heatmap/<string:state>/<string:option>",methods=['GET'])
def ShowHeatMap(state,option):
    DataValue.HeatMap2(state)
    #file_name = 'HeatMap' + str(state) + '.jpg'
    #response = make_response(render_template("index.html"))
    if option == 'display':
        return render_template("index.html")#,image_name = file_name)
    elif option == 'download':
        return send_file('C://Users/mes12/Desktop/Fall 2018 - USU/MIS 5400/Final Project/static/HeatMap.jpg')

@app.route("/taxdata/state/heatmap/",methods=['GET'])
def ShowHeatMap1():
    DataValue.HeatMap()
    #file_name = 'HeatMap' + str(state) + '.jpg'
    #response = make_response(render_template("index.html"))
    
    return render_template("index1.html")#,image_name = file_name)
    
    
    
    
    return 'success', 200



if __name__ == '__main__':
    app.run(debug=True)

