# Use official Python image
FROM python:3.12-slim

# Set working directory in container
WORKDIR /app

# Copy requirements first for caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app
COPY . .

# Expose the port your app runs on
EXPOSE 5000

# Command to run your app (use gunicorn for production)
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
