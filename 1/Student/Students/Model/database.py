import mysql.connector as mc
from Students.Misc.Functions.read_db_config import read_db_config

class Database:

    def connect(self):
        try:
            db_config = read_db_config()
            db_config['database'] = 'horace' 
            return mc.connect(**db_config)
        except mc.Error as e:
            return
