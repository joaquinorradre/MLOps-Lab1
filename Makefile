# Makefile

# Install dependencies from lock file
install:
	uv sync

# Format code with Black
format:
	uv run black api/ cli/ mylib/ tests/

# Lint code with Pylint
lint:
	uv run python -m pylint api/ cli/ mylib/ tests/

# Run tests with Pytest and measure coverage
test:
	uv run python -m pytest -v --cov=mylib --cov=api --cov=cli tests/

# "all" option to run everything in order
all:
	make format
	make lint
	make test