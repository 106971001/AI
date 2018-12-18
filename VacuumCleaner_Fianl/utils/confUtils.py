import json
from os import path
import logging

CONF = None
LOG = None


def init_config():
    """
    Loads the configuration from conf/config.json
    :return: None
    """
    global CONF
    file_path = path.dirname(__file__)
    file_path = path.join(file_path, "..", "conf", "config.json")
    with open(file_path) as f:
        CONF = json.load(f)


def get_logger(name):
    """

    :param name: The name of the logger
    :return: The log
    """
    logging.basicConfig(level=logging.ERROR)
    log = logging.getLogger(name)
    return log


def set_verbose(log):
    """
    set to level Info
    :param log:
    :return: None
    """
    log.setLevel(logging.INFO)


init_config()
LOG = get_logger("VacuumSimulator")
if CONF["logging"]["verbose"]:
    set_verbose(LOG)
