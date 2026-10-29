from src.translator import Translator
from src.verifier import Verifier
from config import MAX_ATTEMPTS

def run_pipeline(scheme_code: str):
    translator = Translator()
    verifier = Verifier()

    print("\n🚀 [1/3] Translating Scheme to Python...")
    try:
        python_code = translator.translate(scheme_code)
    except Exception as e:
        print(f"❌ Translation failed with exception: {e}")
        raise

    if not python_code.strip():
        raise ValueError("Pipeline halted: Translator produced empty python code.")

    for attempt in range(1, MAX_ATTEMPTS + 1):
        print(f"\n🔍 [2/3] Verifying generated code (Attempt {attempt}/{MAX_ATTEMPTS})...")
        
        is_valid, error_msg = verifier.verify(python_code)

        if is_valid:
            print("\n✅ Verification Passed! Code is syntactically sound and passes all tests.")
            print("\n--- FINAL RESULT ---")
            print("Status: SUCCESS")
            print(f"Attempts: {attempt}")
            print("\nGenerated Python Code:\n")
            print(python_code)
            return python_code
        else:
            print(f"⚠️ Verification Failed on Attempt {attempt}.")
            print(f"Error details:\n{error_msg}")

            if attempt == MAX_ATTEMPTS:
                print("\n❌ Pipeline failed: Max attempts reached without successful verification.")
                raise RuntimeError(f"Pipeline failed after {MAX_ATTEMPTS} attempts. Last error:\n{error_msg}")

            print(f"\n🔧 [3/3] Sending error back to translator for repair...")
            try:
                python_code = translator.repair(scheme_code, python_code, error_msg)
            except Exception as e:
                print(f"❌ Repair generation failed with exception: {e}")
                raise

if __name__ == "__main__":
    sample_scheme = """
    (define (factorial n)
      (if (<= n 1)
          1
          (* n (factorial (- n 1)))))
    """
    run_pipeline(sample_scheme)