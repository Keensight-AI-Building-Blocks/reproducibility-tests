from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
import pandas as pd
import os
from tqdm import tqdm
import yaml
import time

config_file = "config.yaml"
if os.path.exists(config_file):
    with open(config_file, "r") as f:
        config_data = yaml.safe_load(f)
else:
    config_data = {}

class CFG:
    model = config_data.get("model", "gpt-4o-mini")
    temperature = config_data.get("temperature", 1.0)
    max_completion_tokens = config_data.get("max_completion_tokens", 1024)
    top_p = config_data.get("top_p", 1.0)
    seed = config_data.get("seed", 42)
    input_file = config_data.get("input_file", "input_test_data.csv")
    prompt = config_data.get("prompt", "normal")

prompts_file = "judge_prompts.yaml"
if os.path.exists(prompts_file):
    with open(prompts_file, "r") as f:
        prompts_data = yaml.safe_load(f)

cfg = CFG()

API_KEY = os.environ.get("OPENAI_API_KEY")

llm = ChatOpenAI(model="gpt-4o-mini", api_key=API_KEY, seed=cfg.seed, temperature=cfg.temperature, max_completion_tokens=cfg.max_completion_tokens, top_p=cfg.top_p)

class Rating(BaseModel):
    rating: float = Field(
        description="Rating of the response from 0-5"
    )

parser = JsonOutputParser(pydantic_object=Rating)

prompt = PromptTemplate(
    template = f"""{prompts_data.get(cfg.prompt, prompts_data["normal"])}""",
    input_variables=["comments", "response"],
    partial_variables={"format_instructions": parser.get_format_instructions()},
)

chain = prompt | llm | parser

data = pd.read_csv(cfg.input_file, index_col=0)

tqdm.pandas()

timestamp = time.strftime("%Y%m%d-%H%M%S")

print("Processing data...")

OUTPUT_DIR = f"output/{timestamp}"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def apply_rating(row):
    retries = 3
    for _ in range(retries):
        try:
            return chain.invoke(input={"comments": row["comments"], "response": row["response"]})["rating"]
        except Exception as e:
            print(f"Error: {e}. Retrying...")
            time.sleep(1)
    return None

data["ratings"] = data.progress_apply(apply_rating, axis=1)

print("Data processed successfully")

data.to_csv(os.path.join(OUTPUT_DIR,"output_test_data.csv"))

print("Average rating: ", data["ratings"].mean())

metadata = {
    "model": cfg.model,
    "temperature": cfg.temperature,
    "max_completion_tokens": cfg.max_completion_tokens,
    "top_p": cfg.top_p,
    "prompt": cfg.prompt,
    "seed": cfg.seed,
    "no_of_samples": len(data),
    "avg_rating": round(float(data["ratings"].mean()),3),
    "variance": round(float(data["ratings"].var()),3),
    "std_dev": round(float(data["ratings"].std()),3),
    "timestamp": timestamp
}

with open(os.path.join(OUTPUT_DIR, "metadata.yaml"), "w") as f:
    yaml.dump(metadata, f, default_flow_style=False, sort_keys=False)