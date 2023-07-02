import re
import json
import os
import zipfile

for year in range(2002, 2024):
    data_dir = "data/nvd/"
    zip_filename = f"{year}.zip"
    zip_path = os.path.join(data_dir, zip_filename)
    # print(zip_path)
    # Path to the folder where the extracted JSON files will be stored
    output_folder = 'data/nvd_extracted' 
    if not os.path.exists(output_folder):
        os.makedirs(output_folder, exist_ok=True)   
    output_dir =  os.path.join(output_folder)
    # Open the ZIP file

    try:
        with zipfile.ZipFile(zip_path, "r") as zip_file:
        # Assuming the JSON file is named 'data.json' within each ZIP file
            for file_name in zip_file.namelist():
                if file_name.endswith(".json"):
                    # Extract the JSON file from the ZIP file
                    zip_file.extract(file_name, output_folder)
                    # print(file_name)
                    json_file_path = os.path.join(output_dir, file_name)
                    # print(json_file_path)
                # Read the contents of the JSON file
                with open(json_file_path, 'r', encoding="utf-8") as json_file:
                    # Create the output folder if it doesn't exist
                    data = json.load(json_file)
                
                # Process the JSON data as needed
                # ...
                print(file_name + " extracted successfully")

                # Remove the extracted JSON file
                # os.remove(filename)
    except Exception as e:
        # print(f"Error reading {zip_path}: {e}")
        continue





# Load the NVD JSON file
extracted_json_files = 'data/nvd_extracted/'
for year in range(2002,2024):
    file_name = f"nvdcve-1.1-{year}.json"
    extracted_json_files_path = os.path.join(extracted_json_files, file_name) 
    # print(extracted_json_files_path)
    with open(extracted_json_files_path, encoding="utf-8") as file:
        nvd_data = json.load(file)

    # Extract the cpe23Uri data
    cpe23uris = []

    # Create a dictionary to store vendor data
    vendor_data = {}

    # Create CVE Versions
    cves = []


    print(len(nvd_data["CVE_Items"]))

    # Iterate over the CVE entries
    for i in range(len(nvd_data["CVE_Items"])):
        cve_num = nvd_data["CVE_Items"][i]["cve"]["CVE_data_meta"]["ID"]
        # Create a list of CVE numbers
        cve_numbers = [cve_num]
        # print(cve_numbers)
        # Extract vendor and product from the CPE URI
        for j in range(len(nvd_data["CVE_Items"][i]["configurations"]["nodes"])):
            cpe_data = nvd_data["CVE_Items"][i]["configurations"]["nodes"][j]["cpe_match"]
            for cpe in cpe_data:
                cpe23Uri = cpe["cpe23Uri"]
                vendor, product, version, *_ = cpe23Uri.split(":")[3:]
                # Check if vendor already exists in the dictionary
                if vendor in vendor_data:
                    # Check if product already exists for the vendor
                    if product in vendor_data[vendor]:
                        vendor_data[vendor][product]["products"].append(product)
                        vendor_data[vendor][product]["cpe23Uris"].append(cpe23Uri)
                        vendor_data[vendor][product]["cve"].append(cve_num)
                        # print(vendor_data[vendor][product])
                    else:
                        vendor_data[vendor][product] = {
                            "cve": [cve_num],
                            "products": [product],
                            "cpe23Uris": [cpe23Uri],
                        }
                        # print(vendor_data[vendor][product])
                else:
                    vendor_data[vendor] = {
                        product: {"cve": [cve_num], "products": [product], "cpe23Uris": [cpe23Uri]}
                    }
                    # print(vendor_data[vendor][product])

    # Create a folder to store the reports
    if not os.path.exists("reports"):
        os.makedirs("reports")

    # Save the vendor data in JSON files
    for vendor, products in vendor_data.items():
        # print(vendor_data)
        sanitized_vendor = re.sub(r'[\\/:*?"<>|]', "_", vendor)
        reports_dir = "reports/"
        vendor_folder = os.path.join(reports_dir, sanitized_vendor)
        os.makedirs(vendor_folder, exist_ok=True)

        for product, data in products.items():
            # print(products)
            # Sanitize the product name to remove invalid characters for file name
            sanitized_product = re.sub(r'[\\/:*?"<>|]', "_", product)

            output = {
                "cve": data["cve"],
                "vendor": vendor,
                "products": data["products"],
                "cpe23Uris": data["cpe23Uris"],
            }

            filename = f"{sanitized_product}.json"
            filepath = os.path.join(vendor_folder, filename)

            with open(filepath, "w") as outfile:
                json.dump(output, outfile, indent=4)

print("Reports generated successfully!")


