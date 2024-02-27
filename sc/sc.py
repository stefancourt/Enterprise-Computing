from flask import Flask, request
import sqlite3
import os
import firebase_admin
from firebase_admin import credentials, db
import argparse

cred = None
firebase_db = None
firebase_mode = None

DATABASE = "cells.db"
app = Flask(__name__)

def setup_firebase():
    global cred, firebase_db, firebase_mode
    firebase_db_name = os.environ.get('FBASE')
    cred = credentials.Certificate("spreadsheet-208ca-firebase-adminsdk-lgvvw-a3a2ff7b65.json")
    firebase_admin.initialize_app(cred, {
        'databaseURL': f'https://{firebase_db_name}-default-rtdb.europe-west1.firebasedatabase.app'
    })
    firebase_db = db.reference('cells')
    firebase_mode = "test"

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
    if firebase_db:
        return firebase_db
    else:
        conn = sqlite3.connect(DATABASE)
        return conn

def change_formula(formula):
    formula = formula.replace('×', '*')
    formula = formula.replace('÷', '/')
    test_formula = formula.split(" ")
    id_list = list()
    print(test_formula)
    print(id_list[0])
    for i in test_formula:
        print(str(i))
        for j in id_list[0]:
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
                    cell_formula = conn.child(j).get()
                    print(str(cell_formula))
                    formula = formula.replace(str(j), "(" + str(cell_formula) + ")")
    print(formula)
    try:
        result = eval(formula)
        print(result)
        return result
    except:
        return change_formula(formula)

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
    else:
        existing_cell = conn.child(js_id).get()
        if existing_cell:
            conn.child(js_id).set(formula)
            return '', 204  # No Content - Updated
        else:
            conn.child(js_id).set(formula)
            return '', 201, {"Location": "/cells/" + js_id}
    return '', 201, {"Location": "/cells/" + js_id}  # OK

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
        conn.child(id).delete()
        return '', 204

@app.route("/cells", methods=["GET"])
def list():
    conn = create_connection()
    if isinstance(conn, sqlite3.Connection):
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM cells")
        cells = cursor.fetchall()
        conn.close()
        cell_ids = [cell[0] for cell in cells]
        return cell_ids, 200
    else:
        try:
            cell_ids = conn.get().keys()
            cell_ids_list = [k  for  k in  cell_ids]
            print([k  for  k in  cell_ids])
            return cell_ids_list, 200
        except:
            return [], 200

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
        cell_formula = conn.child(id).get()
        if cell_formula is not None:
            cell_formula = change_formula(cell_formula)
            print(cell_formula)
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