# SDA Hymns API

This is a FastAPI application with an SQLite database for viewing SDA hymns.

## Features

- View a list of SDA hymns
- Retrieve details of a specific hymn by ID

## Requirements

- Python 3.7+
- FastAPI
- SQLite

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/sda-hymns-api.git
   cd sda-hymns-api
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:
   ```bash
   uvicorn main:app --reload
   ```

## Usage

- Open your browser and navigate to `http://127.0.0.1:8000/docs` to access the interactive API documentation.

## Project Structure

- `main.py`: The main entry point of the application.
- `hymns.db`: The sqlite database with hymn information

## License

This project is licensed under the MIT License.
