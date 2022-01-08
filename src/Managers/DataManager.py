"""

"""

# Generic libraries
import json

# Utilities libraries
from src.Utils import SingletonMetaClass


class DataManager():
    def __init__(self) -> None:
        print("Created instance of DataManager.")

    def __str__(self):
        return """<Some Data>"""