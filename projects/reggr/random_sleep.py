import random
import time
import argparse

def random_sleep(input_file, output_file):
    with open(input_file, 'r') as f:
        content = f.read()

    # Sleep for random duration
    duration = random.uniform(0, 5)
    print(f"Sleeping for {duration:.2f} seconds...")
    time.sleep(duration)
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    with open(output_file, 'w') as f:
        f.write(f"start={timestamp}\n")
        f.write(f"sleep={duration:.2f}\n")
        f.write(f"input_content={content}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process a file with random delay')
    parser.add_argument('-i', '--input', required=True, help='Input file path')
    parser.add_argument('-o', '--output', required=True, help='Output file path')
    args = parser.parse_args()
    random_sleep(args.input, args.output)
