from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROMPTS_PATH = PROJECT_ROOT / "prompts" / "prompts.json"
LOG_DIR = PROJECT_ROOT / "logs"

OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
TIMEOUT = 120

#COACH = "llama3.2:3b"
COACH = "mistral:7b"
TEMP_COACH = 0.4
COACH_OPTIONS = { "temperature": TEMP_COACH}


#GENERATOR = "phi3:mini"
GENERATOR = "mistral:7b"
TEMP_GENERATOR = 0.9
GENERATOR_OPTIONS = { "temperature": TEMP_GENERATOR}


ITERATIONS = 10
SEED_JOKE = "Why was the LLM impatient? because it couldn't wait (weight)?"



