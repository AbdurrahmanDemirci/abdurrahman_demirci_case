import logging
import sys

try:
    import colorlog
    _HAS_COLOR = True
except ImportError:
    _HAS_COLOR = False

# When running under pytest, log_cli handles output — no custom handler needed
_UNDER_PYTEST = "pytest" in sys.modules


def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)

    # Guard against duplicate handlers if called multiple times with the same name
    if logger.handlers:
        return logger

    logger.setLevel(logging.DEBUG)

    if _UNDER_PYTEST:
        # pytest log_cli manages output — just propagate, do not add a custom handler
        logger.propagate = True
    else:
        # Standalone script — attach colorlog handler
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.INFO)

        if _HAS_COLOR:
            formatter = colorlog.ColoredFormatter(
                fmt="%(log_color)s%(asctime)s [%(levelname)-8s]%(reset)s %(name)s: %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
                log_colors={
                    "DEBUG":    "cyan",
                    "INFO":     "green",
                    "WARNING":  "yellow",
                    "ERROR":    "red",
                    "CRITICAL": "bold_red",
                },
            )
        else:
            formatter = logging.Formatter(
                fmt="%(asctime)s [%(levelname)-8s] %(name)s: %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
            )

        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.propagate = False

    return logger
