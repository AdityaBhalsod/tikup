### Description

This is a video streaming application similiar to Tiktok.

### Tech-stack for backend.

1. Django
2. PostgreSQL + MongoDB (currently SQLite for base development purpose)
3. Redis (for caching - popular videos)
4. RabbitMQ (for notifications)
5. RESTful API

### Local Setup

1. Clone this repository
2. Create virtual environment for this project.
3. Activate the virtual environment.
4. Store env variables for the project (neglect this).
5. `pip install requirements.txt` - install all dependencies.
6. `python manage.py migrate` - make database migrations and update tables.
7. `python manage.py runserver` - runs the backend server for application.
8. Fire up the browser and visit `127.0.0.1:8000/admin`