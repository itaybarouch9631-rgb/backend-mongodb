Backend MongoDB

A REST API built with Python, FastAPI, MongoDB Atlas, and Docker.

Features

User registration and login

JWT-based authentication

Task creation and retrieval

User-specific task access

MongoDB Atlas integration

Automated tests with pytest

Docker containerization

Tech Stack

Python

FastAPI

MongoDB Atlas

PyMongo

JWT

Docker

pytest

Project Structure

backend-mongodb/
├── main.py
├── database.py
├── schemas.py
├── security.py
├── routers/
├── services/
├── tests/
├── requirements.txt
├── Dockerfile
├── .dockerignore
└── .gitignore

Configuration

Create a .env file in the project root with the following variables:

MONGODB_URI=your_mongodb_connection_string
JWT_SECRET_KEY=your_secret_key

Replace the placeholder values with your own credentials. Never commit the .env file or publish your secrets.

Run Locally

Create and activate a virtual environment, then install the dependencies:

python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

Start the API:

uvicorn main:app --reload

Open the interactive API documentation at:

http://localhost:8000/docs

Run with Docker

Build the image:

docker build -t backend-mongodb .

Start the container:

docker run -d --name backend-api -p 8000:8000 --env-file .env backend-mongodb

Open the API documentation at:

http://localhost:8000/docs

Run Tests

python -m pytest -v

Project Status

This project is under active development. Features, tests, and documentation will evolve as the project grows.