# Task Manager API

A simple Python backend API built with FastAPI and SQLite.

## Features
- Create tasks
- List tasks
- Mark tasks as complete
- Delete tasks
- Store tasks in SQLite

## Technologies
- Python
- FastAPI
- SQLite
- Uvicorn

## How to run

```bash
python -m venv venv
venv\Scripts\activate
pip install fastapi uvicorn
uvicorn main:app --reload
