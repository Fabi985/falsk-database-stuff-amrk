import sqlite3

class Database:
    def __init__(self):
        # defines our database "SQLTask.db"
        self.DBname = 'Simple_Library_DB.db'

    # Create a database connection
    def connect(self):
        conn = None
        try:
            conn = sqlite3.connect(self.DBname)
        except Exception as e:
            print(e)
        return conn
    
    # Create a query function
    def queryDB(self, command, params=[]):
        conn = self.connect()
        cur = conn.cursor() # Creates a new cursor object for SQL statements
        cur.execute(command, params) # Executes the update based on provided parameters

        # fetchall() - it fetches all rowsin a reuskt set. If some rows have already been extracted from the rest
        result = cur.fetchall() # Gets al the results
        self.disconnect(conn) # call the disconnect function
        return result
    
    # create an update function
    def updateDB(self, command, params=[]):
        conn = self.connect()
        cur = conn.cursor() # Creates a new cursor object for SQL statements
        cur.execute(command, params) # Executes the update based on provided parameters

        # Commit changes to the database
        conn.commit() # commits to the transactions
        result = cur.fetchall() # Gets al the results
        self.disconnect(conn) # call the disconnect function
        return result

#--------------------------------------------------------------------------------------------------------------------------------------------------#

    # close out database
    def disconnect(self, conn):
        conn.close() # This will close the connection to the databaseand release any resources that were being used


