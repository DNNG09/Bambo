from env import Database_Data
import mysql.connector

class Database:
    try: 
        db = mysql.connector.connect(
            host = Database_Data.DATABASE_HOST,
            user = Database_Data.DATABASE_USER,
            password = Database_Data.DATABASE_PASSWORD,
            database = Database_Data.DATABASE_NAME,
            auth_plugin="mysql_native_password"
        )
        cursor = db.cursor(buffered=True)
    except Exception as e:
        print(e)
        quit()