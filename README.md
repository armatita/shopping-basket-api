# Shoba API

Minimal API for a **sho**pping **ba**sket platform API with data analysis.

# How to use


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

# Technical assignment (Description)

You’re working on an online shopping platform. The sales team wants to know 
which items were added to a basket, but removed before checkout. We will use 
this data later for targeted discounts.

Using ~~PHP~~ (Python), build a shopping basket that helps you get this data.

**Minimal requirements**

* Use ~~PHP~~ (Python will be used as requested by recruiter)

**Scope**

* Focus on API side, not on the interface