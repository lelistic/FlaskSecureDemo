# FlaskSecureDemo

FlaskSecureDemo is an example project designed to demonstrate how to develop a Flask application using the `flask-security-too` library for security features like authentication, authorization, and more. This project utilizes Docker Compose to simplify the setup and management of the development environment.

## Features

- Flask application setup with `flask-security-too`
- Integration with PostgreSQL database
- Docker Compose configuration for easy development and deployment
- Hot-reloading for Flask development server
- Example templates to showcase usage

## Prerequisites

Before you begin, ensure you have the following installed on your system:

- Docker
- Docker Compose

## Getting Started

Follow these steps to get the FlaskSecureDemo project up and running.

### Clone the Repository

```bash
git clone https://github.com/your-username/FlaskSecureDemo.git
cd FlaskSecureDemo
```

### Directory Structure

The project directory structure is as follows:

```
FlaskSecureDemo/
├── docker-compose.yml
├── web/
│   ├── Dockerfile.dev
│   ├── app.py
│   ├── requirements.txt
│   └── webapp/
│       ├── __init__.py
│       ├── templates/
│       └── ...
└── ...
```

### Docker Compose Configuration

The `docker-compose.dev.yml` file includes the configuration for both the Flask application and the PostgreSQL database.


### Build and Run

To build and run the application using Docker Compose, execute the following command in the project root:

```bash
docker compose -f docker-compose.dev.yml up --build
```

This command will build the Docker images and start the services defined in the `docker-compose.dev.yml` file.

### Accessing the Application

Once the services are running, you can access the Flask application in your web browser at:

```
http://localhost:8888
```

The PostgreSQL database will be accessible at `localhost:5433`.

### Stopping the Services

To stop the running services, press `Ctrl+C` in the terminal where the services are running. Alternatively, you can run:

```bash
docker compose -f docker-compose.dev.yml down
```

## Rebuild and Run

To rebuild the Docker images and restart the services using the `rebuild.sh` script, execute the following command in the project root:

```bash
./rebuild.sh
```

The `rebuild.sh` script is a shell script used to streamline the process of stopping, rebuilding, and starting the Docker services defined in the `docker-compose.dev.yml` file. The script:

1. stops and removes all the containers, networks, and volumes defined in the `docker-compose.dev.yml` file. It's equivalent to stopping the services and cleaning up any resources associated with them.

2. forcefully removes the Docker image named `lelis-web`. This ensures that the image will be rebuilt from scratch during the next `up` command, rather than using a potentially outdated cached version.

3. builds and starts the services defined in the `docker-compose.dev.yml` file in detached mode (`-d`). The `--build` flag forces a rebuild of the Docker images before starting the containers.

4. shows the logs of all the services defined in the `docker-compose.dev.yml` file, allowing you to see the output and any potential issues during startup.

By using this script, you ensure that your application is running with the latest changes and can quickly identify any issues during startup.


## Usage

This project includes an example Flask application configured with `flask-security-too`. You can extend and modify it to suit your needs.

- Add routes, templates, and static files as required.
- Customize the security settings in the Flask configuration.
- Use the PostgreSQL database for storing and retrieving data.

## Contributing

Contributions are welcome! If you have any suggestions, improvements, or bug fixes, please create a pull request or open an issue on GitHub.
Happy coding! 

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Flask](https://flask.palletsprojects.com/)
- [flask-security-too](https://flask-security-too.readthedocs.io/)
- [Docker](https://www.docker.com/)
- [PostgreSQL](https://www.postgresql.org/)

