import ast
import subprocess
import tempfile
import os

class Verifier:
    def verify(self, python_code: str) -> tuple[bool, str]:
        """
        Verifies python code using:
        1. Static AST syntax checking.
        2. Dynamic execution sandbox test.
        Returns (is_valid, error_message).
        """
        # Step 1: Check syntax via AST
        try:
            ast.parse(python_code)
        except SyntaxError as e:
            return False, f"SyntaxError during AST parsing: {e}"
        except Exception as e:
            return False, f"Unexpected error during AST parsing: {e}"

        # Step 2: Dynamic execution / Test harness verification
        # We write the code to a temporary file and execute it safely in a subprocess
        try:
            with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as tmp:
                tmp.write(python_code)
                tmp_path = tmp.name

            # Run the file via subprocess to check for runtime errors
            result = subprocess.run(
                ["python3", tmp_path],
                capture_output=True,
                text=True,
                timeout=5
            )

            if result.returncode != 0:
                return False, f"Runtime/Execution Error:\n{result.stderr.strip()}"

        except subprocess.TimeoutExpired:
            return False, "Execution timed out (possible infinite loop)."
        except Exception as e:
            return False, f"Execution harness failed: {e}"
        finally:
            if 'tmp_path' in locals() and os.path.exists(tmp_path):
                os.unlink(tmp_path)

        return True, ""