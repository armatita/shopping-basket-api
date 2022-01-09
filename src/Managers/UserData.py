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
from typing import Dict, Tuple, List, Any
import json

# Local libraries
from .CommonVariables import *
from .HistoryContainer import HistoryContainer


class User:
    """
    `User` is a public class from which you can make direct queries to the
    respective user. It can be obtained from the `DataManager`.
    """
    _id: str = None
    _first_name: str = None
    _last_name: str = None
    def __init__(self, parent, id: str, first_name: str, last_name: str) -> None:
        self._data_manager = parent
        self._id = id
        self._first_name = first_name
        self._last_name = last_name

    def id(self) -> str:
        """
        Return unique id for this user.
        """
        return self._id

    def name(self) -> str:
        """
        Returns the name of this user.
        """
        return self.firstName() + " " + self.lastName()

    def firstName(self) -> str:
        """
        Get User first name.
        """
        return self._first_name

    def lastName(self) -> str:
        """
        Get User last name.
        """
        return self._last_name

    def query(self, **kwargs) -> Dict[str, int]:
        """
        Returns a dictionary with the query made for the `purchase` and
        `added` flags for all users.
        """
        return self._data_manager.query(**kwargs, user_id=self.id())

    def history(self) -> HistoryContainer:
        """
        Return history for this user.
        """
        return json.dumps(self._data_manager.history(self._id).dictionary(), indent=4)

    def __str__(self) -> str:
        """
        The string version of this class always return the unique id.
        """
        return self.id()

    
class UserData:
    """
    `UserData` is a container of user information, including its history.
    """
    _id: str = None
    _first_name: str = None
    _last_name: str = None
    _history: HistoryContainer = None
    def __init__(self, parent, id: str, first_name: str, last_name: str, history: Dict[str, Tuple[str, str, bool, bool, str]]) -> None:
        self._data_manager = parent
        self._id = id
        self._first_name = first_name
        self._last_name = last_name
        self._history = HistoryContainer(history)

    def id(self) -> str:
        """
        Returns the id for this user.
        """
        return self._id

    def name(self) -> str:
        """
        Returns the name of this user.
        """
        return self.firstName() + " " + self.lastName()

    def firstName(self) -> str:
        """
        Get User first name.
        """
        return self._first_name

    def lastName(self) -> str:
        """
        Get User last name.
        """
        return self._last_name

    def dictionary(self) -> Dict[str, Any]:
        """
        Returns the information on this class in a form compatible
        with writing to a json file.
        """
        local_dictionary: Dict[str, Any] = {}
        local_dictionary[FIRST_NAME] = self._first_name
        local_dictionary[LAST_NAME] = self._last_name
        local_dictionary[HISTORY] = self._history.dictionary()
        return local_dictionary

    def history(self) -> HistoryContainer:
        """
        Return the HistoryContainer for this UserData.
        """
        return self._history

    def query(self, purchased: bool, added: bool, above:int, below:int, product_name: str) -> Dict[str, int]:
        """
        Returns a dictionary with the query made for the `purchase` and
        `added` flags for this user.
        """
        return self._history.query(purchased=purchased, added=added, above=above, below=below, product_name=product_name)

    def user(self) -> User:
        return User(self._data_manager, self.id(), self.firstName(), self.lastName())


    def __iter__(self):
        """
        Iterating over this object returns the operations.
        """
        for value in self._history:
            yield value


