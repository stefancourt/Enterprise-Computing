from flask import Flask, request
import json
import sqlite3
import os
import requests
import argparse

FBASE = "firebase-database"

FIREBASE_URL = f"https://{FBASE}-default-rtdb.europe-west1.firebasedatabase.app/"
DATABASE = "cells.db"

app = Flask(__name__)
n = 0
def setup_firebase():
    data={}
    response = requests.post(FIREBASE_URL+"cells.json", json=data)
    if response.status_code == 200: 
        global n
        n = 1
        print("Table created successfully.")
    else:
        print("Failed to create table:", response.text)

def firebase_get():
    response = requests.get(FIREBASE_URL+"cells.json")
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to GET data from Firebase:", response.text)
        return None

def setup_sqlite():
    # set up the SQLite database
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS cells" +
                   "(id TEXT PRIMARY KEY, formula TEXT)")
    conn.commit()
    conn.close()

def setup_database(database_flag):
    if database_flag == 'firebase':
        setup_firebase()
    elif database_flag == 'sqlite':
        setup_sqlite()

def create_connection():
    global n
    if n == 1:
        conn = False
        return conn
    else:
        conn = sqlite3.connect(DATABASE)
        return conn

def change_formula(formula, is_first=True):
    formula = formula.replace('×', '*')
    formula = formula.replace('÷', '/')
    test_formula = formula.split(" ")
    id_list = list_ids()
    print(id_list)
    id_list_formula = id_list + ['+', '-', '*', '/']
    if is_first == True:
        for i in range(len(test_formula)):
            if test_formula[i] not in id_list_formula and not test_formula[i].isnumeric():
                formula = formula.replace(str(test_formula[i]), "(" + str(0) + ")")
    for i in test_formula:
        print(str(i))
        for j in id_list:
            if j in i:
                conn = create_connection()
                if isinstance(conn, sqlite3.Connection):
                    cursor = conn.cursor()
                    cursor.execute("SELECT formula FROM cells WHERE id=?", (j,))
                    cell_formula = cursor.fetchone()
                    print(str(cell_formula[0]))
                    formula = formula.replace(str(j), "(" + str(cell_formula[0]) + ")")
                    conn.close()
                else:
                    response = requests.get(FIREBASE_URL + "cells/" + j + ".json")
                    cell_formula = response.json()
                    formula = formula.replace(str(i), "(" + str(cell_formula) + ")")
    print(formula)
    try:
        result = eval(formula)
        print(result)
        return result
    except:
        return change_formula(formula, is_first=False)

def list_ids():
    conn = create_connection()
    if isinstance(conn, sqlite3.Connection):
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM cells")
        cells = cursor.fetchall()
        conn.close()
        cell_ids = [cell[0] for cell in cells]
        return cell_ids
    else:
        response = requests.get(FIREBASE_URL + "cells.json")
        if response.json() !=  None:
            cell_ids = response.json().keys()
            cell_ids_list = [k  for  k in  cell_ids]
            return cell_ids_list
        else:
            return []

@app.route('/cells/<string:id>', methods=["PUT"])
def create(id):
    js = request.get_json()
    js_id = js.get("id")
    formula = js.get("formula")
    if js_id == None or formula == None:
        return '', 400  # Bad Request
    if js_id != id:
        return '', 400  # Bad Request
    conn = create_connection()
    if isinstance(conn, sqlite3.Connection):
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM cells WHERE id=?', (js_id,))
        existing_cell = cursor.fetchone()
        if existing_cell:
            cursor.execute('UPDATE cells SET formula=? WHERE id=?', (formula, js_id))
            conn.commit()
            conn.close()
            return '', 204  # No Content
        cursor.execute("INSERT INTO cells (id, formula) VALUES (?, ?)", (js_id, formula))
        conn.commit()
        conn.close()
        return '', 201, {"Location": "/cells/" + js_id}  # OK
    else:
        response = requests.get(FIREBASE_URL + "cells/" + js_id + ".json")
        print(response.json())
        if response.json() != None:
            requests.put(FIREBASE_URL+"cells/"+js_id+".json", json=formula)
            return '', 204  # No Content - Updated
        else:
            requests.put(FIREBASE_URL+"cells/"+js_id+".json", json=formula)
            return '', 201, {"Location": "/cells/" + js_id}

@app.route("/cells/<string:id>", methods=["DELETE"])
def delete(id):
    conn = create_connection()
    if isinstance(conn, sqlite3.Connection):
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM cells WHERE id=?", (id,))
        existing_cell = cursor.fetchone()
        if existing_cell:
            cursor.execute("DELETE FROM cells WHERE id=?", (id,))
            conn.commit()
            conn.close()
            return '', 204
        else:
            conn.close()
            return '', 404
    else:
        response = requests.delete(FIREBASE_URL + "cells/" + id + ".json")
        if response.status_code == 200:
            return '', 204
        else:
            return '', 404

@app.route("/cells", methods=["GET"])
def list():
    conn = create_connection()
    if isinstance(conn, sqlite3.Connection):
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM cells")
        cells = cursor.fetchall()
        conn.close()
        cell_ids = [cell[0] for cell in cells]
        return json.dumps(cell_ids), 200
    else:
        response = requests.get(FIREBASE_URL + "cells.json")
        if response.json() !=  None:
            cell_ids = response.json().keys()
            cell_ids_list = [k  for  k in  cell_ids]
            return json.dumps(cell_ids_list), 200
        else:
            return json.dumps([]), 200

@app.route("/cells/<string:id>", methods=["GET"])
def read(id):
    conn = create_connection()
    if isinstance(conn, sqlite3.Connection):
        cursor = conn.cursor()
        cursor.execute("SELECT formula FROM cells WHERE id=?", (id,))
        cell_formula = cursor.fetchone()
        conn.close()
        if cell_formula is not None:
            cell_formula = change_formula(cell_formula[0])
            print(cell_formula)
            return {"id": id, "formula": str(cell_formula)}, 200
        else:
            return '', 404
    else:
        response = requests.get(FIREBASE_URL + "cells/" + id + ".json")
        data = response.json()
        print(data)
        if data is not None:
            cell_formula = change_formula(data)
            print(data)
            return {"id": id, "formula": str(cell_formula)}, 200
        else:
            return '', 404

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--database", help="Set database type. Options: firebase, sqlite", type=str)
    args = parser.parse_args()
    database_flag = args.database if args.database else None
    setup_database(database_flag)
    app.run(host="localhost", port=3000)