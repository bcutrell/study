#!/usr/bin/env python3
import os
from pathlib import Path

def combine_files(directories=["src", "benches", "tests"]):
    result = []

    for directory in directories:
        if not os.path.exists(directory):
            continue

        for filepath in Path(directory).rglob("*.rs"):
            # Add filename as comment
            result.append(f"// {filepath}")

            # Read and add file contents
            with open(filepath, 'r') as f:
                result.append(f.read())

            # Add newline between files
            result.append("\n")

    return "\n".join(result)

if __name__ == "__main__":
    print(combine_files())
