# Module 3: Databases (Due: 2025-06-08 23:59:00)
**Authored by:** Jonathan Wu *(jwu146)*

## Quick Start
This project uses **uv** for dependency management, but a `requirements.txt` file is also provided

### Using **uv**:

1. Install **uv** (see [uv documentation](https://docs.astral.sh/uv/getting-started/installation/) for installation instructions).  

2. To sync the project's dependencies with the environment, from the project root, run:
   ```bash
   uv sync
   ```

3. To create and load data into the database, from the project root, run:
    ```bash
    uv run load_data.py
    ```

4. To get answers to the questions listed in the assignment, from the project root, run:
    ```bash
    uv run query_data.py
    ```

5. To see the flask page, run:
    ```bash
    uv run app.py
    ```
-----

### Using **pip** and `requirements.txt`:

1. To sync the project's dependencies using `requirements.txt`, run:
    ```bash
    pip install -r requirements.txt
    ```

2. To create and load data into the database, from the project root, run:
    ```bash
    python load_data.py
    ```

3. To get answers to the questions listed in the assignment, from the project root, run:
    ```bash
    python query_data.py
    ```

4. To see the flask page, run:
    ```bash
    python app.py
    ```

-----

The default save location for `applicant_data.json` file is in `/data`, and is what the script expects to retreive the data for database creation and queries.


## How to Run

**Default values for all arguments are provided:**

* `--db_name=postgres`
* `--db_user=postgres`
* `--db_password=12345`
* `--db_host=localhost`
* `--db_port=5432`

You can override these defaults as needed for your own database environment (PostgreSQL).


### 1. **Load Data Into the Database**

Before running queries, ensure your `applicant_data.json` file is in the `data/` directory.

Run the following command to create the table and load the data (you can provide your own database credentials if needed):

If using pip:

    ```bash
    python load_data.py --db_name=your_db --db_user=your_user --db_password=your_password --db_host=localhost --db_port=5432
    ```

If using uv:

    ```bash
    uv run load_data.py --db_name=your_db --db_user=your_user --db_password=your_password --db_host=localhost --db_port=5432
    ```

### 2. **Query the Data**

If using pip:

    ```bash
    python query_data.py --db_name=your_db --db_user=your_user --db_password=your_password --db_host=localhost --db_port=5432
    ```

If using uv:

    ```bash
    uv run query_data.py --db_name=your_db --db_user=your_user --db_password=your_password --db_host=localhost --db_port=5432
    ```

This script will connect to your database and print answers to the assignment questions. The queries are organized in separate functions for clarity and ease of extension.

### 3. **See Queries in Flask Page**

If using pip:

    ```bash
    python app.py
    ```

If using uv:

    ```bash
    uv run app.py
    ```

## Other Notes
Both query rationale and limitations essay are included in the `limitations.pdf` document in the project's root directory.