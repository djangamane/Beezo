
# Warrior Intel

A scouting application for the University of Arizona Men's Basketball team.

## Setup

1.  **Install Dependencies:**

    ```bash
    pip install fastapi uvicorn sqlalchemy
    # You will also need to have R installed to run the R scripts.
    ```

2.  **Seed the database:**

    ```bash
    python seed.py
    ```

3.  **Run the backend server:**

    ```bash
    uvicorn backend.main:app --reload
    ```

4.  **Run the frontend server:**

    In a separate terminal, navigate to the `frontend` directory and run a simple web server.

    ```bash
    cd frontend
    python -m http.server
    ```

5.  **Access the application:**

    Open your web browser and go to `http://localhost:8000`.

