from logging.config import dictConfig
import logging
import os

log_path = "log/"

if not os.path.exists(log_path):
   os.makedirs(log_path)

dictConfig({
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "default": {
            "format": "[%(asctime)s] %(levelname)-4s %(funcName)s() L%(lineno)-4d %(message)s",
        },
        "detailed": {
            "format": "[%(asctime)s] %(levelname)-4s %(funcName)s() L%(lineno)-4d %(message)s - call_trace=%(pathname)s L%(lineno)-4d",
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
            "stream": "ext://sys.stdout",
        },
        "error_file": {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "detailed",
            "filename": "log/gunicorn.error.log",
            "maxBytes": 10000,
            "backupCount": 10,
            "delay": "True",
        },
        "detailed_file": {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "detailed",
            "filename": "log/gunicorn.detailed.log",
            "maxBytes": 10000,
            "backupCount": 10,
            "delay": "True",
        }
    },
    "loggers": {
        "gunicorn.error": {
            "handlers": ["console", "error_file"], 
            "level": "INFO",
            "propagate": False,
        }
    },
    "root": {
        "handlers": ["console", "detailed_file"],
        "level": "INFO",
    }
})


logger = logging.getLogger(__name__)
