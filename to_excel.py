import re
import pandas as pd
import os

def extract_movie_info_from_m3u8(file_path):
    # Define regex patterns to extract relevant information
    group_title_pattern = re.compile(r'group-title="([^"]+)"')
    year_pattern = re.compile(r'\((\d{4})\)')
    filename_year_pattern = re.compile(r'\b(\d{4})\b')
    resolution_pattern = re.compile(r'(\d{3,4}p)')
    size_pattern = re.compile(r'(\d+(\.\d+)?\sGB)')
    filename_pattern = re.compile(r',(.+\.(mkv|mp4|avi|mov|wmv|flv|m4v|ts|webm|vob))\s')

    # Lists to store extracted information
    titles = []
    years = []
    resolutions = []
    sizes = []
    links = []
    filenames = []
    long_tieng = []
    thuyet_minh = []
    file_types = []

    # Read the file contents
    with open(file_path, 'r', encoding='utf-8') as file:
        file_contents = file.readlines()

    # Process the file contents
    for i, line in enumerate(file_contents):
        if line.startswith('#EXTINF'):
            # Extract group title
            group_title_match = group_title_pattern.search(line)
            if group_title_match:
                title = group_title_match.group(1).strip()
            else:
                title = None

            # Extract year from the group title
            year_match = year_pattern.search(line)
            if year_match:
                year = year_match.group(1).strip()
            else:
                # If year not found in group-title, extract it from the filename
                filename_year_match = filename_year_pattern.search(line)
                if filename_year_match:
                    year = filename_year_match.group(1).strip()
                else:
                    year = None

            # Extract resolution from the filename
            resolution_match = resolution_pattern.search(line)
            if resolution_match:
                resolution = resolution_match.group(1).strip()
            else:
                resolution = None

            # Extract file size
            size_match = size_pattern.search(line)
            if size_match:
                size = size_match.group(1).strip()
            else:
                size = None

            # Extract filename from the EXTINF line
            filename_match = filename_pattern.search(line)
            if filename_match:
                download_filename = filename_match.group(1).strip()
                # Extract file type from filename
                file_type = download_filename.split('.')[-1]
            else:
                download_filename = None
                file_type = None

            # Extract link (next line after #EXTINF)
            if i + 1 < len(file_contents) and file_contents[i + 1].startswith('http'):
                link = file_contents[i + 1].strip()
            else:
                link = None

            # Determine Lồng Tiếng and Thuyết Minh
            long_tieng_flag = False
            thuyet_minh_flag = False

            if download_filename:
                long_tieng_flag = bool(re.search(r'(Long tieng|Lồng tiếng|LT|\.DUB\.)', download_filename, re.IGNORECASE))
                thuyet_minh_flag = bool(re.search(r'(Thuyết minh|Thuyet minh|Tm)', download_filename, re.IGNORECASE))

            titles.append(title if title else "")
            years.append(year if year else "")
            resolutions.append(resolution if resolution else "")
            sizes.append(size if size else "")
            links.append(link if link else "")
            filenames.append(download_filename if download_filename else "")
            long_tieng.append("Yes" if long_tieng_flag else "No")
            thuyet_minh.append("Yes" if thuyet_minh_flag else "No")
            file_types.append(file_type if file_type else "")

    # Create a DataFrame from the extracted information
    data = {
        'Title': titles,
        'Year': years,
        'Resolution': resolutions,
        'Size': sizes,
        'Link': links,
        'Filename': filenames,
        'Lồng Tiếng': long_tieng,
        'Thuyết Minh': thuyet_minh,
        'File Type': file_types
    }
    df = pd.DataFrame(data)

    return df

def process_all_m3u8_files(directory):
    # Process each M3U8 file in the directory
    for filename in os.listdir(directory):
        if filename.endswith('.m3u8'):
            file_path = os.path.join(directory, filename)
            try:
                df = extract_movie_info_from_m3u8(file_path)
                output_path = os.path.join(directory, f'{os.path.splitext(filename)[0]}.xlsx')
                df.to_excel(output_path, index=False)
                print(f"Data successfully saved to {output_path}")
            except Exception as e:
                print(f"Error processing {file_path}: {e}")

if __name__ == '__main__':
    directory = os.path.dirname(os.path.abspath(__file__))
    process_all_m3u8_files(directory)
