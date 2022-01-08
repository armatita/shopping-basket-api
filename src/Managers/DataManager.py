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

# Utilities libraries
from src.Utils import SingletonMetaClass

# Local libraries
from .CommonVariables import *
from .UserData import UserData, User
from .HistoryContainer import HistoryContainer


class DataManager(metaclass=SingletonMetaClass):
    """
    The `DataManager` is the class responsible for loading all data from file.
    From it you can make queries with specific keywords. Those being `purchased`,
    `added` (use `False` if you want removed items), `above` and `below` (integers),
    `product_name`, or `user_id`.

    You can obtain directly a User by using the methods `userById` which returns
    an unique user. Or the method `userByName` which returns a list of users (more
    than one can exist with the same name; only the id is unique).

    Note
    ----

    This class was a made a singleton so that it can be added to an external software
    with ease. Once the first instantiation is done, all others will refer to the same
    data.
    """
    _user_data_file: str = None
    _manager_data_file: str = None
    _raw_user_data: Dict[int, Dict[str, Any]] = None
    _users_data: List[UserData] = []

    def __init__(self, user_data_file: str, manager_data_file: str) -> None:
        self._user_data_file = user_data_file
        self._manager_data_file = manager_data_file
        self._load()

    def userById(self, id: str):
        """
        Return an user by its unique ids.
        """
        return self._id(id).user()
    
    def userByName(self, name: str) -> List[User]:
        """
        Return a list of users with the provided name (first and last names in a string).
        """
        users: List[User] = []
        for user_data in self._users_data:
            if user_data.name() == name:
                users.append(user_data.user())
        return users

    def history(self, id: str) -> HistoryContainer:
        """
        Returns the HistoryContainer of a single user.
        """
        return self._id(id).history()

    def query(self, **kwargs) -> Dict[str, int]:
        """
        Returns a dictionary with the query made for the `purchase` and
        `added` flags for all users.
        """
        # print(kwargs)
        added = True
        purchased = False
        above = None
        below = None
        user_id = None
        product_name = None
        if PURCHASED in kwargs.keys():
            purchased = kwargs[PURCHASED]
        if ADDED in kwargs.keys():
            added = kwargs[ADDED] if not purchased else purchased
        if ABOVE in kwargs.keys():
            above = kwargs[ABOVE]
        if BELOW in kwargs.keys():
            below = kwargs[BELOW]
        if USERID in kwargs.keys():
            user_id = str(kwargs[USERID])
        if PRODUCTNAME in kwargs.keys():
            product_name = kwargs[PRODUCTNAME]
        return self._query(purchased=purchased, added=added, above=above, below=below, user_id=user_id, product_name=product_name)

    def _query(self, purchased: bool, added: bool, above: int, below: int, user_id: str, product_name: str) -> Dict[str, int]:
        """
        Returns a dictionary with the query made for the `purchase` and
        `added` flags for all users.
        """
        dictionary: Dict[str, int] = {}
        for user_data in self._users_data:
            if user_id and user_data.id() != user_id:
                continue
            query_data = user_data.query(purchased=purchased, added=added, above=above, below=below, product_name=product_name)
            for key in query_data.keys():
                if key in dictionary.keys():
                    dictionary[key] = dictionary[key] + query_data[key]
                else:
                    dictionary[key] = query_data[key]
        return dictionary
                

    def dictionary(self) -> Dict[str, Any]:
        """
        Converts all the information on this class into something that
        can be written into a json file.
        """
        data_dictionary: Dict[str, Any] = {}
        for user_data in self._users_data:
            data_dictionary[user_data.id()] = user_data.dictionary()
        return data_dictionary

    def _id(self, id: str) -> UserData:
        """
        Return the UserData respective of the provided id.
        """
        for user_data in self._users_data:
            if user_data.id() == id:
                return user_data

    def _load(self) -> None:
        """
        Loads json data into a convenient container.

        Note
        ----

        I'm creating an abstraction for the information on the json
        file so that:
         - The code is more readable and maintanable.
         - Loading and saving to json files is an expensive operation.
           With this abstraction a refactor only needs to modify the 
           `_save` and `_load` methods and the rest will remain functional.
        """
        with open(self._user_data_file, "r") as fid:
            self._raw_user_data = json.loads(fid.read())
        self._users_data.clear()
        for key, value in self._raw_user_data.items():
            self._users_data.append(UserData(self, id=key, first_name=value[FIRST_NAME], last_name=value[LAST_NAME], history=value[HISTORY]))
        # NOTE: we need to make sure this information is set on a safe file
        #       otherwise we could be overriding the original input data.
        #       (For this task, however, notice that we will not introduce
        #        new user data, so the _save option will never be called).
        # self._save()
        
    def _save(self) -> None:
        """
        Saves the current manager data into a safe file.

        Note
        ----

        I'm creating an abstraction for the information on the json
        file so that:
         - The code is more readable and maintanable.
         - Loading and saving to json files is an expensive operation.
           With this abstraction a refactor only needs to modify the 
           `_save` and `_load` methods and the rest will remain functional.
        """
        data_dictionary = self.dictionary()
        with open(self._manager_data_file, "w") as fid:
            dump = json.dumps(data_dictionary, indent=4)
            fid.write(dump)

    def __str__(self):
        """
        Overloading the `__str__` so that any `print` instruction on this
        class will return the json string of all information on class. The
        same for `str` conversions.
        """
        return json.dumps(self.dictionary(), indent=4)
