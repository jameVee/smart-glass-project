import sqlite3
import json
from flask import Flask, render_template, request, url_for, flash, redirect, jsonify

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.htm")

@app.route("/api_get_data/", methods=['GET'])
def api_get_data():

    db_file = "smartGlassesDB.db"
    sqlite_select_query = """SELECT * FROM Acquaintance"""

    sqliteConnection = sqlite3.connect(db_file)
    sqliteConnection.row_factory = sqlite3.Row 
    cursor = sqliteConnection.cursor()

    cursor.execute(sqlite_select_query)

    records = cursor.fetchall()

    cursor.close()
    sqliteConnection.close()

    data_json_form = json.dumps( [dict(ix) for ix in records], indent=2 )
    
    #return jsonify(data_json_form).json()
    return data_json_form

@app.route("/api_post_data/", methods=['POST'])
def api_post_data():
    if request.is_json:
        json_data = request.get_json()
        print(f"json data = {json_data}")
        sqlstatement = ''
        TABLE_NAME = ''

        for TABLE_NAME, data in json_data.items():

            print('Table : ', TABLE_NAME)
            print('Data : ', data)

            firstrecord = True

            for record in data:


                keylist = "("
                valuelist = "("
                firstPair = True

                for key, value in record.items():
                    if not firstPair:
                        keylist += ", "
                        valuelist += ", "
                    firstPair = False
                    keylist += key
                    #if type(value) in (str, unicode):
                    if type(value) == str:
                        valuelist += "'" + value + "'"
                    else:
                        valuelist += str(value)

                keylist += ")"
                valuelist += ")"

                if firstrecord:
                    firstrecord = False;
                    sqlstatement += "INSERT INTO " + TABLE_NAME + " " + keylist + " VALUES " + valuelist
                else:
                    sqlstatement += ", " + valuelist
        
        db_file = "smartGlassesDB.db"

        sqliteConnection = sqlite3.connect(db_file)
        cursor = sqliteConnection.cursor()
        cursor.execute(sqlstatement)
        sqliteConnection.commit()

        cursor.close()
        sqliteConnection.close()
        
        print(sqlstatement)
        return sqlstatement, 201
    return {"error": "Request must be JSON"}, 415

@app.route("/api_delete_data/", methods=['POST'])
def api_delete_data():
    if request.is_json:

        json_data = request.get_json()
        print(f"json data = {json_data}")
        sqlstatement = ''
        TABLE_NAME  = ''
        keylist     = ''
        valuelist   = ''

        for TABLE_NAME, data in json_data.items():

            print('Table : ', TABLE_NAME)
            print('Data : ', data)
            
            i = 0
            firstRecord = True

            for record in data:                               
                for key, value in record.items():
                    print(i," key: ",key," value: ",value)
                    keylist = key
                    if firstRecord:
                        firstRecord = False
                        valuelist   += str(value)                        
                    else:
                        valuelist   += ", "
                        valuelist   += str(value)                    
                i += 1
                    
            sqlstatement += "DELETE FROM " + TABLE_NAME + " WHERE " + keylist + " IN (" + valuelist + ")"
            
        
        db_file = "smartGlassesDB.db"

        sqliteConnection = sqlite3.connect(db_file)
        cursor = sqliteConnection.cursor()
        cursor.execute(sqlstatement)
        sqliteConnection.commit()

        cursor.close()
        sqliteConnection.close()
        
        print(sqlstatement)                    

        return sqlstatement, 201
    return {"error": "Request must be JSON"}, 415