#!/bin/bash
# test_script.sh

# Extract sleep time from req file
sleep_time=$(grep -o 'sleep_time=[0-9.]*' "$2" | cut -d= -f2)

# Sleep for the specified duration
sleep "$sleep_time"

# Write to response file
echo "Completed after ${sleep_time}s" > "$3"