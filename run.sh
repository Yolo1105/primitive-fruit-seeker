#!/bin/bash

# Step 1: Execute convert_to_json_3.py
echo "Running convert_to_json_3.py..."
python3 convert_to_json_3.py
if [ $? -ne 0 ]; then
    echo "Error: convert_to_json_3.py failed to execute."
    exit 1
fi

# Step 2: Execute crawl_1.py
echo "Running crawl_1.py..."
python3 crawl_1.py
if [ $? -ne 0 ]; then
    echo "Error: crawl_1.py failed to execute."
    exit 1
fi

# Step 3: Execute parse_data_2.py
echo "Running parse_data_2.py..."
python3 parse_data_2.py
if [ $? -ne 0 ]; then
    echo "Error: parse_data_2.py failed to execute."
    exit 1
fi

echo "All scripts executed successfully."
