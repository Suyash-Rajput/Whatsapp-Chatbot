

def read_json_file(file_path):
    my_json_data = {}
    if not check_file(file_path):
        return my_json_data
    with open(file_path, "r", encoding="utf-8") as json_file:
        my_json_data = json.load(json_file)
    return my_json_data