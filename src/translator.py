from groq import Groq
from config import AI_API_KEY, MODEL_NAME, TEMPERATURE

class Translator:
    def __init__(self, api_key: str | None = None):
        key = api_key or AI_API_KEY
        if not key:
            raise ValueError("AI_API_KEY not found in environment or .env file.")
        
        self.client = Groq(api_key=key)
        self.model = MODEL_NAME
        
        print(f"🔌 [Groq Translator] Initialized client successfully with model: {self.model}")

    def translate(self, scheme_code: str) -> str:
        """Translates Scheme code into clean, standalone Python code using Groq."""
        print(f"🌐 [Groq Translator] Sending translation request to API...")
        
        prompt = f"""
You are an expert compiler engineer. Translate the following Scheme code into idiomatic Python 3.

Requirements:
1. Return ONLY valid Python code inside a ```python ``` code block.
2. Do not include markdown commentary, explanations, or usage examples outside the code block.
3. Ensure function names and signatures logically correspond to the Scheme definitions.

Scheme Code:
{scheme_code}
"""
        # Exceptions (like connection errors or API timeouts) will naturally bubble up
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=TEMPERATURE
        )
        code = self._extract_code(response.choices[0].message.content)
        
        if not code:
            raise ValueError("Translator received a response from the API, but code extraction resulted in empty output.")
            
        print(f"✨ [Groq Translator] Received and extracted translation response.")
        return code

    def repair(self, scheme_code: str, python_code: str, error_msg: str) -> str:
        """Fixes failed Python translation given the error traceback from the Verifier."""
        print(f"🔧 [Groq Translator] Triggering repair loop with error context...")
        
        prompt = f"""
A previous translation of Scheme to Python produced a runtime or syntax error.

Original Scheme Code:
{scheme_code}

Faulty Python Code:
{python_code}

Error / Traceback from Verifier:
{error_msg}

Task: Fix the Python code so that it passes execution cleanly.
Return ONLY the corrected, valid Python code inside a ```python ``` code block.
"""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=TEMPERATURE
        )
        code = self._extract_code(response.choices[0].message.content)
        
        if not code:
            raise ValueError("Repair agent received a response, but code extraction resulted in empty output.")
            
        return code

    def _extract_code(self, text: str) -> str:
        """Extracts code inside ```python ``` blocks if present."""
        if "```python" in text:
            return text.split("```python")[1].split("```")[0].strip()
        elif "```" in text:
            return text.split("```")[1].split("```")[0].strip()
        return text.strip()