# Student Records API

## Project Description
This project uses a REST API for managing system records for university students. The API provides 7 endpoints (5 CRUD + 2 filtering) that allows users to create, read, update, and delete student records, as well as filter by major or a GPA threshold. Each endpoint provides proper HTTP status codes and have input validation with explicit checks that raise `HTTPException`s. Uses an SQLite database for data storage and persists across server restarts.

## Installation Instructions
1. Clone this repository to your computer:
```bash
git clone "https://github.com/alexb544/rest-api-project.git"
```

2. Create and activate a new virtual environment for the project:
```bash
python -m venv .venv
source .venv/Scripts/activate 
```

3. Install any project dependencies from `requirements.txt`:
```bash
pip install -r requirements.txt
```
You can verify installation via: `pip list | grep fastapi` & `uvicorn --version`

 4. Run the server:
```bash
uvicorn main:app --reload
```
Click on the link provided after the server starts ``, this opens a new webpage in your browser. 
- Add `/docs` to the end of the URL to go to FastAPI's user friendly page. 

## API Endpoints
List all endpoints with:
- HTTP method
- URL path
- Description
- Status codes

## Testing Instructions
- How to test the API (FastAPI's `/docs` interface recommended)
- Note about database initialization

## Example Usage
Three example requests demonstrating different operations
1. 
2. 
3. 
