from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
import geopandas as gpd
import numpy as np
from model.database import Database

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
        query = "SELECT criar_views_terrenos()"
        self.read_sql(query)

    def get_view(self, view_name, geom_col):
        query = f"SELECT * FROM {view_name}"
        df = self.read_postgis(query, geom_col=geom_col)
        return df

    def get_objetos_types(self):
        query = "select obj.id_objeto_movel as id, tipo_obj.nome as nome from objeto_movel as obj left join tipo_objeto_movel as tipo_obj on obj.id_tipo_objeto_movel = tipo_obj.id_tipo_objeto_movel"
        df = self.read_sql(query)
        return df