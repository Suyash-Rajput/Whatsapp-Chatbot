import os, csv
import json
from datetime import datetime, timezone

def read_json_file(file_path):
    my_json_data = {}
    if not os.path.exists(file_path):
        return my_json_data
    with open(file_path, "r", encoding="utf-8") as json_file:
        my_json_data = json.load(json_file)
    return my_json_data

def print_time_taken(start_time, end_time):
    end_time_aware = end_time.replace(tzinfo=timezone.utc)
    duration = end_time_aware - start_time
    total_time_seconds = duration.total_seconds()
    print(f"Time taken - : {total_time_seconds:.6f} seconds")
    seconds = round(total_time_seconds, 0)
    minutes = seconds // 60
    return minutes


def read_csv(file_path):
    data = []
    with open(file_path, 'r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(row)
    return data