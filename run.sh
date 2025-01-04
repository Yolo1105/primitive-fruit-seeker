#!/bin/bash

echo "Running crawl_1.py..."
python3 crawl_1.py
if [ $? -ne 0 ]; then
    echo "Error: crawl_1.py failed to execute."
    exit 1
fi

echo "Running parse_data_2.py..."
python3 parse_data_2.py
if [ $? -ne 0 ]; then
    echo "Error: parse_data_2.py failed to execute."
    exit 1
fi

echo "Running convert_to_json_3.py..."
python3 convert_to_json_3.py
if [ $? -ne 0 ]; then
    echo "Error: convert_to_json_3.py failed to execute."
    exit 1
fi

echo "All scripts executed successfully."