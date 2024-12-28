from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
import geopandas as gpd
import numpy as np
import pandas as pd

# Configurações de conexão com o banco de dados
DB_NAME = "fuga_selvagem"
DB_USER = "postgres"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_PASSWORD = "123456"  # Adicione sua senha aqui

class Database:

    def __init__(self):
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



class PostGis(Database):

    def __init__(self):
        super().__init__()

    def read_postgis(self, query, geom_col=None):
        try:
            print("Query:", query)
            df = gpd.read_postgis(text(query), self.connection, geom_col=geom_col)
            print("Columns available:", df.columns)
            return df
        except SQLAlchemyError as e:
            print(f"Error executing query: {e}")
        except Exception as e:
            print(f"Error executing query: {e}")
    
    def validate_geometry(self, df, geom_col):
         # Verificar se a coluna de geometria está presente
        if geom_col not in df.columns:
            raise ValueError(f"Query missing geometry column '{geom_col}'")
        
        # Criar GeoDataFrame com a coluna de geometria correta
        gdf = gpd.GeoDataFrame(df, geometry=geom_col)
        
        # Verificar e corrigir geometrias inválidas
        gdf = gdf[gdf.is_valid]
        
        # Verificar se as coordenadas são finitas
        gdf = gdf[gdf.geometry.apply(lambda geom: np.all(np.isfinite(geom.bounds)))]
        
        return gdf
    
    def simular_perseguicao(self, num_iteracoes):
        query = f"SELECT simular_perseguicao({num_iteracoes})"
        self.read_sql(query)
        query = "SELECT criar_views_objetos()"
        self.read_sql(query)

    def get_view(self, view_name, geom_col):
        query = f"SELECT * FROM {view_name}"
        df = self.read_postgis(query, geom_col=geom_col)
        return df

    def get_objetos_types(self):
        query = "select obj.id_objeto_movel as id, tipo_obj.nome as nome from objeto_movel as obj left join tipo_objeto_movel as tipo_obj on obj.id_tipo_objeto_movel = tipo_obj.id_tipo_objeto_movel"
        df = self.read_sql(query)
        return df
    
