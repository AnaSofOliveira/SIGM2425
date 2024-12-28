import tkinter as tk
from tkinter import ttk
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from sqlalchemy import create_engine

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
    engine = connect_db()
    query = f"SELECT * FROM {view_name}"
    df = gpd.read_postgis(query, engine, geom_col=geom_col)
    return df

# Função para carregar tipos de objetos móveis
def load_object_types():
    engine = connect_db()
    query = "select obj.id_objeto_movel as id, tipo_obj.nome as nome from objeto_movel as obj left join tipo_objeto_movel as tipo_obj on obj.id_tipo_objeto_movel = tipo_obj.id_tipo_objeto_movel"
    df = pd.read_sql(query, engine)
    return df

class ZoomPan:
    def __init__(self, ax):
        self.ax = ax
        self.press = None

# Lista global para armazenar as seleções
selected_objects = []

# Função para criar a interface gráfica
def create_gui():
    global graph_frame  # Definir graph_frame como global
    root = tk.Tk()
    root.title("Fuga Selvagem - Trajetórias e Cinemáticas")

    # Definir o ícone da aplicação
    icon_path = r"C:\Users\ana.sofia.oliveira\Documents\ISEL\SIGM2425\trabalhoPratico\src\interface\imgs\postgres.ico"
    root.iconbitmap(icon_path)

    paned_window = ttk.PanedWindow(root, orient=tk.HORIZONTAL)
    paned_window.pack(fill=tk.BOTH, expand=1)

    # Área para checkboxes (15%)
    control_frame = tk.Frame(paned_window)
    paned_window.add(control_frame, weight=1)
    create_controls(control_frame)

    # Área do gráfico (85%)
    global graph_frame
    graph_frame = tk.Frame(paned_window)
    paned_window.add(graph_frame, weight=4)
    update_plot()

    root.mainloop()

# Função para criar os checkboxes
def create_controls(frame):
    tk.Label(frame, text="Selecione o Animal", font=('Arial', 20)).pack()
    object_types = load_object_types()
    for _, row in object_types.iterrows():
        obj_id = row['id']
        obj_name = row['nome']
        var = tk.BooleanVar()
        chk = tk.Checkbutton(frame, text=f'{obj_name} ({obj_id})', variable=var, command=lambda id=obj_id, var=var: on_checkbox_toggle(id, var), anchor='w', font=('Arial', 12))
        chk.pack()

# Função chamada quando uma checkbox é selecionada/deselecionada
def on_checkbox_toggle(obj_id, var):
    global selected_objects
    if var.get():
        selected_objects.append(obj_id)
    else:
        selected_objects.remove(obj_id)
    update_plot()

# Função para atualizar o gráfico com base nas seleções
def update_plot():
    clear_plots()
    fig, ax = plt.subplots(figsize=(6, 10))
    canvas = FigureCanvasTkAgg(fig, master=graph_frame)
    plot_trajectory_and_kinematics(selected_objects, canvas, ax)
    ax.set_xticks([])  # Remover valores do eixo x
    ax.set_yticks([])  # Remover valores do eixo y
    setup_zoom_and_drag(canvas, ax)

# Função para plotar a trajetória e cinemática
def plot_trajectory_and_kinematics(selected_objects, canvas, ax):
    # Plotar terreno
    print("Plotting terrain")
    plot_terrain(ax)

    for obj_id in selected_objects:

        # Plotar cinemática
        print("Plotting kinematics")
        kin_view = f"v_cinematica_{obj_id}"
        kin_df = load_view_data(kin_view, 'g_posicao')
        if not kin_df.empty:
            print("Cinemáticas:\n", kin_df)
            kin_df.plot(ax=ax, color='blue', label=f'Kinematics {obj_id}', aspect=1)

        # Plotar trajetória
        print("Plotting trajectory")
        traj_view = f"v_trajectoria_{obj_id}"
        traj_df = load_view_data(traj_view, 'geo_ponto')
        if not traj_df.empty:
            print("Trajetórias:\n", traj_df)
            traj_df.plot(ax=ax, color='red', label=f'Trajectory {obj_id}', aspect=1)

    print("Drawing canvas")
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=1)

# Função para limpar os gráficos
def clear_plots():
    for widget in graph_frame.winfo_children():
        widget.destroy()

# Função para configurar eventos de zoom e drag
def setup_zoom_and_drag(canvas, ax):
    def on_press(event):
        if event.button == 1:
            canvas.mpl_connect('motion_notify_event', on_drag)
            canvas.mpl_connect('button_release_event', on_release)
            on_press.x0, on_press.y0 = event.xdata, event.ydata

    def on_release(event):
        canvas.mpl_disconnect(canvas.mpl_connect('motion_notify_event', on_drag))
        canvas.mpl_disconnect(canvas.mpl_connect('button_release_event', on_release))

    def on_drag(event):
        if event.inaxes and event.button == 1:
            dx = event.xdata - on_press.x0
            dy = event.ydata - on_press.y0
            xlim = ax.get_xlim()
            ylim = ax.get_ylim()
            ax.set_xlim(xlim[0] - dx, xlim[1] - dx)
            ax.set_ylim(ylim[0] - dy, ylim[1] - dy)
            canvas.draw()

    def on_zoom(event):
        if event.inaxes:
            scale_factor = 1.1 if event.button == 'up' else 0.9
            xlim = ax.get_xlim()
            ylim = ax.get_ylim()
            ax.set_xlim([x * scale_factor for x in xlim])
            ax.set_ylim([y * scale_factor for y in ylim])
            canvas.draw()

    canvas.mpl_connect('button_press_event', on_press)
    canvas.mpl_connect('scroll_event', on_zoom)

# Função para plotar o terreno
def plot_terrain(frame_or_ax):
    fig, ax = plt.subplots(figsize=(6, 10)) if isinstance(frame_or_ax, tk.Frame) else (None, frame_or_ax)

    # Carregar dados das vistas e definir cores específicas
    views = {
        'v_florestas': '#228B22',  # fresh green
        'v_lagos': '#ADD8E6',      # light blue
        'v_cultivos': '#FFD700',   # dark yellow
        'v_pantanos': '#8B4513'    # dark brown
    }
    for view, colors in views.items():
        try:
            df = load_view_data(view, 'geo_terreno')
            if not df.empty and df.geometry.is_valid.all():
                print("Terrenos:\n", df)
                df.plot(ax=ax, color=colors)
        except Exception as e:
            print(f"Error loading view {view}: {e}")

    if fig:
        canvas = FigureCanvasTkAgg(fig, master=frame_or_ax)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=1)

if __name__ == "__main__":
    create_gui()