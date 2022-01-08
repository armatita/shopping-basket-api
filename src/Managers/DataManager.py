"""
MIT License

Copyright (c) 2022 Pedro Correia

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""


# Generic libraries
from typing import Dict, Any
import json

# Utilities libraries
from src.Utils import SingletonMetaClass


class User:
    _id: str = None
    _items: Dict[str, int] = None
    def __init__(self, id: str) -> None:
        self._id = id
        self._items = {}

    def addItem(self, item: str) -> int:
        if item in self._items.keys():
            self._items[item] += 1
            return self._items[item]
        self._items[item] = 1
        return 1

    def removeItem(self, item: str) -> int:
        return self._items.pop(item, 0)

    def checkout(self) -> float:
        pass

        


class DataManager(metaclass=SingletonMetaClass):
    _user_data_file: str = None
    _user_data: Dict[int, Dict[str, Any]] = None
    def __init__(self, user_data_file: str) -> None:
        self._user_data_file = user_data_file
        self._loadUserData()

    def _loadUserData(self):
        with open(self._user_data_file, "r") as fid:
            self._user_data = json.loads(fid.read())

    def __str__(self):
        return """<Some Data>"""