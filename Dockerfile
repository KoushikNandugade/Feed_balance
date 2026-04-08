FROM python:3.12-slim

WORKDIR /app

# Copy ALL project files first (required because pyproject.toml references local directories)
COPY . .

# Install the project and its dependencies
RUN pip install --no-cache-dir .

# Expose port 7860 (default for HF Spaces)
EXPOSE 7860

# Ensure the app can find its internal modules
ENV PYTHONPATH=/app

# Run the server on port 7860
CMD ["python", "-m", "feed_balance.server.app", "--port", "7860"]
