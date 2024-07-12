# FastAPI Web Application

A web application built using FastAPI, SQLAlchemy, and Pydantic, following the MVC design pattern. It includes user authentication, post management, and caching.

## Features

- User Signup and Login
- Token-based Authentication
- CRUD Operations for Posts
- In-memory Caching for Posts
- Field Validation with Pydantic

## Requirements

- Python 3.8+
- MySQL Database

## Installation

### 1. Clone the Repository

```sh
git clone https://github.com/yourusername/fastapi-webapp.git
cd fastapi-webapp
```

### 2. Create and Activate Virtual Environment

```sh
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```sh
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Create a `.env` file in the root directory and add the following:

```env
DATABASE_URL=mysql+pymysql://user:password@localhost/dbname
SECRET_KEY=mysecret_secret_key
```

### 5. Apply Database Migrations

Initialize the database by creating the required tables:

```sh
alembic upgrade head
```

### 6. Run the Application

Start the FastAPI application using Uvicorn:

```sh
uvicorn app.main:app --reload
```
