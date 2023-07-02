import json
import os
import npm as npm

file_path = os.path.join("data", "node", "names.json")
# download_npm_data = 

def get_metadata():
    # Read the JSON file containing package names
    with open(file_path, "r") as file:
        package_data = json.load(file)
        print(type(package_data) , len(package_data))
        for name in package_data:
            npm.download_package_metadata(name)


get_metadata()
