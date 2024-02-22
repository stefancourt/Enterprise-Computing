import sqlite3

database = "database.db"

class Airport:
    def __init__(self,code,name):
        self.code = code
        self.name = name
        
def main():
    # set up database
    with sqlite3.connect("database.db") as connection:
        cursor = connection.cursor()
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS airports" + 
            "(code TEXT PRIMARY KEY , name TEXT)"
        )
        connection.commit()

    # insert a record
    airport = Airport("LHR", "London Heathrow")
    with sqlite3.connect("database.db") as connection:
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO airports(code, name) VALUES (?,?)",
            (airport.code,airport.name)
        )
        connection.commit()
        print(cursor.rowcount > 0)

    # lookup a record
    code = "LHR"
    with sqlite3.connect("database.db") as connection:
        cursor = connection.cursor()
        cursor.execute(
            "SELECT code, name FROM airports WHERE code=?", (code,)
        )
        row = cursor.fetchone()
        if row:
            airport = Airport(row[0], row[1])
        else:
            airport = None
        
        if airport != None:
            print(airport.code, airport.name)

    # insert another records
    airport = Airport("PEK","Peking")
    with sqlite3.connect("database.db") as connection:
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO airports(code,name) VALUES (?,?)",
            (airport.code,airport.name)
        )
        connection.commit()
        print(cursor.rowcount > 0)

    airport = Airport("PEK","Beijing")
    with sqlite3.connect("database.db") as connection:
        cursor = connection.cursor()
        cursor.execute(
            "UPDATE airports SET name=? WHERE code=?",
            (airport.namsource,airport.code)
        )
        connection.commit()
        print(cursor.rowcount > 0)

    code = "PEK"
    with sqlite3.connect("database.db") as connection:
        cursor = connection.cursor()
        cursor.execute(
            "SELECT code, name FROM airports WHERE code=?",(code,)
        )
        row = cursor.fetchone()
        if row:
            airport = Airport(row[0],row[1])
        else:
            airport = None

        if airport != None:
            print(airport.code,airport.name)


if __name__ == "__main__":
    main()