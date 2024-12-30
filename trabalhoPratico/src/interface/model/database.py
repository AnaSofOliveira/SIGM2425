from sqlalchemy import create_engine, text
import pandas as pd
import json
import os
from config.config import DATABASE_CONFIG_PATH

class Database2:

    def __init__(self):

        config_path = DATABASE_CONFIG_PATH

        with open(config_path, 'r') as config_file:
            config = json.load(config_file)

        DB_NAME = config.get("DB_NAME")
        DB_USER = config.get("DB_USER")
        DB_HOST = config.get("DB_HOST")
        DB_PORT = config.get("DB_PORT")
        DB_PASSWORD = config.get("DB_PASSWORD")

        self.url = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
        self.__engine = create_engine(self.url)
    
    # Função para conectar ao banco de dados usando SQLAlchemy
    def connect(self):
        try:
            self.connection = self.__engine.connect()
            print("Connection to database established successfully.")
        except Exception as e:
            print(f"Error connecting to database: {e}")

    def disconnect(self):
        try:
            if self.connection:
                self.connection.close()
            print("Connection to database closed successfully.")
        except Exception as e:  
            print(f"Error closing connection to database: {e}")

    def read_sql(self, query):
        try:
            print("Query:", query)
            return pd.read_sql(text(query), self.connection)
        except Exception as e:
            print(f"Error executing query: {e}")



    
