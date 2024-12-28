from sqlalchemy import create_engine, text
import geopandas as gpd
import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

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



class PostGis(Database):

    def __init__(self):
        super().__init__()

    def read_postgis(self, query, geom_col=None):
        try:
            print("Query:", query)
            df = gpd.read_postgis(text(query), self.connection, geom_col=geom_col)
            print("Columns available:", df.columns)
            return df
        except Exception as e:
            print(f"Error executing query: {e}")
    
    def validate_geometry(self, df, geom_col):
         # Verificar se a coluna de geometria está presente
        if geom_col not in df.columns:
            raise ValueError(f"Query missing geometry column '{geom_col}' in view {view_name}")
        
        # Criar GeoDataFrame com a coluna de geometria correta
        gdf = gpd.GeoDataFrame(df, geometry=geom_col)
        
        # Verificar e corrigir geometrias inválidas
        gdf = gdf[gdf.is_valid]
        
        # Verificar se as coordenadas são finitas
        gdf = gdf[gdf.geometry.apply(lambda geom: np.all(np.isfinite(geom.bounds)))]
        
        return gdf

    def get_terrenos(self):
        query = "SELECT * FROM terreno"
        df = self.read_postgis(query, geom_col='geo_terreno')
        return df


class GUI:
    
    def __init__(self):
        self.root = tk.Tk()
        self.db = PostGis()
        
    
    def create(self):
        self.db.connect()
        self.root.title("Visualização de Dados Geoespaciais")
        self._create_window()
        self._create_checkbox()
        self._create_canvas()

    def start(self):
        # Plotar dados fixos inicialmente
        self._show_terrenos(self.ax)
        self.ax.set_aspect('equal')  # Ajustar o aspecto do ax para garantir que ele seja válido
        handles, labels = self.ax.get_legend_handles_labels()
        self.ax.legend(handles, labels)
        self.canvas.draw()

        self.root.mainloop()

    def update(self):
        pass

    def destroy(self):
        self.db.disconnect()

    def _create_window(self):
        # Definir a janela para ocupar 90% da tela cheia
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.window_width = int(screen_width * 0.9)
        self.window_height = int(screen_height * 0.9)
        self.root.geometry(f"{self.window_width}x{self.window_height}")

    def _create_checkbox(self):
        # Frame para os checkboxes
        frame = ttk.Frame(self.root, padding="10")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        view_vars = []
        checkbox_order = []

        # Checkboxes para as views de trajetórias
        for i in range(1, 10):
            view_name = f"v_trajectoria_{i}"
            title = f"Trajetória {i}"
            var = tk.BooleanVar()
            checkbox = ttk.Checkbutton(frame, text=title, variable=var, 
                                    command=lambda vn=view_name, v=var, t=title: on_checkbox_click(vn, v, t))
            checkbox.grid(row=i, column=0, padx=5, pady=5)
            view_vars.append((view_name, var, title))

        # Checkboxes para as views de cinemática
        for i in range(1, 10):
            view_name = f"v_cinematica_{i}"
            title = f"Cinemática {i}"
            var = tk.BooleanVar()
            checkbox = ttk.Checkbutton(frame, text=title, variable=var, 
                                    command=lambda vn=view_name, v=var, t=title: on_checkbox_click(vn, v, t))
            checkbox.grid(row=i, column=1, padx=5, pady=5)
            view_vars.append((view_name, var, title))

    def _create_canvas(self):
        # Canvas para plotagem
        canvas_width = self.window_width - 200  # Ajustar a largura do canvas, subtraindo a largura do frame das checkboxes
        canvas_height = self.window_height
        self.fig, self.ax = plt.subplots(figsize=(canvas_width / 100, canvas_height / 100))  # Ajustar o tamanho do canvas
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().grid(row=0, column=1, rowspan=20, sticky=(tk.N, tk.S, tk.E, tk.W))

        # Ajustar o layout do canvas
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

    def _show_terrenos(self, ax):
        gdf = self.db.get_terrenos()
        gdf.plot(ax=ax, label='terreno', alpha=0.5)
        

# test database connection and postGis
if __name__ == "__main__":
    gui = GUI()
    gui.create()
    gui.start()



