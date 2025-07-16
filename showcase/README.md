# Showcase Web Application

This application is a simple Flask-based web server designed to showcase a portfolio of artworks, including a developmental trail for each piece and selectable frames.

## Running with Docker (Recommended)

This application is designed to be run inside a Docker container.

### Prerequisites

*   [Docker](https://docs.docker.com/get-docker/) installed on your system.

### Build the Docker Image

1.  **Navigate to the project's root directory:**
    Open your terminal or command prompt. Make sure you are in the main project directory that contains the `showcase` folder (i.e., you should see `showcase/` if you type `ls`).

2.  **Build the image:**
    Run the following command. This tells Docker to build an image using the `Dockerfile` it finds inside the `showcase` directory.
    ```bash
    docker build -t showcase-app showcase/
    ```
    *   `-t showcase-app`: Tags the image with the name `showcase-app`.
    *   `showcase/`: This is the build context. It tells Docker to look for the `Dockerfile` inside the `showcase` directory and to send the contents of that directory to the Docker daemon.

### Run the Docker Container

1.  **Run the container:**
    Once the image is built successfully, run the following command to start a container from the image:
    ```bash
    docker run -p 5001:5000 showcase-app
    ```
    *   `-p 5001:5000`: This maps port `5001` on your host machine to port `5000` inside the Docker container (where the Flask app is running). You can change `5001` to any other available port on your host if needed (e.g., `-p 8080:5000`).
    *   `showcase-app`: The name of the image to run.

2.  **Access the application:**
    Open your web browser and navigate to:
    ```
    http://localhost:5001
    ```
    (If you used a different host port in the `docker run` command, replace `5001` with that port number).

### Stopping the Container

1.  To find the ID of your running container, you can use:
    ```bash
    docker ps
    ```
2.  Then, to stop the container, use:
    ```bash
    docker stop <container_id_or_name>
    ```

## Development (Alternative - Running directly with Flask)

If you prefer to run the Flask development server directly without Docker (e.g., for quick local development):

1.  **Navigate to the `showcase` directory:**
    ```bash
    cd showcase
    ```
2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Run the Flask app:**
    ```bash
    flask run --host=0.0.0.0 --port=5000
    ```
5.  Access the application at `http://localhost:5000`.

Remember to deactivate the virtual environment when you're done:
```bash
deactivate
```
