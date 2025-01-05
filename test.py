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

cfg = CFG()

API_KEY = os.environ.get("OPENAI_API_KEY")

llm = ChatOpenAI(model="gpt-4o-mini", api_key=API_KEY, seed=cfg.seed, temperature=cfg.temperature, max_completion_tokens=cfg.max_completion_tokens, top_p=cfg.top_p)

class Rating(BaseModel):
    rating: float = Field(
        description="Rating of the response from 0-5"
    )

parser = JsonOutputParser(pydantic_object=Rating)



prompt = PromptTemplate(
    template="""
This output is from a YouTube comment analysis pipeline, which analyzes comments on a given video. Your task is to evaluate the quality of the analysis based on the following structure provided in the response:\n
{format_instructions}\n

Response:
strengths (List[str]): Key strengths identified in the comments.
weaknesses (List[str]): Notable weaknesses highlighted in the comments.
opportunities (List[str]): Potential opportunities suggested by the comments.
suggestions (List[str]): Specific suggestions provided by the comments.
overall_sentiment (str): A concise description of the overall sentiment expressed in the comments.
Below are the comments for the analyzed video:
Comments:
{comments}

Analysis Response:
{response}

Your task is to evaluate the analysis provided in the Response and grade its accuracy, clarity, and completeness.""",
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

data["ratings"] = data.progress_apply(lambda x: chain.invoke(input={"comments": x["comments"], "response": x["response"]})["rating"], axis=1)



print("Data processed successfully")

data.to_csv(os.path.join(OUTPUT_DIR,"output_test_data.csv"))

print("Average rating: ", data["ratings"].mean())

metadata = {
    "model": cfg.model,
    "temperature": cfg.temperature,
    "max_completion_tokens": cfg.max_completion_tokens,
    "top_p": cfg.top_p,
    "seed": cfg.seed,
    "no_of_samples": len(data),
    "avg_rating": round(float(data["ratings"].mean()),3),
    "variance": round(float(data["ratings"].var()),3),
    "std_dev": round(float(data["ratings"].std()),3),
    "timestamp": timestamp
}

with open(os.path.join(OUTPUT_DIR, "metadata.yaml"), "w") as f:
    yaml.dump(metadata, f, default_flow_style=False, sort_keys=False)