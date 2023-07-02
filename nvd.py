import requests
import zipfile
import os

# Specify the range of years for which you want to download CVE files
start_year = 2000
end_year = 2023
# Create the 'data' folder if it doesn't exist
data_folder = 'data'
if not os.path.exists(data_folder):
    os.makedirs(data_folder)

# Create the 'node' folder inside the 'data' folder if it doesn't exist
nvd_folder = os.path.join(data_folder, 'nvd')
if not os.path.exists(nvd_folder):
    os.makedirs(nvd_folder)

# Iterate over the years
for year in range(start_year, end_year + 1):
    # Construct the URL to download the CVE file for the current year
    url = f"https://nvd.nist.gov/feeds/json/cve/1.1/nvdcve-1.1-{year}.json.zip"

    # Send a GET request to download the CVE file
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Create a zip file with the year as the name
        zip_file_name = f"{year}.zip"
        zip_dir = os.path.join("data", "nvd",zip_file_name)
        with open(zip_dir, "wb") as file:
            file.write(response.content)
        print(f"Downloaded {zip_file_name}")
    else:
        print(f"Failed to download CVE file for {year}")

print("All CVE files downloaded and archived into " + zip_dir)
