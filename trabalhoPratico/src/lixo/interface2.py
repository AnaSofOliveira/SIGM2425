from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QRadioButton, QButtonGroup, QScrollArea, QGraphicsView, QGraphicsScene, QLineEdit
)
from PyQt5.QtGui import QWheelEvent
from PyQt5.QtCore import Qt
import psycopg2
import sys

class AnimalSelectorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Animal Selector")
        self.setGeometry(100, 100, 800, 600)
        self.setup_ui()

        # Database connection (adjust parameters as needed)
        self.conn = psycopg2.connect(
            dbname="fuga_selvagem", user="postgres", password="postgres", host="localhost", port="5432"
        )
        self.load_static_views()
        self.load_animal_list()

    def setup_ui(self):
        # Main layout
        main_layout = QHBoxLayout(self)

        # Left panel layout
        self.left_panel = QVBoxLayout()

        # Timer input and play button
        self.timer_input = QLineEdit("50")
        self.timer_input.setFixedWidth(50)
        self.play_button = QPushButton(">")
        self.play_button.setFixedSize(30, 30)

        timer_layout = QHBoxLayout()
        timer_layout.addWidget(self.timer_input)
        timer_layout.addWidget(QLabel("minutos"))
        timer_layout.addWidget(self.play_button)

        self.left_panel.addLayout(timer_layout)

        # Animal selection
        self.button_group = QButtonGroup(self)
        self.button_group.setExclusive(True)  # Only one selection at a time

        # Scroll area (optional for large lists)
        scroll_area = QScrollArea()
        scroll_widget = QWidget()
        scroll_widget.setLayout(self.left_panel)
        scroll_area.setWidget(scroll_widget)
        scroll_area.setWidgetResizable(True)
        scroll_area.setFixedWidth(200)

        # Add left panel to main layout
        main_layout.addWidget(scroll_area)

        # Right panel for visualization
        self.graph_view = QGraphicsView()
        self.scene = QGraphicsScene()
        self.graph_view.setScene(self.scene)
        
        # Add zoom controls
        zoom_controls = QHBoxLayout()
        self.zoom_in_button = QPushButton("+")
        self.zoom_out_button = QPushButton("-")
        zoom_controls.addWidget(self.zoom_in_button)
        zoom_controls.addWidget(self.zoom_out_button)
        zoom_controls.addStretch()

        self.zoom_in_button.clicked.connect(self.zoom_in)
        self.zoom_out_button.clicked.connect(self.zoom_out)

        graph_layout = QVBoxLayout()
        graph_layout.addWidget(self.graph_view)
        graph_layout.addLayout(zoom_controls)

        main_layout.addLayout(graph_layout)

        # Enable drag and drop
        self.graph_view.setDragMode(QGraphicsView.ScrollHandDrag)

    def load_static_views(self):
        # Load static views (forests, crops, lakes, swamps)
        queries = {
            "v_florestas": "SELECT * FROM v_florestas;",
            "v_cultivos": "SELECT * FROM v_cultivos;",
            "v_lagos": "SELECT * FROM v_lagos;",
            "v_pantanos": "SELECT * FROM v_pantanos;"
        }

        for name, query in queries.items():
            data = self.execute_query(query)
            self.render_static_view(name, data)

    def load_animal_list(self):
        # Query to load animal names from the database
        query = "SELECT id_objeto_movel, nome FROM objeto_movel;"
        animals = self.execute_query(query)

        for animal in animals:
            animal_id, animal_name = animal
            radio_button = QRadioButton(f"{animal_name} ({animal_id})")
            self.button_group.addButton(radio_button)
            radio_button.toggled.connect(self.update_view)
            self.left_panel.addWidget(radio_button)

    def execute_query(self, query):
        with self.conn.cursor() as cur:
            cur.execute(query)
            return cur.fetchall()

    def render_static_view(self, name, data):
        # Example rendering logic for static views
        for row in data:
            x, y = row[0], row[1]  # Adjust based on your schema
            self.scene.addEllipse(x, y, 5, 5)  # Draw points for each row

    def update_view(self):
        # Update view based on selected animal
        selected_button = self.button_group.checkedButton()
        if selected_button:
            animal_info = selected_button.text()
            animal_id = int(animal_info.split('(')[-1][:-1])  # Extract ID from "Name (ID)"
            query = f"SELECT * FROM v_trajetoria_{animal_id};"
            data = self.execute_query(query)

            # Clear previous trajectories
            self.scene.clear()

            # Reload static views
            self.load_static_views()

            # Render trajectory for selected animal
            for row in data:
                x, y = row[0], row[1]  # Adjust based on your schema
                self.scene.addLine(x, y, x + 1, y + 1)  # Example trajectory rendering

    def zoom_in(self):
        self.graph_view.scale(1.2, 1.2)

    def zoom_out(self):
        self.graph_view.scale(0.8, 0.8)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AnimalSelectorApp()
    window.show()
    sys.exit(app.exec_())
