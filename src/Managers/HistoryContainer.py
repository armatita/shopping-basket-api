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


class Operation:
    Id: str = None
    Name: str = None
    Price: float = None
    Added: bool = None
    Purchased: bool = None
    RemovedId: str = None
    def __init__(self, id: str, name: str, price: float, added: bool, purchased: bool, removed_id: str = None) -> None:
        self.Id = id
        self.Name = name
        self.Price = price
        self.Added = added
        self.Purchased = purchased
        self.RemovedId = removed_id


class HistoryContainer:
    _history: List[Operation] = None
    def __init__(self, history: Dict[str, Tuple[str, float, bool, bool, str]]) -> None:
        self._buildHistoryFromDictionary(history)

    def dictionary(self) -> Dict[str, Tuple[str, str, float, bool, bool, str]]:
        """
        Returns the information on this class in a form compatible
        with writing to a json file.
        """
        dictionary: Dict[str, Tuple[str, float, bool, bool, str]] = {}
        for operation in self._history:
            dictionary[operation.Id] = (operation.Name, operation.Price, operation.Added, operation.Purchased, operation.RemovedId)
        return dictionary

    def query(self, purchased: bool, added: bool, above: int, below: int, product_name: str) -> Dict[str, int]:
        """
        Returns a dictionary with the query made for the `purchase` and
        `added` flags.
        """
        dictionary: Dict[str, int] = {}
        for operation in self._history:
            if operation.Added == added and operation.Purchased == purchased:
                if product_name and operation.Name != product_name:
                    continue
                if above and operation.Price < above:
                    continue
                if below and operation.Price > below:
                    continue
                if operation.Name in dictionary.keys():
                    dictionary[operation.Name] = dictionary[operation.Name] + 1
                else:
                    dictionary[operation.Name] = 1
        return dictionary

    def _buildHistoryFromDictionary(self, history: Dict[str, Tuple[str, float, bool, bool, str]]) -> None:
        """
        Generic parser to easilly convert between a dictionary (coming from a json file)
        and an easier to read structure. This method loads all operations into the `_history`
        variable.
        """
        self._history = []
        for key in history:
            id = key
            name = history[key][0]
            price = history[key][1]
            added = history[key][2]
            purchased = history[key][3]
            removed_id = None
            if len(history[key]) > 4:
                removed_id = history[key][4]
            self._history.append(Operation(id, name, price, added, purchased, removed_id))

    def __iter__(self):
        """
        Iterating over this object returns the operations.
        """
        for value in self._history:
            yield value