#! /files/Programming/Projects/renpy-lsp-server/venv/bin/python
import sys
import argparse
import warnings
from loguru import logger
from renpylsp import RenpyLanguageServer

def define_arguments(parser: argparse.ArgumentParser):
    parser.description = "Renpty Language Server"
    parser.add_argument('--port', type=int, default=3000,
                        help="The port to which the LSP binds")


def _setup_logger():
    warnings.filterwarnings("ignore")
    event_logger_format: str = "<g>{time:YYYY-MM-DD HH:mm:ss}</g> <c>{name}</c> <magenta>>></magenta> <lvl>{message}</lvl>"
    logger.remove()
    logger.add(sink='logs/app.log', mode='w+', level="DEBUG",
               format=event_logger_format, diagnose=False)
    # logger.add(sink=sys.stdout, colorize=True, level="DEBUG",
    #            format=event_logger_format, diagnose=False)
    #


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    define_arguments(parser)
    args = parser.parse_args()
    _setup_logger()

    logger.info("Starting up!")
    server = RenpyLanguageServer()
    server.start()
    logger.info("Finished starting up!")
