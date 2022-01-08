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

#################################################################################
# You can run this file out of the box to generate sysnthetic user data and
# retrieve information from it. This includes things like: Most sold item, 
# Number of items that were added to the basket (including purchases), Number of
# items that were removed, Most removed item, etc. However, this is NOT an API.
# It's meant to generate data for testing the proper API.
#################################################################################

# Generic libraries
from typing import Dict, List, Tuple, Any
import argparse
import hashlib
import random
import json
import os


# NOTE: creating a command line arguments parse.
#       To try it out: python generate_users.py --number 100 --output "users.json"
parser = argparse.ArgumentParser(description="Generate user data for an shopping platform.")
parser.add_argument('--number', help="Number of users to be generated.", default=100)
parser.add_argument('--output', help="File to which the data will be dumped (json).", default="users.json")
parser.add_argument('--products', help="Json file with list of possible producsts.", default="products.json")
parser.add_argument('--purchase_probability', help="The probability of an item being purchased.", default=0.05)
parser.add_argument('--adding_probability', help="The probability of an item being added.", default=0.75)
args = parser.parse_args()


# NOTE: creating some utility functions.
def hashstring(s: str) ->str:
    """
    Generating an "unique" user id from the sha224 algorithm.
    """
    return hashlib.sha224(s.encode('ascii')).hexdigest()

def isascii(s: str):
    """
    Check if the characters in string s are in ASCII, U+0-U+7F.
    
    Note
    ----

    Retrieved from here: https://stackoverflow.com/a/18403812/2868335
    """
    return len(s) == len(s.encode())

def get_names(path: str) -> List[str]:
    """
    Obtaining list of names from file that follow the ascii encoding.

    Note
    ----

    * Any problematic characters will be replaced.
    """
    names: List[str] = []
    with open(path, "r", errors='replace') as fid:
        full_file = fid.readlines()
        for name in full_file:
            if isascii(name):
                names.append(name.replace("\n",""))
    return names

def random_name(first_names: List[str], last_names: List[str]) -> str:
    """
    Generate a random name of the form <first name> <last name> given the
    input lists.
    """
    return random.choice(first_names) + " " + random.choice(last_names)


def random_user_data(name: str, products: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Generating some random history for a user with added items, removed items,
    and purchased items.

    Note
    ----

    The verbosity of the history container among other is conditioned by the
    fact that we will need to save this to file. Alternatively something
    like `NameTuple`or a proper class would be used.
    """

    def add_product(products: List[Dict[str, Any]], history:Dict[str, Tuple[str, int, bool, bool]]) -> None:
        product = random.choice(products)
        purchase_id = random.randint(0, 999999)
        # NOTE: (Name, Price, Added/Removed, Purchased/Not)
        value = (product['name'], product['price'], True, False)
        history[hashstring(product['name']+str(purchase_id))] = value

    def remove_product(history: Dict[str, Tuple[str, int, bool, bool]]) -> None:
        keys = [id for id in history.keys() if not history[id][3]]
        chosen_key = random.choice(keys)
        random_id = random.randint(10000, 999999)
        # NOTE: (Name, Price, Added/Removed, Purchased/Not, removed id)
        history[hashstring(history[chosen_key][0] + str(random_id))] = (history[chosen_key][0], history[chosen_key][1], False, False, chosen_key)

    def purchase_product(history: Dict[str, Tuple[str, int, bool, bool]]) -> None:
        keys = [id for id in history.keys() if not history[id][3] and history[id][2]]
        chosen_key = random.choice(keys)
        history[chosen_key] = (history[chosen_key][0], history[chosen_key][1], history[chosen_key][2], True)

    def available_products_for_purchase(history: Dict[str, Tuple[str, int, bool, bool]]) -> None:
        return len([id for id in history.keys() if not history[id][3] and history[id][2]])

    data = {"name": name, "first_name": name.split(" ")[0], "last_name": name.split(" ")[1]}

    number_of_logs: int = random.randint(5, 25)
    history: Dict[str, Tuple[str, int, bool, bool, int]] = {} # As in {id: (Name, Price, Added/Removed, Purchased/Not, removed_id (optional))}
    for _ in range(number_of_logs):
        if available_products_for_purchase(history) < 3:
            add_product(products, history)
        else:
            random_probability_value = random.uniform(0, 1)
            if random_probability_value < args.purchase_probability:
                purchase_product(history)
            elif args.purchase_probability < random_probability_value < args.purchase_probability + args.adding_probability:
                add_product(products, history)
            elif random_probability_value > args.purchase_probability + args.adding_probability:
                remove_product(history)
    data['history'] = history
    return data

def creating_and_saving_user_data() -> Dict[str, Dict[str, Any]]:    
    # NOTE: loading some list of names retrieved from:
    #       https://github.com/philipperemy/name-dataset 
    #       (it was an arbitrary choice for convenience)
    first_names = get_names("first_names.all.txt")
    last_names = get_names("last_names.all.txt")

    # NOTE: loading the list of products provided for the task.
    with open(args.products, "r") as fid:
        products: List[Dict[str, Any]] = json.loads(fid.read())

    # NOTE: generating users.
    users: Dict[str, Dict[str, Any]] = {}
    for user_number in range(args.number):
        name: str = random_name(first_names, last_names)
        code: str = name + str(user_number)

        # NOTE: creating an "unique" id for a user (they might have the same name).
        id: str = hashstring(code)

        # NOTE: generating some random user data.
        user_data: Dict[str, Any] = random_user_data(name, products)
        users[id] = user_data

    # NOTE: saving users data to file.
    with open(args.output, "w") as fid:
        dump = json.dumps(users, indent=4)
        fid.write(dump)

    return users

# NOTE: creating some numerical analysis functions for quick checks over
#       synthetic data stability.
def get_number_of_items_purchased(user_data: Dict[str, Dict[str, Any]]) -> Tuple[int, int, int]:
    """
    Returns the number of items purchased.
    """
    total = 0
    added = 0
    all_ops = 0
    for value in user_data.values():
        for item in value['history'].values():
            # NOTE: (Name, Price, Added/Removed, Purchased/Not, removed id)
            if item[2]:
                added += 1
            if item[3]:
                total += 1
            all_ops += 1
    return total, added, all_ops

def get_most_N_item(user_data: Dict[str, Dict[str, Any]], index: int, comparison: bool = True) -> Tuple[str, Dict[str, int]]:
    """
    Return the most item of the boolean indexes.

    Note
    ----

    (Name, Price, Added/Removed, Purchased/Not, removed id), so 2 or 3
    """
    items = {}
    for value in user_data.values():
        for item in value['history'].values():
            if item[index] == comparison:
                if item[0] in items.keys():
                    items[item[0]] = items[item[0]] + 1
                else:
                    items[item[0]] = 1
    
    most_item = None
    biggest_counter = 0
    for key in items.keys():
        if items[key] > biggest_counter:
            biggest_counter = items[key]
            most_item = key
    
    return most_item, items

def get_most_purchased_item(user_data: Dict[str, Dict[str, Any]]) -> Tuple[str, Dict[str, int]]:
    """
    Returns the name of the most purchased item.
    """
    return get_most_N_item(user_data, 3)

def get_most_added_item(user_data: Dict[str, Dict[str, Any]]) -> Tuple[str, Dict[str, int]]:
    """
    Returns the name of the most added item.
    """
    return get_most_N_item(user_data, 2)

def get_most_removed_item(user_data: Dict[str, Dict[str, Any]]) -> Tuple[str, Dict[str, int]]:
    """
    Returns the name of the most added item.
    """
    return get_most_N_item(user_data, 2, comparison=False)


# NOTE: running script functions
print("1. Creating User Data and saving it to file.")
user_data = creating_and_saving_user_data()
print("2. Retrieving some statistics.")
number_of_items_purchased, number_of_items_added, number_of_operations = get_number_of_items_purchased(user_data)
most_purchased_item, purchased_items = get_most_purchased_item(user_data)
most_added_item, added_items = get_most_added_item(user_data)
most_removed_item, removed_items = get_most_removed_item(user_data)
print("3. Printing statistics:")
print("    - Number of Items Purchased:", number_of_items_purchased, "(", int((number_of_items_purchased/number_of_items_added)*100),"% of added)",  "(", int((number_of_items_purchased/number_of_operations)*100),"% of all)")
print("    - Most Purchased Item:      ", most_purchased_item)
print("    - Most Added Item:          ", most_added_item)
print("    - Most Removed Item:        ", most_removed_item)
print("")
print("    - Number of purchases per item:", json.dumps(purchased_items, indent=4))
print("    - Number of additions per item:", json.dumps(added_items, indent=4))
print("    - Number of removals per item:", json.dumps(removed_items, indent=4))

print("Synthetic User Data generation COMPLETE!")
