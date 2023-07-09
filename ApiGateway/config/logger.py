import logging
import colorlog


file_handler = logging.FileHandler("app.log")  # Nombre del archivo de registro
file_handler.setLevel(logging.WARNING )  # Nivel de registro para escribir en el archivo
file_formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s", "%Y-%m-%d %H:%M:%S")  # Formato del registro en el archivo
file_handler.setFormatter(file_formatter)

formatter = colorlog.ColoredFormatter(
    "%(log_color)s%(levelname)-8s%(reset)s %(message)s",
    log_colors={
        "DEBUG": "cyan",
        "INFO": "green",
        "WARNING": "yellow",
        "ERROR": "red",
        "CRITICAL": "red,bg_white"
    },
    secondary_log_colors={},
    style="%"
)
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger = logging.getLogger()
logger.addHandler(handler)
logger.addHandler(file_handler)