import json
import requests
import os

# Create the 'data' folder if it doesn't exist
data_folder = 'data'
if not os.path.exists(data_folder):
    os.makedirs(data_folder)

# Create the 'node' folder inside the 'data' folder if it doesn't exist
node_folder = os.path.join(data_folder, 'node')
if not os.path.exists(node_folder):
    os.makedirs(node_folder)


def download_package_metadata(package):
    url = f"https://registry.npmjs.org/{package}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        filename = os.path.join(node_folder, f'{package}.json')
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)
        print(f"Package {package} metadata downloaded and saved successfully.")
        return True
    else:
        print(f"Error downloading package metadata: {response.text}")


def load_package_details(package_name):
    try:
        with open(f"{package_name}.json", "r") as f:
            data = json.load(f)
            if package_name in data:
                package_info = data[package_name]
                print(f"Package: {package_name}")
                print(f"Latest Version: {package_info['dist-tags']['latest']}")
                print(f"Dependencies:")
                for dependency, version in package_info.get("dependencies", {}).items():
                    print(f"{dependency}: {version}")
            else:
                print(f"Package '{package_name}' not found in metadata.")
    except FileNotFoundError:
        print(
            "Package metadata file not found. Please download the metadata first using 'download_package_metadata'."
        )


# Version History
def get_version_history(package_name):
    file_path = os.path.join(node_folder, f'{package_name}.json')
    try:
        with open(file_path, "r") as file:
            file_data = json.load(file)
            versions_list = file_data.get("versions")
            version_history = file_data.get("time")
            if version_history:
                for key, val in version_history.items():
                    print("Version : ", key, "Release Date : ", val)
            # if versions_list:
            #     for version_num in versions_list:
            #         print(version_num)
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except json.JSONDecodeError:
        print(f"Invalid JSON format: {file_path}")


# Load and print details of a specific package
# package_name = input("Enter the package name: ")
# Download package metadata
# if download_package_metadata(package_name) == True:
#     get_version_history(package_name)
