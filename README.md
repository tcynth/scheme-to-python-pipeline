# Scheme-to-Python AI Transpiler & Verification Pipeline

An agentic AI engineering project that transpiles Scheme code into idiomatic Python 3, backed by an automated execution, AST validation, and self-correction repair loop.

## 🚀 Architecture & Features

- **Provider-Agnostic LLM Integration:** Powered by high-speed cloud inference (Groq) with a secure, generic API key abstraction (`AI_API_KEY`).
- **Multi-Tier Verification Harness:** 
  1. *Static Analysis:* Validates syntax safety using Python's built-in `ast` module.
  2. *Dynamic Sandboxing:* Executes code safely within an isolated subprocess with strict timeouts.
- **Agentic Self-Correction Loop:** If verification fails, the pipeline automatically captures the error traceback, feeds it back into the model context, and triggers an autonomous repair cycle.
- **Clean Configuration Management:** Centralized configuration parameters and environment variables managed at the project root.

---

## 📂 Project Structure

```text
scheme-to-python-pipeline/
├── .env.example        # Template for secure environment variables
├── .gitignore          # Protects secrets (.env, cache, virtual environments)
├── config.py           # Centralized configuration & versioning
├── src/
│   ├── pipeline.py     # Main agentic execution state machine
│   ├── translator.py   # LLM translation & repair client
│   └── verifier.py     # AST & subprocess execution harness


