# DEMS

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

## Contributing

If you would like to contribute, please open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For further information or questions, you can contact me at [titanioy98@gmail.com](mailto:titanioy98@gmail.com)
