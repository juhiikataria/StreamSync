FROM python:3.11-slim-buster

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the container
COPY requirements.txt .

# Install dependencies
RUN pip install -r requirements.txt

# Copy the rest of the project files to the container
COPY . .

# Expose the port that the application will be running on
EXPOSE 8000

# Run the application
CMD ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "app.main:app"]

