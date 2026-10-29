import os
from dotenv import load_dotenv

load_dotenv()

# API Configuration
AI_API_KEY = os.getenv("AI_API_KEY")

# Model & Generation Parameters
MODEL_NAME = os.getenv("AI_MODEL_NAME", "openai/gpt-oss-20b")
TEMPERATURE = 0.1
MAX_ATTEMPTS = 3
