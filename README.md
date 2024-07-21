# Weather App

Weather App is a Django-based web application that allows users to search for the weather in various cities and view the search history. It also provides an API endpoint to get the number of searches for each city.

## Features

- Search for the weather in different cities
- View search history
- API endpoint to get the number of searches for each city

## Requirements

- Python 3.12
- Django 5.0.7
- Requests 2.32.3
- Django REST Framework 3.15.2

## Installation

1. **Clone the repository:**

    
bash
    git clone https://github.com/Cur1yB/weather-app.git
    cd weather-app


2. **Install dependencies using Poetry:**

    
bash
    poetry install


3. **Activate the virtual environment:**

    
bash
    poetry shell


4. **Apply migrations:**

    
bash
    make migrate


## Usage

1. **Run the development server:**

    
bash
    make runserver


    The application will be available at http://127.0.0.1:8000/.

2. **Run tests:**

    
bash
    make testing


## API

### Get Search Count for Cities

- **Endpoint:** /api/search-count/
- **Method:** GET
- **Description:** Returns the number of searches for each city.

Example response:

json
[
    {"city": "Moscow", "search_count": 5},
    {"city": "London", "search_count": 3}
]

## Makefile Commands

- **runserver**: Start the development server.
- **migrate**: Create and apply migrations.
- **testing**: Run the tests.

## Contact

If you have any questions, please feel free to contact me at alexandr.ignatev1996@gmail.com.
