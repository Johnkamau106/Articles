# Articles Project

A Python project for managing articles, authors, and magazines using a simple database-backed model.

## Project Structure

```
code-challenge/
  lib/
    models/
      author.py
      # ... other model files
    controllers/
    db/
    debug.py
  scripts/
    run_queries.py
    setup_db.py
  tests/
    test_article.py
    test_author.py
    test_magazine.py
README.md
```

## Features

- Manage authors, articles, and magazines
- Database-backed models
- CRUD operations for each model
- Unit tests for core functionality

## Setup

1. **Clone the repository**
2. **Create a virtual environment**
   ```sh
   python3 -m venv env
   source env/bin/activate
   ```
3. **Install dependencies**
   ```sh
   pip install -r requirements.txt
   ```
4. **Set up the database**
   ```sh
   python code-challenge/scripts/setup_db.py
   ```

## Running

- To run queries or interact with the database:
  ```sh
  python code-challenge/scripts/run_queries.py
  ```

## Testing

- To run all tests:
  ```sh
  pytest code-challenge/tests/
  ```

## License

This project is licensed under the MIT License.

---

Feel free to contribute or open issues!