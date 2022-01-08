# Shoba API

Minimal API for a **sho**pping **ba**sket platform API with data analysis.

# How to use

Shoba has a command line interface with the following instruction (you can
access this information with `python shobo.py -h`):

 - `user_id` : expected to be a 256 characters unique Id string to an user.
 - `user_name` : expected to be a complete name string (first and last) for a user.
 - `product_name` : expected to be a product name string.
 - `purchased` : if present the search is limited to purchased products (this takes priority if conflicting).
 - `added` : if added the search is limited to added products.
 - `removed` : if added the search is limited to removed products.
 - `above` : if added the search is limited to products with price above input integer.
 - `below` : if added the search is limited to products with price below input integer.

Here is an example of some of the queries you can make:

```
# NOTE: get list of ids for all users named "trixy culverhouse"
python shobo.py --user_name "trixy culverhouse"

# NOTE: get user name and history
python shobo.py --user_id "51a4101a4165b76eb1fb6a0ac1b7af364796afd88979fe18076f98c1"

# NOTE: get products removed by this id named "Fisherprice Baby Mixer"
python shobo.py --user_id "51a4101a4165b76eb1fb6a0ac1b7af364796afd88979fe18076f98c1" --removed --product_name "Fisherprice Baby Mixer"

# NOTE: get all products removed with price above 300
python shobo.py --removed --above 300

# NOTE: get all producst removed with price below 300
python shobo.py --removed --below 300

# NOTE: get all producst removed with price above 300 and below 600
python shobo.py --removed --above 300 --below 600

# NOTE: get all products removed
python shobo.py --removed

# NOTE: get all products added
python shobo.py --added

# NOTE: get all products purchased
python shobo.py --purchased

# NOTE: get all producst purchased with price above 300 and below 600
python shobo.py --purchased --above 300 --below 600
```

# Generating synthetic data

This repository comes with a script to produce synthetic user data and
perform light analysis on it. To use it run the `python generate_python.py`
file inside the `data` folder.

You should obtain new information inside the `data\users.json` file along
with a report with a light numerical analysis over the data produced. For
example:

```
1. Creating User Data and saving it to file.
2. Retrieving some statistics.
3. Printing statistics:
    - Number of Items Purchased: 58 ( 4 % of added) ( 4 % of all)
    - Most Purchased Item:       Reloop Headphone
    - Most Added Item:           Pioneer DJ Mixer
    - Most Removed Item:         Fisherprice Baby Mixer

    - Number of purchases per item: {
    "Reloop Headphone": 14,
    "Pioneer DJ Mixer": 13,
    "Roland Wave Sampler": 12,
    "Fisherprice Baby Mixer": 9,
    "Rokit Monitor": 10
}
    - Number of additions per item: {
    "Reloop Headphone": 227,
    "Roland Wave Sampler": 249,
    "Pioneer DJ Mixer": 252,
    "Fisherprice Baby Mixer": 231,
    "Rokit Monitor": 223
}
    - Number of removals per item: {
    "Reloop Headphone": 47,
    "Fisherprice Baby Mixer": 49,
    "Roland Wave Sampler": 40,
    "Rokit Monitor": 47,
    "Pioneer DJ Mixer": 30
}
Synthetic User Data generation COMPLETE!
```

Also notice that the script is prepared to deal with variables provided from
the command line. Run `python generate_users.py -h` to see all the option.


# Architecture and Technical Details

The user data being produced for this task is of the type:

```
{
    "51a4101a4165b76eb1fb6a0ac1b7af364796afd88979fe18076f98c1": {
        "first_name": "trixy",
        "last_name": "culverhouse",
        "history": {
            "997159759937862a85f386f14feee1fc8421c6e906125ae374a6e8c3": [
                "Reloop Headphone", <--- Product Name
                159,                <--- Product Price
                true,               <--- Added (True) or Removed (False) operation
                true,               <--- Purchased (True) or not
                null                <--- If removed which Id was removed (str)
            ],
            "6596433be9ff1800bf385bb9bcbdaeeed30d765602a824989990fcb4": [
                "Reloop Headphone",
                159,
                true,
                false,
                null
            ],
        ...
```

Each user will have an unique Id produced from a SHA256 algorithm (based on name
and counter). Similarly the same can be said for each `added`, or `removed` operation.

The history per user is being stored as opposed to actually adding and removing items.
This was done so that time dependent queries could be added (although they do not exits
in the version made for this assignment).

Furthermore there is an abstraction that the `DataManager` does over the original json
data. This was done to facilitate maintenance, readability, but also to make sure that
if the storage system (reading and writing json files per operation is expensive) is
refactored only the `_save` and `_load` function need to be replaced.

The architecture is quite simple and can be described as such:

```
shobo.py (public CLI API)
   |_
      DataManager (loads and saves to json file; stores instances of UserData)
           |_
              UserData (stores user name, id, and history)
                |  |_
                |     HistoryContainer (stores all user operations)
                |           |_
               _|              Operation (specifies an operation characteristics)
User (public class with User information and direct queries referring to it)
```

To see the public classes `DataManager` and `User` in action refer to the file `quick_tests.py`.

At the lack of proper UI a command line interface was added to this API. Queries can
be made with simple keyword (check section above).


# Technical assignment (Description)

You’re working on an online shopping platform. The sales team wants to know 
which items were added to a basket, but removed before checkout. We will use 
this data later for targeted discounts.

Using ~~PHP~~ (Python), build a shopping basket that helps you get this data.

**Minimal requirements**

* Use ~~PHP~~ (Python will be used as requested by recruiter)

**Scope**

* Focus on API side, not on the interface