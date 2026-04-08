FROM python:3.12-slim

WORKDIR /app

# Install dependencies
COPY pyproject.toml .
RUN pip install --no-cache-dir .

# Copy project files
COPY . .

# Expose port 7860 (default for HF Spaces)
EXPOSE 7860

# Run the server on port 7860
CMD ["python", "-m", "feed_balance.server.app", "--port", "7860"]
