import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

class Database:
    try: 
        db = mysql.connector.connect(
            host = os.getenv('DATABASE_HOST'),
            user = os.getenv('DATABASE_USER'),
            password = os.getenv('DATABASE_PASSWORD'),
            database = os.getenv('DATABASE_NAME'),
            auth_plugin="mysql_native_password"
        )
        cursor = db.cursor(buffered=True)
    except Exception as e:
        print(e)
        quit()