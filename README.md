Healthcare Backend (Django REST API)
Simple backend for healthcare management with user auth, patients, doctors, and patient-doctor mapping.

Features:
JWT auth (register, login, refresh)
CRUD for patients & doctors
Assign doctors to patients
PostgreSQL ready (using Neon DB)
Django admin support

Setup
# clone project & go inside
cd healthcare

# activate venv
.\.venv\Scripts\activate   # windows

# run server
python manage.py runserver

For admin panel:
python manage.py createsuperuser
Visit: http://localhost:8000/admin/

API Endpoints
Auth
POST /api/auth/register/
POST /api/auth/login/
POST /api/auth/token/refresh/

Patients (auth required)
GET/POST /api/patients/
GET/PUT/DELETE /api/patients/<id>/

Doctors
GET/POST /api/doctors/
GET/PUT/DELETE /api/doctors/<id>/
GET /api/doctors/specializations/

Mappings
POST /api/mappings/ (assign doctor to patient)
GET /api/mappings/
GET /api/mappings/<patient_id>/
PUT/DELETE /api/mappings/detail/<id>/
GET /api/mappings/status-choices/

DB
Dev → SQLite
Prod → PostgreSQL (.env file has DATABASE_URL)

Project Structure
healthcare/
 ├── authentication/  # auth
 ├── patients/        # patients
 ├── doctors/         # doctors
 ├── mappings/        # patient-doctor mapping
 └── healthcare_project/  # settings, urls
