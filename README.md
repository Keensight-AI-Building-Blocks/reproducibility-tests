# reproducibility-tests

## Overview
This project contains a script to evaluate the quality of YouTube comment analysis using a language model. The script processes comments and responses, rates the analysis, and generates metadata about the evaluation.

## Configuration
The script uses a configuration file `config.yaml` to set various parameters:
- `model`: The language model to use (default: `gpt-4o-mini`)
- `temperature`: Sampling temperature (default: `1.0`)
- `max_completion_tokens`: Maximum tokens for completion (default: `1024`)
- `top_p`: Nucleus sampling parameter (default: `1.0`)
- `prompt`: The prompt type to use (default: `normal`)
- `input_file`: Path to the input CSV file containing comments and responses (default: `input_test_data.csv`)

## Usage
1. Ensure you have the required dependencies installed.
2. Set the `OPENAI_API_KEY` environment variable with your OpenAI API key.
3. Create a `config.yaml` file with the desired configuration (optional).
4. Run the script:
    ```bash
    python test.py
    ```

## Output
The script generates the following outputs:
- A CSV file with the ratings for each response in the `output/{timestamp}` directory.
- A `metadata.yaml` file containing metadata about the evaluation in the same directory.

## Example `config.yaml`
```yaml
model: "gpt-4o-mini"
temperature: 0.7
max_completion_tokens: 512
top_p: 0.9
prompt: "lenient"
input_file: "input_test_data.csv"
```

## Example `metadata.yaml`
```yaml
model: "gpt-4o-mini"
temperature: 1.0
max_completion_tokens: 1024
top_p: 1.0
prompt: "normal"
no_of_samples: 100
avg_rating: 4.5
variance: 0.25
std_dev: 0.5
timestamp: "20231010-123456"
total_time: 120.5
```

## Running Multiple Tests
To run multiple tests with different configurations, use the `master.py` script. This script will automatically update the configuration file and run the tests.

1. Ensure you have the required dependencies installed.
2. Set the `OPENAI_API_KEY` environment variable with your OpenAI API key.
3. Run the `master.py` script:
    ```bash
    python master.py
    ```

## Compiling Results
To compile the results from multiple test runs into a single CSV file, use the `compile.py` script.

1. Ensure you have the required dependencies installed.
2. Run the `compile.py` script:
    ```bash
    python compile.py
    ```
3. The compiled results will be saved in `metadata.csv`.

