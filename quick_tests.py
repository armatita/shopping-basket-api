# NOTE: loading the data manager (main source for queries).
from src.Managers import DataManager


# NOTE: doing some arbitary sanity checks.
print("1. Loading the data manager.")
dm = DataManager("data/users.json", "data/safe_users.json")
print("2. Check the number for each of the purchased items.")
print("  ", dm.query(purchased=True))
print("3. Check for the numner of each of the purchased items with product name: Reloop Headphone.")
print("  ", dm.query(purchased=True, product_name='Reloop Headphone'))
print("4. Check the number for each of the purchased items with a price above 600.")
print("  ", dm.query(purchased=True, above=600))
print("5. Check the number for each of the added items.")
print("  ", dm.query(added=True))
print("6. Check the number for each of the added items with a price below 600 but above 300.")
print("  ", dm.query(added=True, below=600, above=300))
print("7. Check the number for each of the added items with price above 600.")
print("  ", dm.query(added=False, above=600))
print("8. Check the number for each of the added items with product name blabla (does not exit).")
print("  ", dm.query(added=True, product_name="blabla"))
print("9. Access directly the user by name: trixy culverhouse.")
user = dm.userByName("trixy culverhouse")[0]
print("   - User Id is:", user)
print("10. Query list of purchased items by trixy culverhouse using the data manager.")
print("  ", dm.query(purchased=True, user_id=user))
print("11. Query list of purchased items by trixy culverhouse using the User API.")
print("  ", user.query(purchased=True))