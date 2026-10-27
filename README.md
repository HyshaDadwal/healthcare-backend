# Healthcare Backend API

A Django REST Framework application for managing patients, doctors, and patient–doctor assignments. The application uses PostgreSQL for data storage and JWT authentication to secure API endpoints.

## Technologies Used

- Python
- Django
- Django REST Framework
- PostgreSQL
- Simple JWT
- python-dotenv

## Features

- User registration and login using email and password
- JWT-based authentication
- Patient creation, retrieval, updating, and deletion
- Doctor creation, retrieval, updating, and deletion
- Patient–doctor assignment management
- Patient ownership restrictions
- Doctor modification and deletion restricted to the doctor creator
- Duplicate patient–doctor assignment prevention
- Environment-based configuration for sensitive settings

## Setup Instructions

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd healthcare-backend
```

### 2. Create and activate a virtual environment

On Windows PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root and configure the database settings expected by `config/settings.py`.

Example:

```env
SECRET_KEY=replace-with-a-secure-secret-key
DEBUG=True
DB_NAME=healthcare_db
DB_USER=healthcare_user
DB_PASSWORD=replace-with-your-local-database-password
DB_HOST=localhost
DB_PORT=5432
```

Use your actual local PostgreSQL credentials. Never commit `.env` to GitHub.

### 5. Create the PostgreSQL database

Create a PostgreSQL database named `healthcare_db`, or use the database name configured in your `.env` file.

Ensure PostgreSQL is running and the configured database user has the necessary permissions.

### 6. Apply migrations

```powershell
python manage.py migrate
```

### 7. Start the development server

```powershell
python manage.py runserver
```

The API will be available at `http://127.0.0.1:8000/`.

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/auth/register/` | Register a user |
| POST | `/api/auth/login/` | Obtain JWT tokens |
| POST | `/api/auth/token/refresh/` | Refresh an access token |
| GET, POST | `/api/patients/` | List or create patients |
| GET, PUT, PATCH, DELETE | `/api/patients/<id>/` | Retrieve, update, or delete a patient |
| GET, POST | `/api/doctors/` | List or create doctors |
| GET, PUT, PATCH, DELETE | `/api/doctors/<id>/` | Retrieve, update, or delete a doctor |
| GET, POST | `/api/mappings/` | List or create patient–doctor assignments |
| GET | `/api/mappings/<patient_id>/` | List assignments for a patient |
| DELETE | `/api/mappings/<mapping_id>/` | Delete an assignment |

Protected endpoints require a valid JWT access token in the Authorization header:

`Authorization: Bearer <access_token>`

## Security

- Passwords are managed using Django's password-hashing mechanisms.
- JWT authentication protects API endpoints.
- Patients are restricted to their respective owners.
- Doctors can be viewed by authenticated users, while updates and deletions are restricted to their creators.
- Patient–doctor assignments are restricted to patients owned by the authenticated user.
- Environment variables are used for sensitive configuration.

## Testing

Run the following commands:

```powershell
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py migrate
```

API endpoints can be tested using Postman.

## Database

PostgreSQL is used as the application's relational database.