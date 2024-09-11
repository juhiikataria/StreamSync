# # Medpay-Task ( Devrishi Sikka )

Build a publisher/subscribe model to process streaming data and provide an up-to-date view of incoming data.

[Click here to try the API](http://13.235.242.50/docs)


## Getting Started

1. Run using any ASGI server (eg. Uvicorn):
   
   a. Install the required packages:
   
      ```bash
      pip install fastapi uvicorn pandas
      ```
   b. Clone the Project
      
        https://github.com/DevrishiSikka/Medpay-Task.git
        cd Medpay-Task-main
   
   c. Run the FastAPI application:
      
      ```bash
      uvicorn app.main:app --reload
      ```
   d. Access the API docs
       
       http://127.0.0.1:8000/doc


2. Run using Docker Container and deploy on AWS EC2

   a. Create Dockerfile with the following configuration

   ``` Dockerfile
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
   ```

   b. Build the Docker image

   ```Dockerfile
   docker build -t <IMAGE_NAME> .
   ```

   c. Run dockerfile and map port 8000 of docker container to port 80 of the EC2 machine 
   ```Dockerfile
   docker run -dp 80:8000 <IMAGE_NAME>
   ```


# Info File

app/main.py: Main FastAPI application file with API routes and configurations.

data/transaction.csv: Contains transaction data.

data/sku_info.csv: Contains SKU information.

routers/CategoryOperations.py: Contains API endpoints for category-related operations.

routers/SKUOperations.py: Contains API endpoints for SKU-related operations.

routers/Transactions.py: Contains API endpoints for transaction-related operations.

