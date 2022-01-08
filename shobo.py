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

# ##########################################################################
# Here are some possible test queries you can use to check this API:
#   python shobo.py --user_name "trixy culverhouse"  (list of ids for users with name trixy culverhouse)
#   python shobo.py --user_id "51a4101a4165b76eb1fb6a0ac1b7af364796afd88979fe18076f98c1" (User name and history)
#   python shobo.py --user_id "51a4101a4165b76eb1fb6a0ac1b7af364796afd88979fe18076f98c1" --removed --product_name "Fisherprice Baby Mixer" (products removed by this id named "Fisherprice Baby Mixer")
#   python shobo.py --removed --above 300 (all products removed with price above 300)
#   python shobo.py --removed --below 300 (all producst removed with price below 300)
#   python shobo.py --removed --above 300 --below 600 (all producst removed with price above 300 and below 600)
#   python shobo.py --removed (all products removed)
#   python shobo.py --added (all products added)
#   python shobo.py --purchased (all products purchased)
#   python shobo.py --purchased --above 300 --below 600 (all producst purchased with price above 300 and below 600)
# ##########################################################################

# Generic libraries
import sys
import argparse

# Loading shobo libraries
from src.Managers import DataManager


# NOTE: creating a command line arguments parse.
#       To try it out: python generate_users.py --number 100 --output "users.json"
parser = argparse.ArgumentParser(description="Query data from a shopping basket platform.")
parser.add_argument('--user_id', type=str, help="Returns name and history of user when used alone, limits query in conjuction with other keywords.", default=None)
parser.add_argument('--user_name', type=str, help="Returns list of all unique ids with that name when used alone, limits query in conjuction with other keywords (using the first on the list).", default=None)
parser.add_argument('--product_name', type=str, help="Limit the query to all products with that unique name.", default=None)
parser.add_argument('--purchased', help="Limit the query to purchased products.", action='store_true')
parser.add_argument('--added', help="Limit the query to added products.", action='store_true')
parser.add_argument('--removed', help="Limit the query to removed products (opposite).", action='store_true')
parser.add_argument('--above', type=int, help="Limit the query to products with price above the input.", default=None)
parser.add_argument('--below', type=int, help="Limit the query to products with price below the input.", default=None)
args = parser.parse_args()

# NOTE: creating data manager.
dm = DataManager("data/users.json", "data/safe_users.json")

if args.removed:
    args.added = not args.removed

if args.user_id and not any([args.purchased, args.added, args.removed, args.above, args.below]):
    user = dm.userById(args.user_id)
    print("User Name:", user.name())
    print("User History (Product Name, Price, Added/Removed, Purchased, RemovedId):")
    print(user.history())
    sys.exit()
elif args.user_id and any([args.purchased, args.added, args.removed, args.above, args.below]):
    user = dm.userById(args.user_id)
    print("User Name:", user.name())
    print("Query Result:", dm.query(user_id=args.user_id, 
                                    product_name=args.product_name if args.product_name else None,
                                    purchased=args.purchased if args.purchased else False,
                                    added=args.added if args.added else False,
                                    above=args.above if args.above else None,
                                    below=args.below if args.below else None,
                                    ))
    sys.exit()

if args.user_name and not any([args.purchased, args.added, args.removed, args.above, args.below]):
    users = dm.userByName(args.user_name)
    if len(users) == 0:
        print("No such user exists.")
        sys.exit()
    print("User Ids:", [user.id() for user in users])
    sys.exit()
elif args.user_name and any([args.purchased, args.added, args.removed, args.above, args.below]):
    users = dm.userByName(args.user_name)
    if len(users) == 0:
        print("No such user exists.")
        sys.exit()
    print("Query Result:", dm.query(user_id=users[0].id(), 
                                    product_name=args.product_name if args.product_name else None,
                                    purchased=args.purchased if args.purchased else False,
                                    added=args.added if args.added else False,
                                    above=args.above if args.above else None,
                                    below=args.below if args.below else None,
                                    ))
    sys.exit()

print("Query Result:", dm.query(product_name=args.product_name if args.product_name else None,
                                purchased=args.purchased if args.purchased else False,
                                added=args.added if args.added else False,
                                above=args.above if args.above else None,
                                below=args.below if args.below else None,
                                ))
