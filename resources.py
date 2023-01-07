import sys
import os


def get_resource(file_path : str):
    try:
        return sys._MEIPASS + os.sep + file_path
    except AttributeError:
        return app_dir() + file_path

def app_dir():
    if sys.argv[0][0] == os.sep:
        return os.path.dirname(sys.argv[0]) + os.sep
    else:
        return os.path.dirname(os.getcwd() + os.sep + sys.argv[0]) + os.sep