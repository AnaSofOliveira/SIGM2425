from controller.controller_gui import ControllerGui
import tkinter as tk
from tkinter import ttk
from config.config import APP_NAME, ICON_PATH, TEXT_SIZE, FONT_FAMILY, TEXT_MAIN_LABEL, TEXT_UPDATE_BUTTON, TEXT_INTERATIONS_LABEL

class GUI:
    def __init__(self):
        self.root = tk.Tk()
        self.controller = ControllerGui()
    
    def create(self):
        self.controller.start()
        self.root.title(APP_NAME)

        # Definir o ícone da aplicação
        self.root.iconbitmap(ICON_PATH)

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
        tk.Label(frame, text=TEXT_MAIN_LABEL, font=(FONT_FAMILY, TEXT_SIZE)).pack()
        object_types = self.controller.load_object_types()
        for _, row in object_types.iterrows():
            obj_id = row['id']
            obj_name = row['nome']
            var = tk.BooleanVar()
            chk = tk.Checkbutton(frame, text=f'{obj_name} (ID: {obj_id})', variable=var, command=lambda id=obj_id, var=var: self.controller.on_checkbox_toggle(id, var, self.graph_frame), anchor='w', font=('Arial', 12))
            chk.pack(anchor='w', padx=16)


        submit_button = tk.Button(frame, text=TEXT_UPDATE_BUTTON, command=lambda : self.controller.on_submit(text_input.get(),self.graph_frame), font=('Arial', 12))
        submit_button.pack(pady=16, side=tk.BOTTOM)

        text_input = tk.Entry(frame, font=(FONT_FAMILY, TEXT_SIZE)) # REVIEW: Anteriormente a 12
        text_input.insert(10, "10")
        text_input.pack(side=tk.BOTTOM , padx=16, pady=8)

        tk.Label(frame, text=TEXT_INTERATIONS_LABEL, font=(FONT_FAMILY, TEXT_SIZE)).pack(side=tk.BOTTOM) # REVIEW: Anteriormente a 16

        divider = tk.Frame(frame, height=2, bd=1, relief=tk.SUNKEN)
        divider.pack(fill=tk.X, side=tk.BOTTOM, pady=16)
      