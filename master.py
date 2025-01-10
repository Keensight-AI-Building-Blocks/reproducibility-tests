import yaml
import subprocess
from tqdm import tqdm
import os

# temperature_values = [0.0, 0.5, 1.0]
# top_p_values = [0.0, 0.5, 1.0]
# grading_prompts = ["strict", "normal", "lenient"]
grading_prompts = ["normal","lenient"]

base_config = {
    "model": "gpt-4o-mini",
    "max_completion_tokens": 1024,
    "input_file": "input_test_data.csv",
    "temperature": 1.0,
    "top_p": 1.0,
    "prompt": "normal"
}

def update_config(config):
    with open("config.yaml", "w") as f:
        yaml.dump(config, f, default_flow_style=False, sort_keys=False)

def run_test(log_file):
    with open(log_file, "a") as f:
        subprocess.run(["python", "test.py"], stdout=f, stderr=subprocess.STDOUT)

# Log file to store all test runs
log_file = "output/all_tests.log"
os.makedirs("output", exist_ok=True)

# for temp in tqdm(temperature_values, desc="Temperature Values"):
#     for i in range(5):
#         config = base_config.copy()
#         config["temperature"] = temp
#         update_config(config)
#         with open(log_file, "a") as f:
#             f.write(f"\nRunning test with temperature={temp}, run={i+1}\n")
#         run_test(log_file)

# for top_p in tqdm(top_p_values, desc="Top P Values"):
#     for i in range(5):
#         config = base_config.copy()
#         config["top_p"] = top_p
#         update_config(config)
#         with open(log_file, "a") as f:
#             f.write(f"\nRunning test with top_p={top_p}, run={i+1}\n")
#         run_test(log_file)

for prompt in tqdm(grading_prompts, desc="Grading Prompts"):
    for i in range(5):
        config = base_config.copy()
        config["prompt"] = prompt
        update_config(config)
        with open(log_file, "a") as f:
            f.write(f"\nRunning test with prompt={prompt}, run={i+1}\n")
        run_test(log_file)