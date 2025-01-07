# SDA Hymns API

This is a FastAPI application with an SQLite database for viewing SDA hymns.

## Features

- View a list of most SDA hymns (currently) with additional information.

  Parameters: `q (optional)`, `cateogries (optional)`, `limit )(default=100)`, `offset (default=0)`

  For example:

  - The key it is played in
  - The author
  - Date of publication
  - and more

- Retrieve details of a specific hymn by hymn nu

## Requirements

- Python 3.7+
- FastAPI
- SQLite

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/dev-murphy/sda-hymns-api.git
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
