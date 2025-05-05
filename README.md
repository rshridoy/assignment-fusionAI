# Country Fusion

A Django application for displaying country information fetched from the REST Countries API.

## Features

- RESTful API for country information
- Simple web interface to browse countries
- Authentication for API access
- Country search functionality 
- View countries by region and language

## Installation

### Prerequisites

- Python 3.9+
- pip

### Setup Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/rshridoy/assignment-fusionAI.git
   cd country_fusion
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Set up the database:
   ```bash
   python manage.py migrate
   ```

6. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

7. Load sample users (optional):
   ```bash
   python manage.py loaddata countries/fixtures/users.json
   ```

8. Fetch country data:
   ```bash
   python manage.py fetch_countries
   ```

## Running the Application

1. Start the development server:
   ```bash
   python manage.py runserver
   ```

2. Access the application:
   - Web interface: http://localhost:8000/
   - Admin interface: http://localhost:8000/admin/
   - API: http://localhost:8000/api/countries/

## API Endpoints

- `GET /api/countries/` - List all countries
- `GET /api/countries/<id>/` - Get a specific country
- `POST /api/countries/` - Create a new country
- `PUT /api/countries/<id>/` - Update a country
- `DELETE /api/countries/<id>/` - Delete a country
- `GET /api/countries/<id>/region/` - Get countries in the same region
- `GET /api/countries/language/<language>/` - Get countries that speak a specific language
- `GET /api/countries/search/<query>/` - Search countries by name

## Technologies Used

- Django
- Django REST Framework
- Bootstrap
- SQLite (default database)
