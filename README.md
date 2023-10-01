# Book Giveaway Service API

## Introduction

The Book Giveaway Service API is a RESTful service designed to streamline the process of sharing books among users. This API provides a platform for both registered and non-registered users to give away books they no longer need and discover new books to read. It includes user registration, book management, and various resources like book authors, genres, conditions, and more.

## Technology Stack

This project is built using the following technologies:

- **Python**: The core programming language used for development.
- **Django**: A powerful Python web framework.
- **Django Rest Framework**: A toolkit for building Web APIs in Django.
- **PostgreSQL**: A robust open-source relational database system.
- **Docker**: A containerization platform for easy deployment.

## Getting Started

Follow these steps to set up and run the Book Giveaway Service API on your local machine:

### Clone the Project

```sh
git clone https://github.com/TatoSoselia/book-giveaway-rest-api.git

```

### Install Dependencies

Build the project's dependencies using Docker Compose:

```sh
docker-compose build
```

### Run the API

Start the API server with Docker Compose:

```sh
docker-compose up
```

## Register as Superuser

To access the admin panel and perform administrative tasks, you need to register as a superuser. Run the following command via Docker Compose:

```sh
docker-compose run --rm app sh -c "python manage.py createsuperuser"
```

Now, you can access the admin panel at:

```sh
http://127.0.0.1:8000/admin/
```

## API Documentation

comprehensive API documentation using Swagger, simplifying the process of understanding and interacting with the API. To access and explore the API documentation, please follow these steps:

1. **Start the API Server**: Make sure that the API server is up and running, following the instructions provided in the "Getting Started" section.
2. **Access the Swagger UI**: Open your web browser and navigate to the Swagger UI endpoint, which is typically located at:

```sh
http://127.0.0.1:8000/api/docs/
```

Here, you will find extensive information about API endpoints, their functionalities, and detailed usage instructions.

## Testing
To ensure the reliability and functionality of this project, use testing. You can run the tests the following command via Docker Compose:
```sh
docker-compose run --rm app sh -c "python manage.py test"
```

## Linting
Linting is important for maintaining code quality and consistency. We use flake8 for linting. You can run the linting checks with the following command:
```sh
docker-compose run --rm app sh -c "flake8"
```
