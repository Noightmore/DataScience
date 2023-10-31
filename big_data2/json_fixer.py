import json


def remove_and_verify_json(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    try:
        json_data = json.loads(''.join(lines))
        print("JSON file is valid.")
    except json.JSONDecodeError as e:
        print(f"Error in JSON file: {e}")
        print("Here are the 3 lines around the error (with the error line removed):")
        error_line = e.lineno - 1
        del lines[error_line]
        for i in range(max(0, error_line - 3), min(len(lines), error_line + 3)):
            print(f"{i + 1}: {lines[i].strip()}")


if __name__ == "__main__":
    file_path = "Idnes_data_final.json"  # Replace with the path to your JSON file
    remove_and_verify_json(file_path)
