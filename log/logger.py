import logging
import colorlog

def configure_logger():
    handler = colorlog.StreamHandler()
    handler.setFormatter(
        colorlog.ColoredFormatter(
            "%(log_color)s%(asctime)s %(levelname)s: %(name)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
            log_colors={
                "DEBUG": "white",
                "INFO": "white",
                "WARNING": "yellow",
                "ERROR": "red",
                "CRITICAL": "red,bg_white"
            }
        )
    )
    
    root_logger = logging.getLogger()

    if not root_logger.handlers:
        root_logger.addHandler(handler)

    root_logger.setLevel(logging.INFO)

