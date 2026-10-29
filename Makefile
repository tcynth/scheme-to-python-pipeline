.PHONY: run clean ship

run:
	python3 -m src.pipeline

clean:
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -type d -exec rm -r {} +
	@echo "🧹 Cleaned Python bytecode and cache files."

ship: clean
	@echo "🚀 Running verification pipeline..."
	@python3 -m src.pipeline; \
	if [ $$? -eq 0 ]; then \
		echo ""; \
		echo "✅ Pipeline passed successfully! Preparing commit..."; \
		git add .; \
		read -p "💬 Enter commit message: " msg; \
		if [ -z "$$msg" ]; then \
			echo "❌ Commit message cannot be empty. Aborting."; \
			exit 1; \
		fi; \
		git commit -m "$$msg"; \
		echo "✨ Successfully committed changes!"; \
	else \
		echo ""; \
		echo "❌ Pipeline verification failed. Commit aborted."; \
		exit 1; \
	fi
