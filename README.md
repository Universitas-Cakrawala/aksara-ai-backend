# Aksara AI Backend

## Description

Brief description of your project.

## Getting Started

### Prerequisites

Ensure you have the following software installed on your local machine:

- [Python 3.x](https://www.python.org/downloads/)
- [Git](https://git-scm.com/downloads/)

### Installation

1. **Clone the repository**

    ```sh
    git clone https://github.com/yourusername/yourproject.git
    cd yourproject
    ```

2. **Create and activate a virtual environment**

    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Copy the example environment file**

    ```sh
    cp .env.example .env
    ```

4. **Install the required packages**

    ```sh
    pip install -r requirements.txt
    ```

5. **Set up the database**

    Configure your PostgreSQL database connection in `.env`:
    ```env
    DATABASE_CONN=postgresql://username:password@localhost:5432/database_name
    ```

6. **Run database migrations**

    ```sh
    # Apply migrations
    make migrate-up
    
    # Seed database with initial data
    make seed
    ```

### Running the Project

1. **Run the application using Uvicorn**

    ```sh
    uvicorn main:app --reload --host 127.0.0.1 --port 8000
    ```

    - `main` is the name of the Python file containing your FastAPI app.
    - `app` is the name of the FastAPI instance.
    - `--reload` will enable auto-reload for development.
    - `--host 127.0.0.1` will make the server accessible only on local computer.
    - `--port 8000` specifies the port number.

### Accessing the Application

- Once the server is running, you can access the API documentation at:
  - OpenAPI: [Swagger Documentation](http://127.0.0.1:8000/docs)

### Default Credentials

After seeding the database, you can use these default credentials:
- **Username**: admin
- **Password**: admin123
- **Email**: admin@aksara.ai

## Database Migration

This project uses Alembic for database migrations. See [MIGRATION.md](MIGRATION.md) for detailed documentation.

### Quick Migration Commands

```sh
# Create new migration
make migrate-create MSG="Description of changes"

# Apply migrations
make migrate-up

# Rollback migration
make migrate-down REV=revision_id

# Check current status
make migrate-current

# Seed database
make seed
```

## Available Make Commands

```sh
# Setup (install + migrate + seed)
make setup

# Development
make dev              # Start development server
make install          # Install dependencies
make clean            # Clean cache files

# Database
make migrate-up       # Apply migrations
make migrate-down     # Rollback migration  
make migrate-create   # Create new migration
make seed             # Seed database

# Docker
make docker-up        # Start with Docker
make docker-down      # Stop Docker containers
```

## Project Structure

```
aksara-ai-backend/
├── migrations/           # Database migrations
├── src/
│   ├── auth/            # Authentication logic
│   ├── config/          # Database and app configuration
│   ├── health/          # Health check endpoints
│   ├── middleware/      # Custom middlewares
│   ├── refresh_token/   # JWT refresh token management
│   ├── user/            # User management
│   └── utils/           # Utility functions
├── main.py              # FastAPI application entry point
├── migrate.py           # Migration management script
├── seed.py              # Database seeding script
├── Makefile            # Development commands
└── requirements.txt     # Python dependencies
```

## Contributing

If you would like to contribute, please open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For further information or questions, you can contact me at [titanioy98@gmail.com](mailto:titanioy98@gmail.com)
