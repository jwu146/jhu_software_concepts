# Web Applications

## Quick Start
This project uses **uv** for dependency management, but a `requirements.txt` file is also provided

### Using **uv**:

1. Install **uv** (see [uv documentation](https://docs.astral.sh/uv/getting-started/installation/) for installation instructions).  

2. To sync the project's dependencies with the environment, from the project root, run:
   ```bash
   uv sync
   ```

3. To run the project, from the project root, run:
    ```bash
    uv run run.py
    ```

-----

### Using **pip** and `requirements.txt`:

1. To sync the project's dependencies using `requirements.txt`, run:
    ```bash
    pip install -r requirements.txt
    ```

2. To run the project, from the project root, run:
    ```bash
    python run.py
    ```

-----

With the environment setup, open [http://localhost:8000](http://localhost:8000) in your browser to view the web application.



## References used: 

* [Real Python: Flask Project Setup](https://realpython.com/flask-project/)