
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from model.postgis import PostGis
from controller.zoom_controller import ZoomController
import tkinter as tk
import matplotlib.pyplot as plt

class ControllerGui:

    def __init__(self):
        self.db = PostGis()
        self.zoom_controller = ZoomController()

    def start(self):
        self.selected_objects = []
        self.db.connect()
    
    def stop(self):
        self.db.disconnect()

    def on_checkbox_toggle(self,obj_id, var, frame):
        if var.get():
            self.selected_objects.append(obj_id)
        else:
            self.selected_objects.remove(obj_id)
        self.update_plot(frame)

    def clear_plots(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()
    

    def plot_terrain(self, frame_or_ax):
        fig, ax = (None, frame_or_ax)
        #plt.subplots(figsize=(20, 20)) if isinstance(frame_or_ax, tk.Frame) else
        # Carregar dados das vistas e definir cores específicas
        views = {
            'v_floresta': '#228B22',  # fresh green
            'v_lago': '#ADD8E6',      # light blue
            'v_cultivo': '#FFD700',   # dark yellow
            'v_pantano': '#8B4513'    # dark brown
        }
        for view, colors in views.items():
            try:
                df = self.load_view_data(view, 'geo_terreno')
                if df is not None and not df.empty and df.geometry.is_valid.all():
                    print("Terrenos:\n", df)
                    df.plot(ax=ax, color=colors)
            except Exception as e:
                print(f"Error loading view {view}: {e}")

        if fig:
            canvas = FigureCanvasTkAgg(fig, master=frame_or_ax)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=1)


    # Função para plotar a trajetória e cinemática
    def plot_trajectory_and_kinematics(self, selected_objects, ax):
        # Plotar terreno
        print("Plotting terrain")
        self.plot_terrain(ax)

        for obj_id in selected_objects:

            # Plotar trajetória
            print("Plotting trajectory")
            traj_view = f"v_trajectoria_{obj_id}"
            traj_df = self.load_view_data(traj_view, 'geo_ponto')
            if traj_df is not None and not traj_df.empty:
                print("Trajetórias:\n", traj_df)
                traj_df.plot(ax=ax, color='red', label=f'Trajectory {obj_id}', aspect=1)
            
            # Plotar cinemática
            print("Plotting kinematics")
            kin_view = f"v_cinematica_{obj_id}"
            corpo_df = self.load_view_data(kin_view, 'geo_corpo')
            posicao_df = self.load_view_data(kin_view, 'g_posicao')
            pos = posicao_df['g_posicao'][0]
            if corpo_df is not None and not corpo_df.empty and corpo_df.geometry.is_valid.all():
                corpo_df.plot(ax=ax, color='black', label=f'Kinematics {obj_id}', aspect=1)
                ax.text(pos.x+20, pos.y+20, f'({round(pos.x, 2)}, {round(pos.y, 2)})', fontsize=8, ha='center')

    def update_plot(self, frame):
        self.clear_plots(frame)

        fig, ax = plt.subplots() #figsize=(10, 10)
        fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
        canvas = FigureCanvasTkAgg(fig, master=frame)
        self.plot_trajectory_and_kinematics(self.selected_objects, ax)
        ax.set_xticks([])  # Remover valores do eixo x
        ax.set_yticks([])  # Remover valores do eixo y
        ax.set_aspect('auto')
        ax.axis('off')
        self.zoom_controller.setup_zoom_and_drag(canvas, ax)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=1)

    def on_submit(self, ni, frame):
        print("Atualizando gráfico", ni)
        self.db.simular_perseguicao(ni)
        self.update_plot(frame)

    def load_object_types(self):
        return self.db.get_objetos_types()
    
    def load_view_data(self, view_name, geom_col):
        return self.db.get_view(view_name, geom_col)
