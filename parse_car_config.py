import os
import pandas as pd
import openpyxl


def parse_config_file(file_path):
    """Parses a config.txt file and extracts parameters into a dictionary."""
    data = {}
    current_section = ""

    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if not line or line.startswith("#"):  # Ignore empty lines and comments
                continue

            if line.startswith("[") and line.endswith("]"):  # Detect section
                current_section = line.strip("[]")
            elif "=" in line:
                key, value = map(str.strip, line.split("=", 1))
                full_key = f"{current_section}.{key}" if current_section else key
                data[full_key] = value

    return data


def consolidate_configs_to_excel(base_folder, output_file):
    """Goes through all folders in base_folder, parses config.txt files, and consolidates data into an Excel file."""
    all_data = []

    for folder in os.listdir(base_folder):
        folder_path = os.path.join(base_folder, folder)
        config_path = os.path.join(folder_path, "config.txt")

        if os.path.isdir(folder_path) and os.path.isfile(config_path):
            config_data = parse_config_file(config_path)
            config_data["Folder Name"] = folder  # Add folder name to trace back
            all_data.append(config_data)

    if all_data:
        df = pd.DataFrame(all_data).fillna('')
        df.to_excel(output_file, index=False)
        print(f"Excel file saved: {output_file}")
    else:
        print("No valid config files found.")


if __name__ == "__main__":
    cars_folder = "E:\\SteamLibrary\\steamapps\\common\\Car Mechanic Simulator 2021\\Car Mechanic Simulator 2021_Data\\StreamingAssets\\Cars"  # Base folder where all car folders are located
    output_excel = "consolidated_configs.xlsx"
    consolidate_configs_to_excel(cars_folder, output_excel)
