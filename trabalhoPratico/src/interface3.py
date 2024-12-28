
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from database import PostGis
import pandas as pd


class ZoomController:

    def setup_zoom_and_drag(self, canvas, ax):
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
                scale_factor = 0.9 if event.button == 'up' else 1.1
                xlim = ax.get_xlim()
                ylim = ax.get_ylim()
                ax.set_xlim([x * scale_factor for x in xlim])
                ax.set_ylim([y * scale_factor for y in ylim])
                canvas.draw()

        canvas.mpl_connect('button_press_event', on_press)
        canvas.mpl_connect('scroll_event', on_zoom)


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
                df = self.load_view_data(view, 'geo_terreno')
                if not df.empty and df.geometry.is_valid.all():
                    print("Terrenos:\n", df)
                    df.plot(ax=ax, color=colors)
            except Exception as e:
                print(f"Error loading view {view}: {e}")

        if fig:
            canvas = FigureCanvasTkAgg(fig, master=frame_or_ax)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=1)


    # Função para plotar a trajetória e cinemática
    def plot_trajectory_and_kinematics(self, selected_objects, canvas, ax):
        # Plotar terreno
        print("Plotting terrain")
        self.plot_terrain(ax)

        for obj_id in selected_objects:

            # Plotar cinemática
            print("Plotting kinematics")
            kin_view = f"v_cinematica_{obj_id}"
            kin_df = self.load_view_data(kin_view, 'g_posicao')
            if not kin_df.empty:
                print("Cinemáticas:\n", kin_df)
                kin_df.plot(ax=ax, color='blue', label=f'Kinematics {obj_id}', aspect=1)

            # Plotar trajetória
            print("Plotting trajectory")
            traj_view = f"v_trajectoria_{obj_id}"
            traj_df = self.load_view_data(traj_view, 'geo_ponto')
            if not traj_df.empty:
                print("Trajetórias:\n", traj_df)
                traj_df.plot(ax=ax, color='red', label=f'Trajectory {obj_id}', aspect=1)

        print("Drawing canvas")
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=1)

    def update_plot(self, frame):
        self.clear_plots(frame)
        fig, ax = plt.subplots(figsize=(6, 10))
        canvas = FigureCanvasTkAgg(fig, master=frame)
        self.plot_trajectory_and_kinematics(self.selected_objects, canvas, ax)
        ax.set_xticks([])  # Remover valores do eixo x
        ax.set_yticks([])  # Remover valores do eixo y
        self.zoom_controller.setup_zoom_and_drag(canvas, ax)

    def on_submit(self, ni):
        print("Atualizando gráfico", ni)

    def load_object_types(self):
        return self.db.get_objetos_types()
    
    def load_view_data(self, view_name, geom_col):
        return self.db.get_view(view_name, geom_col)


class GUI:
    def __init__(self):
        self.root = tk.Tk()
        self.controller = ControllerGui()
    
    def create(self, icon_path):
        self.controller.start()
        self.root.title("Fuga Selvagem - Trajetórias e Cinemáticas")

        # Definir o ícone da aplicação
        self.root.iconbitmap(icon_path)

        self.paned_window = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        self.paned_window.pack(fill=tk.BOTH, expand=1)
        self.__create_checkbox()
        self.__create_map()
        

    def start(self):
        self.root.mainloop()

    def destroy(self):
        self.controller.stop()

    def __create_checkbox(self):
        # Área para checkboxes (15%)
        control_frame = tk.Frame(self.paned_window)
        self.paned_window.add(control_frame, weight=1)
        self.__create_controls(control_frame)

    def __create_map(self):
        # Área do gráfico (85%)
        self.graph_frame = tk.Frame(self.paned_window)
        self.paned_window.add(self.graph_frame, weight=4)
        self.controller.update_plot(self.graph_frame)

    def __create_controls(self, frame):
        tk.Label(frame, text="Selecione o Animal", font=('Arial', 20)).pack()
        object_types = self.controller.load_object_types()
        for _, row in object_types.iterrows():
            obj_id = row['id']
            obj_name = row['nome']
            var = tk.BooleanVar()
            chk = tk.Checkbutton(frame, text=f'{obj_name} (ID: {obj_id})', variable=var, command=lambda id=obj_id, var=var: self.controller.on_checkbox_toggle(id, var, self.graph_frame), anchor='w', font=('Arial', 12))
            chk.pack(anchor='w', padx=16)


        submit_button = tk.Button(frame, text="Atualizar", command=lambda : self.controller.on_submit(text_input.get()), font=('Arial', 12))
        submit_button.pack(pady=16, side=tk.BOTTOM)

        text_input = tk.Entry(frame, font=('Arial', 12))
        text_input.insert(10, "10")
        text_input.pack(side=tk.BOTTOM , padx=16, pady=8)

        tk.Label(frame, text="Número de Iterações", font=('Arial', 16)).pack(side=tk.BOTTOM)

        divider = tk.Frame(frame, height=2, bd=1, relief=tk.SUNKEN)
        divider.pack(fill=tk.X, side=tk.BOTTOM, pady=16)
        

if __name__ == "__main__":
    icon_path = r"C:\Users\A40610\Desktop\SIGM2425\trabalhoPratico\src\interface\imgs\postgres.ico"
    #icon_path = r"C:\Users\ana.sofia.oliveira\Documents\ISEL\SIGM2425\trabalhoPratico\src\interface\imgs\postgres.ico"
    gui = GUI()
    gui.create(icon_path)
    gui.start()


