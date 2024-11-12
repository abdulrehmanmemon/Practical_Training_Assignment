## Overview

This project is a FastAPI-based web application with PostgreSQL as the database. It includes user authentication and role-based access control. Admin users can create, update, and delete users, while regular users can view their own profiles.

## Architecture

- **FastAPI**: The web framework used for building the API.
- **PostgreSQL**: The database used for storing user data.
- **Docker**: Used for containerizing the application and database.
- **SQLAlchemy**: ORM used for database interactions.
- **Pydantic**: Used for data validation and serialization.


### User Login:

Users can log in by sending a POST request to the /login endpoint with their username and password.
If the credentials are valid, a JWT is generated and returned to the user.

### Authenticated Requests:

Users must include the JWT in the Authorization header of subsequent requests to authenticate themselves.
The application verifies the JWT and extracts the user information to enforce role-based access control.
### CRUD Operations:

Admin users can perform CRUD operations on user data by sending requests to the appropriate endpoints (users, /users/{user_id}).
Regular users can view their own profile by sending a GET request to /users/{user_id}.

## Setup Instructions

### Prerequisites

- Docker and Docker Compose installed on your machine.

### Steps

1. **Clone the repository**:
   git clone https://github.com/abdulrehmanmemon/Practical_Training_Assignment.git
   
2. **Create a .env file**: Create a .env file in the root directory and add the following environment variables:
DATABASE_URL=postgresql://postgres:expired@localhost/Project
SECRET_KEY=your_secret_key
ACCESS_TOKEN_EXPIRE_MINUTES=30
ALGORITHM=HS256
3. **Build and run the Docker containers**:
   docker-compose up --build
4. **Access the application:**
   The application will be available at http://127.0.0.1:8000
5. **API Documentation**:
   You can access the API documentation at http://127.0.0.1:8000/docs


# API Usage
**Login**
Endpoint: POST /login
curl -X POST "http://127.0.0.1:8000/login" -H "Content-Type: application/x-www-form-urlencoded" -d 'username=ali&password=ali'
{
  "access_token": "your_access_token",
  "token_type": "bearer"
}

**Register a User  (Admin Only)**
Endpoint: POST /register 
curl -X POST "http://127.0.0.1:8000/register" \
-H "Content-Type: application/json" \
-H "Authorization: Bearer your_access_token" \
-d '{
  "username": "ali",
  "email": "ali@example.com",
  "password": "ali",
  "role": "user"
}'

**Get All Users (Admin Only)**
Endpoint: GET /users
curl -X GET "http://127.0.0.1:8000/users" -H "Authorization: Bearer your_access_token"

**Get User by ID**
Endpoint: GET /users/{user_id}
curl -X GET "http://127.0.0.1:8000/users/1" -H "Authorization: Bearer your_access_token"

**Update User (Admin Only)**
Endpoint: PUT /users/{user_id}
curl -X PUT "http://127.0.0.1:8000/users/1" -H "Authorization: Bearer your_access_token" -H "Content-Type: application/json" -d '{
  "username": "updateduser",
  "email": "updateduser@example.com",
  "password": "newpassword",
  "role": "user"
}'

**Delete User (Admin Only)**
Endpoint: DELETE /users/{user_id}
curl -X DELETE "http://127.0.0.1:8000/users/1" -H "Authorization: Bearer your_access_token"


**Get All Users (Admin Only)**
Endpoint: GET /users
curl -X GET "http://127.0.0.1:8000/users" -H "Authorization: Bearer your_access_token"

by Abdul Rehman
