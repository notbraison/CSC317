import mysql.connector
import os

db_config = {
    "host": os.environ['DATABASE_HOST'],
    "user": os.environ['DATABASE_USERNAME'],
    "password": os.environ['DATABASE_PASSWORD'],
    "database": os.environ['DATABASE'],
    "port": 3306
}

db_conn = mysql.connector.connect(**db_config)