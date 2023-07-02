import requests
import xml.etree.ElementTree as ET
import zipfile
import json
import os

# URL to download the CPE dictionary in XML format
url = "https://nvd.nist.gov/feeds/xml/cpe/dictionary/official-cpe-dictionary_v2.3.xml.zip"

# Send a GET request to download the ZIP file
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    print("Function called")
    # Save the ZIP file
    with open("official-cpe-dictionary_v2.3.xml.zip", "wb") as file:
        file.write(response.content)

    # Extract the XML file from the ZIP archive
    with zipfile.ZipFile("official-cpe-dictionary_v2.3.xml.zip", "r") as archive:
        archive.extractall()

    # Read the XML file
    tree = ET.parse("official-cpe-dictionary_v2.3.xml")
    root = tree.getroot()

    # Define the XML namespace
    ns = {"cpe": "http://cpe.mitre.org/dictionary/2.0"}

    # Extract vendor names from the XML data
    vendors = set()
    for cpe_item in root.findall(".//cpe:cpe-item", ns):
        vendor_elem = cpe_item.find("cpe:vendor", ns)
        if vendor_elem is not None and vendor_elem.text is not None:
            vendors.add(vendor_elem.text)

    # Convert vendors set to a list
    vendors_list = list(vendors)

    # Save the vendors list in a JSON file
    file_name = 'vendors.json'
    vendor_dir = os.path.join("data", "nvd", file_name)
    with open(vendor_dir, "w") as file:
        json.dump(vendors_list, file)

    # Print the list of vendors
    for vendor in vendors_list:
        print(vendor)
else:
    print("Failed to download the CPE dictionary.")


import xml.etree.ElementTree as ET

def process_element(elem):
    print("process element function called")
     # Extract the data from the XML element
    vendor_elem = elem.find("{http://cpe.mitre.org/dictionary/2.0}vendor")
    product_elem = elem.find("{http://cpe.mitre.org/dictionary/2.0}product")
    version_elem = elem.find("{http://cpe.mitre.org/dictionary/2.0}version")

    # Check if the elements exist before accessing their text attribute
    vendor = vendor_elem.text if vendor_elem is not None else ""
    product = product_elem.text if product_elem is not None else ""
    version = version_elem.text if version_elem is not None else ""

    print(f"Vendor: {vendor}")
    print(f"Product: {product}")
    print(f"Version: {version}")
    print("---")

# Open the XML file for parsing
with open("official-cpe-dictionary_v2.3.xml", "rb") as file:
    # Create an iterator for parsing the XML file incrementally
    context = ET.iterparse(file, events=("start", "end"))

    # Skip the root element
    _, root = next(context)

    # Process each element in the XML file
    for event, elem in context:
        if event == "end" and elem.tag == "{http://cpe.mitre.org/dictionary/2.0}cpe-item":
            # Process the element and print the data
            process_element(elem)

            # Clear the element from memory
            elem.clear()

            # Move to the next sibling element to save memory
            root.clear()


process_element()