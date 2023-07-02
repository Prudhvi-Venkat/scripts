import os
import re
import json

# Take user inputs
vendor = input("Enter the vendor name: ")
product = input("Enter the product name: ")

# Sanitize vendor and product names
sanitized_vendor = re.sub(r'[\\/:*?"<>|]', "_", vendor)
sanitized_product = re.sub(r'[\\/:*?"<>|]', "_", product)

# Construct folder paths
root_dir = "reports/"
product_name = f"{sanitized_product}.json"
vendor_folder = os.path.join(root_dir, sanitized_vendor)
# product_folder = os.path.join(vendor_folder, sanitized_product)
json_file_path = os.path.join(vendor_folder, product_name)

# Read the JSON file
try:
    with open(json_file_path) as json_file:
        data = json.load(json_file)
        # Process the JSON data as needed
        print(data)
        # ...
except FileNotFoundError:
    print(f"JSON file not found: {json_file_path}")
