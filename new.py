import os
import json
import requests

def extract_dependencies(directory):
    dependencies = {}

    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('package-lock.json'):
                lock_file_path = os.path.join(root, file)
                with open(lock_file_path, 'r') as lock_file:
                    lock_data = json.load(lock_file)

                if 'dependencies' in lock_data:
                    for name, package in lock_data['dependencies'].items():
                        print(package['version'], name)
                        version = package['version']
                        dependencies.setdefault(name, {})
                        dependencies[name]['version'] = version
    return dependencies

def get_package_info(package):
        try:
            url = f"https://registry.npmjs.org/{package}"
            response = requests.get(url)

            if response.status_code == 200:
                data = response.json()
                # print("Version : ", data["dist-tags"]
                #       ["latest"], " Name :", data["name"])
                latest_version = data["dist-tags"]["latest"]
                package_name = data["name"]

                return package_name, latest_version
            else:
                print(
                    f"Error retrieving package info for {package}: {response.text}")
        except requests.exceptions.RequestException as e:
            print(f"Error retrieving package info for {package}: {e}")

        return None, None


# Example usage
directory_path = './'
dependencies = extract_dependencies(directory_path)
# print(dependencies)
for i in dependencies:
    get_package_info(i)
    # get_latest_version(i)
