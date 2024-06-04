import requests
import os
import subprocess
import time

# URLs to download the M3U8 files
urls = {
    "thuviencine_movies_new_iptv.m3u8": "https://hqth.me/phimlevip",
    "thuvienhd_phim-le_new_iptv.m3u8": "https://hqth.me/phimlevip2"
}

# Directory to save the downloaded files
download_dir = "."

def download_files(urls, download_dir):
    for filename, url in urls.items():
        start_time = time.time()
        response = requests.get(url)
        if response.status_code == 200:
            print(f"Downloading {filename} from {url}...")
            file_path = os.path.join(download_dir, filename)
            with open(file_path, 'wb') as file:
                file.write(response.content)
            end_time = time.time()
            print(f"Downloaded {filename} from {url} in {end_time - start_time:.2f} seconds")
        else:
            print(f"Failed to download {filename} from {url}")

def install_dependencies():
    print("Installing dependencies...")
    subprocess.check_call(["pip", "install", "pandas", "openpyxl", "requests"])
    print("Dependencies installed.")

def run_to_excel_script():
    print("Running to_excel.py script...")
    subprocess.check_call(["python", "to_excel.py"])
    print("Finished running to_excel.py script.")

if __name__ == "__main__":
    install_dependencies()
    download_files(urls, download_dir)
    run_to_excel_script()
