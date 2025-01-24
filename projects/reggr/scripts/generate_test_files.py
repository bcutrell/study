import os
import random

test_dir = "test_inputs"
os.makedirs(test_dir, exist_ok=True)

for i in range(100):
    sleep_time = random.uniform(1.0, 5.0)
    content = f"sleep_time={sleep_time:.2f}"
    path = f"{test_dir}/req_{i:03}"
    
    with open(path, 'w') as f:
        f.write(content)