# main.py
# Stage 1, Step 1: Basic Server Setup

# 1. Import the FastAPI class from the fastapi library.
from fastapi import FastAPI

# 2. Create an instance of the FastAPI application.
# This 'app' object will be the main point of interaction for our API.
app = FastAPI(
    title="Student Performance Prediction API",
    version="0.0.1" # Start with a pre-release version
)

# 3. Define a route for the root URL ("/").
# The '@app.get("/")' is a "decorator" that tells FastAPI that the function
# below it is responsible for handling GET requests to the root path.
@app.get("/")
def read_root():
    """
    This is the root endpoint. It's a simple way to check if the
    server is running correctly.
    """
    return {"message": "Welcome to the Student Performance Prediction API. Server is running!"}

# --- Instructions to Run ---
# 1. Save this code in a file named `main.py`.
# 2. Open your terminal in the same directory.
# 3. Run the server with the command: uvicorn main:app --reload
# 4. Open your web browser and go to http://127.0.0.1:8000
#    You should see the welcome message.
