import json


def verify_json_file(file_path):
    try:
        with open(file_path, 'r') as file:
            json_data = json.load(file)
            print("JSON file is valid.")
    except json.JSONDecodeError as e:
        print(f"Error in JSON file: {e}")
        print("Here are the 3 lines around the error:")
        with open(file_path, 'r') as file:
            lines = file.readlines()
            error_line = e.lineno - 1
            for i in range(max(0, error_line - 3), min(len(lines), error_line + 4)):
                print(f"{i + 1}: {lines[i].strip()}")


if __name__ == "__main__":
    file_path = "Idnes_data_final.json"  # Replace with the path to your JSON file
    verify_json_file(file_path)
