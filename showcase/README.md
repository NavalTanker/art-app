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

## Customizing Content

### Gallery Background

You can add a custom background to the showcase gallery wall.

1.  Find an image you want to use as the background.
2.  Name it `showcase_background.jpg` (or `.png`, or `.gif`).
3.  Place this file inside the `showcase/static/images/` directory.
4.  If running in Docker, rebuild your image and run the container. The app will automatically detect and use your custom background.

### Artwork Descriptions

You can add custom descriptions for each stage of a gallery by creating a single text file in the gallery's main folder.

1.  Create a new file named `descriptions.txt` inside a gallery folder (e.g., `showcase/static/galleries/gallery-1/descriptions.txt`).
2.  In this file, each line corresponds to a stage. The first line is the description for Stage 1, the second line is for Stage 2, and so on.

**Example `descriptions.txt`:**
```
This is the initial sketch for my new piece.
Here I've blocked in the main colors.
This is the final, detailed artwork.
```

If this file is not present, or if it has fewer lines than there are stages, the application will use a default description for the remaining stages.

## Setting Up Supabase for Authentication

This project uses Supabase for user authentication. You will need to create a free Supabase project and provide its credentials to the application via environment variables.

### 1. Create a Supabase Project

1.  Go to [supabase.com](https://supabase.com/) and sign up or log in.
2.  Create a new project. You can use the free tier.
3.  Once your project is created, go to the **Project Settings** (the gear icon in the left sidebar).
4.  In the settings menu, click on **API**.

### 2. Find Your Credentials

On the API settings page, you will find:

*   **Project URL**: Under the "Project URL" section.
*   **Project API Keys**: Under this section, find the `anon` `public` key. This is your public-facing "anon key".

You will also need a **Flask Secret Key** for session management. This can be any long, random string of your choice.

### 3. Create a `.env` File

For a much easier and more secure setup, you will use an environment file (`.env`) to store your keys.

1.  In the **root directory** of the project (the same folder that contains the `showcase/` directory), create a new file named `.env`.
2.  Copy the template below and paste it into your new `.env` file.
3.  Replace the placeholder text with your actual credentials from the Supabase dashboard.

**`.env` file template:**
```
# Supabase Credentials
SUPABASE_URL="YOUR_SUPER_LONG_SUPABASE_URL"
SUPABASE_KEY="YOUR_VERY_LONG_SUPABASE_ANON_KEY"

# Flask Secret Key - can be any long, random string
FLASK_SECRET_KEY="YOUR_SUPER_SECRET_RANDOM_STRING"
```

**Important:** The `.env` file should **never** be committed to version control (a `.gitignore` file would typically be used to prevent this).

### 4. Run the Application

#### For Docker (Recommended)

Now you can run the container using the `--env-file` flag. This command securely passes all the keys from your `.env` file to the container.

**IMPORTANT: This command must be run from the project's root directory** (the same folder where you created the `.env` file and where you see the `showcase/` directory).

```bash
docker run --env-file ./.env -p 5001:5000 showcase-app
```
*Note: The image name is `showcase-app`, not `showcase-ap`.*

#### For Local Development

Because the app now uses `python-dotenv`, you no longer need to `export` or `set` the variables manually. Simply run the app, and it will automatically load them from your `.env` file.

1.  Navigate to the `showcase` directory: `cd showcase`
2.  Run the app: `flask run`

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
