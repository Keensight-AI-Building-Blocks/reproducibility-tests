import yaml
import subprocess
from tqdm import tqdm

temperature_values = [0.7, 1.0, 1.3]
top_p_values = [0.8, 1.0, 1.2]
grading_prompts = ["strict", "normal", "lenient"]

base_config = {
    "model": "gpt-4o-mini",
    "max_completion_tokens": 1024,
    "seed": 42,
    "input_file": "input_test_data.csv",
    "temperature": 1.0,
    "top_p": 1.0,
    "prompt": "normal"
}

def update_config(config):
    with open("config.yaml", "w") as f:
        yaml.dump(config, f, default_flow_style=False, sort_keys=False)

def run_test():
    subprocess.run(["python", "test.py"])

for temp in tqdm(temperature_values, desc="Temperature Values"):
    for _ in range(5):
        config = base_config.copy()
        config["temperature"] = temp
        update_config(config)
        run_test()

for top_p in tqdm(top_p_values, desc="Top P Values"):
    for _ in range(5):
        config = base_config.copy()
        config["top_p"] = top_p
        update_config(config)
        run_test()

for prompt in tqdm(grading_prompts, desc="Grading Prompts"):
    for _ in range(5):
        config = base_config.copy()
        config["prompt"] = prompt
        update_config(config)
        run_test()