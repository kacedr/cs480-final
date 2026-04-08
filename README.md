# CS 480 Final Project

A terminal-based application for 480 final project built with Python and PostgreSQL.

## Team

- Kyle Gleason
- Dan Grosch
- James Nguyen
- Mandar Patel

## Stack 
(please feel free to change if needed)
- Python 3
- PostgreSQL
- psycopg (Postgres driver)
- python-dotenv (env var loading)
- tabulate (pretty terminal tables)

## Prerequisites

You need PostgreSQL and Python 3 installed locally.

### macOS (Homebrew)

    brew install postgresql
    brew services start postgresql

### Ubuntu / Debian

    sudo apt update
    sudo apt install postgresql postgresql-contrib python3-venv
    sudo service postgresql start

### Windows

Install Postgres from https://www.postgresql.org/download/windows/ and make sure psql is on your PATH. You will likely need a password in your DATABASE_URL.

## Setup

Clone the repo and cd into it:

    git clone <repo-url>
    cd cs480-final

Create and activate a virtual environment:

    python3 -m venv .venv
    source .venv/bin/activate

On Windows the activate command is .venv\Scripts\activate.

Install dependencies:

    pip install -r requirements.txt

Copy the example env file and edit it with your local Postgres credentials:

    cp .env.example .env

Open .env and set DATABASE_URL to match your local setup. On macOS it usually looks like:

    DATABASE_URL=postgresql://yourusername@localhost:5432/cs480final

## Database setup

Create the database and load the schema and seed data:

    ./db/reset.sh

This drops the database if it exists, recreates it, and loads db/schema.sql followed by db/seed.sql. Run it any time you want a clean slate.

If the script fails on permissions, run chmod +x db/reset.sh first.

## Running the app

From the project root with your venv activated:

    python -m app.main

You should see the main menu. Use the number keys to navigate.

## Project structure

    cs480-final/
    ├── README.md
    ├── .gitignore
    ├── .env.example          # template, safe to commit
    ├── .env                  # don't commit
    ├── requirements.txt
    ├── app/
    │   ├── __init__.py
    │   ├── main.py           # entry point and menu loop
    │   ├── db.py             # connection helper
    │   └── queries.py        # all SQL operations
    ├── db/
    │   ├── schema.sql        # CREATE TABLE statements
    │   ├── seed.sql          # sample data
    │   └── reset.sh          # drop, recreate, reload
    └── docs/
        └── ERD.png           # entity relationship diagram

## Workflow
- All SQL queries live in app/queries.py. Keep them out of main.py.
- When you change the schema, update db/schema.sql and rerun ./db/reset.sh.
- Commit your changes on main (try not to brick the code).
## Git workflow
    git pull 
    # make changes
    git add .
    git commit -m "Short description of change"
    git push

## Please Please Please Please
please `git pull` before making changes to prevent merge conflicts :smiley:  

