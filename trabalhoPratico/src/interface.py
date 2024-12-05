import tkinter as tk
from tkinter import ttk
from sqlalchemy import create_engine
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

# Configurações de conexão com o banco de dados
DB_NAME = "fuga_selvagem"
DB_USER = "postgres"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_PASSWORD = "postgres"  # Adicione sua senha aqui

# Função para conectar ao banco de dados usando SQLAlchemy
def connect_db():
    engine = create_engine(f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')
    return engine

# Função para carregar dados de uma view
def load_view_data(view_name, geom_col):
    print(f"Carregando dados da view {view_name}...")
    print("Coluna de geometria:", geom_col)
    engine = connect_db()
    query = f"SELECT * FROM {view_name}"
    df = gpd.read_postgis(query, engine, geom_col=geom_col)
    
    print("Colunas disponíveis:", df.columns)
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

# Função para plotar os dados fixos
def plot_fixed_data(ax):
    fixed_views = ["terreno"]
    for view_name in fixed_views:
        gdf = load_view_data(view_name, 'geo_terreno')
        gdf.plot(ax=ax, label=view_name, alpha=0.5)

# Função para plotar os dados selecionados
def plot_selected_data(ax, selected_views):
    for view_name, title in selected_views:
        gdf = load_view_data(view_name, 'geo_ponto')
        gdf.plot(ax=ax, label=title)

# Função para atualizar a visualização
def update_plot():
    selected_views = []
    for view_name, var, title in checkbox_order:
        if var.get():
            selected_views.append((view_name, title))
    
    ax.clear()
    plot_fixed_data(ax)
    plot_selected_data(ax, selected_views)
    ax.set_aspect('equal')  # Ajustar o aspecto do ax para garantir que ele seja válido
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles, labels)
    canvas.draw()

# Função para lidar com o clique no checkbox
def on_checkbox_click(view_name, var, title):
    if var.get():
        checkbox_order.append((view_name, var, title))
    else:
        checkbox_order.remove((view_name, var, title))
    update_plot()

# Função para criar a interface gráfica
def create_gui():
    global root, canvas, ax, view_vars, checkbox_order
    root = tk.Tk()
    root.title("Visualização de Dados Geoespaciais")

    # Definir a janela para ocupar 90% da tela cheia
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    window_width = int(screen_width * 0.9)
    window_height = int(screen_height * 0.9)
    root.geometry(f"{window_width}x{window_height}")

    # Frame para os checkboxes
    frame = ttk.Frame(root, padding="10")
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

    # Canvas para plotagem
    canvas_width = window_width - 200  # Ajustar a largura do canvas, subtraindo a largura do frame das checkboxes
    canvas_height = window_height
    fig, ax = plt.subplots(figsize=(canvas_width / 100, canvas_height / 100))  # Ajustar o tamanho do canvas
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.get_tk_widget().grid(row=0, column=1, rowspan=20, sticky=(tk.N, tk.S, tk.E, tk.W))

    # Ajustar o layout do canvas
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)

    # Plotar dados fixos inicialmente
    plot_fixed_data(ax)
    ax.set_aspect('equal')  # Ajustar o aspecto do ax para garantir que ele seja válido
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles, labels)
    canvas.draw()

    root.mainloop()

# Executar a interface gráfica
if __name__ == "__main__":
    create_gui()