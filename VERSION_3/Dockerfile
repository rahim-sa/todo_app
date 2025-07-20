FROM python:3.11-slim

# 1. Install UV and system dependencies
RUN pip install --no-cache-dir uv && \
    apt-get update && \
    apt-get install -y --no-install-recommends build-essential && \
    rm -rf /var/lib/apt/lists/*

# 2. Set up project
WORKDIR /app
COPY . .

# 3. Install with UV (system-wide)
RUN uv pip install --system . --no-cache-dir

# 4. Create direct Python runner
RUN echo '#!/bin/sh\npython todo_app_v3.py' > /entrypoint.sh && \
    chmod +x /entrypoint.sh

CMD ["/entrypoint.sh"]