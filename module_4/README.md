# Module 4: Pytest and Sphinx (Due: 2025-06-15 23:59:00)
**Authored by:** Jonathan Wu *(jwu146)*

## Quick Start
This project uses **uv** for dependency management, but a `requirements.txt` file is also provided for pip.

### Using **uv**:

1. Install **uv** (see [uv documentation](https://docs.astral.sh/uv/getting-started/installation/) for installation instructions).

2. To sync the project's dependencies with the environment, from the project root, run:

   ```bash
   uv sync
   ```

---

### Using **pip** and `requirements.txt`:

1. To install dependencies using `requirements.txt`, run:

   ```bash
   pip install -r requirements.txt
   ```

---

## Running Tests

To run all tests with pytest:

```bash
pytest
```

To run only pizza-related tests:

```bash
pytest -m pizza
```

To run only order-related tests:

```bash
pytest -m order
```

To run integration-related tests:

```bash
pytest -m "pizza and order"
```

---

## Overview

This project implements a pizza ordering system as described in the assignment. There are two core modules: `pizza` and `order`, along with a comprehensive set of unit and integration tests using pytest. Documentation is generated using Sphinx and is available online.

## Project Structure

* `src/`: Contains the source code (`order.py`, `pizza.py`)
* `tests/`: Contains all unit and integration tests
* `pytest.ini`: Pytest configuration for test markers
* `requirements.txt`: Project dependencies (pip)
* `pyproject.toml`: Project dependencies (uv)
* `README.md`: This file

## Cost Table

Pizza prices are calculated using the following variables:

* **Crust:** Thin (\$5), Thick (\$6), Gluten Free (\$8)
* **Sauce:** Marinara (\$2), Pesto (\$3), Liv Sauce (\$5)
* **Topping:** Pineapple (\$1), Pepperoni (\$2), Mushrooms (\$3)
* **Cheese:** Mozzarella (always included)

---

## Documentation

Read the documentation here:
[https://jwu146-module-4.readthedocs.io/en/latest/](https://jwu146-module-4.readthedocs.io/en/latest/)

Sphinx-generated HTML can also be found locally under `./build/html/index.html` after building the docs.

---