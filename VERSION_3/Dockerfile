# Use Python 3.11 (slim reduces image size)
FROM python:3.11-slim

# Install UV for Windows compatibility
RUN pip install uv && \
    uv venv --python=3.11 /venv && \
    . /venv/bin/activate

# Set working directory (PowerShell compatible)
WORKDIR C:/app

# Copy dependency files (caching optimization)
COPY pyproject.toml .
RUN uv pip install . --no-cache-dir  # Force clean install

# Copy app code (excludes files in .dockerignore)
COPY . .

# Test command (matches your local workflow)
RUN uv run pytest --cov=src --cov-report=term-missing

# Main command (matches your 'uv run todo_app_v3.py')
CMD ["uv", "run", "todo_app_v3.py"]