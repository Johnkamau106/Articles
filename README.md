# Articles Code Challenge

## Overview

This project models the relationships between Authors, Articles, and Magazines using Python and SQLite.  
- An Author can write many Articles  
- A Magazine can publish many Articles  
- Each Article belongs to one Author and one Magazine  

## Setup

1. Create and activate a virtual environment:

```bash
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
Install dependencies:

bash
Copy
Edit
pip install pytest sqlite3
Set up the database:

bash
Copy
Edit
python scripts/setup_db.py
Seed the database with sample data:

bash
Copy
Edit
python -m lib.db.seed
Testing
Run all tests with:

bash
Copy
Edit
pytest
Project Structure
lib/models/ — Python classes for Authors, Articles, and Magazines

lib/db/ — Database connection, schema, and seed data

tests/ — Test cases for each model

scripts/ — Database setup and example query scripts

Author
John Kamau