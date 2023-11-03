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
    
    # This will try join the trainer table and booking table and then eventually the user data one as well
    def bookingDB(self):
        conn = self.connect()
        cur = conn.cursor()
        create_temp_table_sql = """
CREATE TEMPORARY TABLE temp_tbl AS
    SELECT *
    FROM Booking_Data_TBL
    CROSS JOIN Trainer_TBL
    USING (Trainer_ID);
"""
        cur.execute(create_temp_table_sql)
        select_from_temp_table_sql = """
SELECT Booking_ID, Booking_Name, Booking_Details, Booking_Availability, User_Name, User_Profile, User_First_Name, User_Last_Name
FROM temp_tbl
CROSS JOIN User_Data_TBL
USING (User_ID);
"""     
        cur.execute(select_from_temp_table_sql)
        conn.commit() # commits to the transactions
        result = cur.fetchall()
        return result

    def bookingDropTempTBLDB(self):
        conn = self.connect()
        cur = conn.cursor()
        drop_temp_table_sql = "DROP TABLE temp_tbl"
        cur.execute(drop_temp_table_sql)
#--------------------------------------------------------------------------------------------------------------------------------------------------#

    # close out database
    def disconnect(self, conn):
        conn.close() # This will close the connection to the databaseand release any resources that were being used


