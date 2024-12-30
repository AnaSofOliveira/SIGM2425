from typing import Final
import os

DATABASE_CONFIG_PATH: Final = os.path.join(os.path.dirname(__file__), 'database.json')

APP_NAME: Final = 'Fuga Selvagem - Trajetórias e Cinemáticas'
# ICON_PATH: Final = r"C:\Users\A40610\Desktop\SIGM2425\trabalhoPratico\src\interface\imgs\postgres.ico"
ICON_PATH: Final = r"C:\Users\ana.sofia.oliveira\Documents\ISEL\SIGM2425\trabalhoPratico\imgs\postgres.ico"

TEXT_SIZE: Final = 20
FONT_FAMILY: Final = 'Arial'

TEXT_MAIN_LABEL: Final = 'Selecione o Animal'
TEXT_UPDATE_BUTTON: Final = 'Atualizar'
TEXT_INTERATIONS_LABEL: Final = 'Número de Iterações'