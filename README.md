## Overview

This project is a FastAPI-based web application with PostgreSQL as the database. It includes user authentication and role-based access control. Admin users can create, update, and delete users, while regular users can view their own profiles.

## Architecture

- **FastAPI**: The web framework used for building the API.
- **PostgreSQL**: The database used for storing user data.
- **Docker**: Used for containerizing the application and database.
- **SQLAlchemy**: ORM used for database interactions.
- **Pydantic**: Used for data validation and serialization.

## Setup Instructions

### Prerequisites

- Docker and Docker Compose installed on your machine.

### Steps

1. **Clone the repository**:
   ```sh
   git clone https://github.com/your-repo/project-name.git
   cd project-name
