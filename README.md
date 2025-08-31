# Healthcare Backend - Django REST API

A comprehensive Django REST API backend for healthcare management, featuring user authentication, patient management, doctor profiles, and patient-doctor assignments.

## 🚀 Features

- **JWT Authentication** - Secure user registration and login
- **Patient Management** - CRUD operations for patient records
- **Doctor Management** - CRUD operations for doctor profiles
- **Patient-Doctor Mapping** - Assign doctors to patients
- **PostgreSQL Support** - Ready for production with Neon DB
- **RESTful API Design** - Following REST conventions
- **Comprehensive Validation** - Data validation and error handling
- **Admin Interface** - Django admin for easy management

## 📋 Requirements

- Python 3.8+
- Django 4.2.7
- Django REST Framework
- PostgreSQL (for production)

## ⚡ Quick Start

### 1. Setup Environment

```bash
# Navigate to the project directory
cd d:\healthcare

# Activate the virtual environment
.\.venv\Scripts\activate  # Windows
```

### 2. Run the Application

```bash
# Start the development server
python manage.py runserver
```

Your application is now running with PostgreSQL and ready for production use!

### 3. Create Admin User (Optional)

To access the Django admin interface:

```bash
python manage.py createsuperuser
```

Then visit `http://localhost:8000/admin/` to manage your data.

## 🔧 API Endpoints

### Authentication
- `POST /api/auth/register/` - Register new user
- `POST /api/auth/login/` - Login user  
- `POST /api/auth/token/refresh/` - Refresh JWT token

### Patients (Authenticated users only)
- `GET /api/patients/` - List all patients
- `POST /api/patients/` - Create new patient
- `GET /api/patients/<id>/` - Get patient details
- `PUT /api/patients/<id>/` - Update patient
- `DELETE /api/patients/<id>/` - Delete patient

### Doctors
- `GET /api/doctors/` - List all doctors
- `POST /api/doctors/` - Create new doctor
- `GET /api/doctors/<id>/` - Get doctor details
- `PUT /api/doctors/<id>/` - Update doctor
- `DELETE /api/doctors/<id>/` - Delete doctor
- `GET /api/doctors/specializations/` - Get specialization options

### Patient-Doctor Mappings
- `GET /api/mappings/` - List all mappings
- `POST /api/mappings/` - Create new mapping
- `GET /api/mappings/<patient_id>/` - Get doctors for patient
- `PUT /api/mappings/detail/<id>/` - Update mapping
- `DELETE /api/mappings/detail/<id>/` - Delete mapping
- `GET /api/mappings/status-choices/` - Get status options

## 📖 Complete API Documentation

**Base URL:** `http://localhost:8000`

### 🔐 Authentication APIs

#### 1. Register User
**POST** `/api/auth/register/`

**Headers:**
```
Content-Type: application/json
```

**Request Body:**
```json
{
    "username": "your_username",
    "email": "your_email@example.com",
    "password": "your_password",
    "password_confirm": "your_password",
    "first_name": "Your First Name",
    "last_name": "Your Last Name"
}
```

**Response (201 Created):**
```json
{
    "message": "User registered successfully",
    "user": {
        "id": 1,
        "username": "your_username",
        "email": "your_email@example.com",
        "first_name": "Your First Name",
        "last_name": "Your Last Name",
        "date_joined": "2025-08-30T18:00:00Z"
    },
    "tokens": {
        "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
        "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
    }
}
```

#### 2. Login User
**POST** `/api/auth/login/`

**Headers:**
```
Content-Type: application/json
```

**Request Body:**
```json
{
    "username": "your_username",
    "password": "your_password"
}
```

**Response (200 OK):**
```json
{
    "message": "Login successful",
    "user": {
        "id": 1,
        "username": "your_username",
        "email": "your_email@example.com",
        "first_name": "Your First Name",
        "last_name": "Your Last Name",
        "date_joined": "2025-08-30T18:00:00Z"
    },
    "tokens": {
        "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
        "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
    }
}
```

#### 3. Refresh Token
**POST** `/api/auth/token/refresh/`

**Headers:**
```
Content-Type: application/json
```

**Request Body:**
```json
{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

---

### 👤 Patient Management APIs

**⚠️ All patient endpoints require authentication. Include this header:**
```
Authorization: Bearer YOUR_ACCESS_TOKEN
```

#### 1. Create Patient
**POST** `/api/patients/`

**Headers:**
```
Content-Type: application/json
Authorization: Bearer YOUR_ACCESS_TOKEN
```

**Request Body:**
```json
{
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com",
    "phone": "+1234567890",
    "date_of_birth": "1985-05-15",
    "gender": "M",
    "address": "123 Main St, Apt 4B",
    "city": "New York",
    "state": "NY",
    "zip_code": "10001",
    "blood_group": "O+",
    "allergies": "Peanuts, Shellfish",
    "medical_history": "Previous heart surgery in 2020"
}
```

**Gender Options:** `M` (Male), `F` (Female), `O` (Other)

**Response (201 Created):**
```json
{
    "message": "Patient created successfully",
    "patient": {
        "id": 1,
        "first_name": "John",
        "last_name": "Doe",
        "full_name": "John Doe",
        "email": "john.doe@example.com",
        "phone": "+1234567890",
        "date_of_birth": "1985-05-15",
        "gender": "M",
        "address": "123 Main St, Apt 4B",
        "city": "New York",
        "state": "NY",
        "zip_code": "10001",
        "blood_group": "O+",
        "allergies": "Peanuts, Shellfish",
        "medical_history": "Previous heart surgery in 2020",
        "created_by": "your_username",
        "created_at": "2025-08-30T18:00:00Z",
        "updated_at": "2025-08-30T18:00:00Z"
    }
}
```

#### 2. List All Patients
**GET** `/api/patients/`

**Headers:**
```
Authorization: Bearer YOUR_ACCESS_TOKEN
```

**Response (200 OK):**
```json
{
    "count": 2,
    "patients": [
        {
            "id": 1,
            "first_name": "John",
            "last_name": "Doe",
            "full_name": "John Doe",
            "email": "john.doe@example.com",
            "phone": "+1234567890",
            "date_of_birth": "1985-05-15",
            "gender": "M",
            "created_at": "2025-08-30T18:00:00Z"
        }
    ]
}
```

#### 3. Get Patient Details
**GET** `/api/patients/<patient_id>/`

**Example:** `GET /api/patients/1/`

**Headers:**
```
Authorization: Bearer YOUR_ACCESS_TOKEN
```

#### 4. Update Patient
**PUT** `/api/patients/<patient_id>/`

**Headers:**
```
Content-Type: application/json
Authorization: Bearer YOUR_ACCESS_TOKEN
```

**Request Body (Partial Update):**
```json
{
    "phone": "+1987654321",
    "allergies": "Peanuts, Shellfish, Eggs"
}
```

#### 5. Delete Patient
**DELETE** `/api/patients/<patient_id>/`

**Headers:**
```
Authorization: Bearer YOUR_ACCESS_TOKEN
```

**Response (204 No Content):**
```json
{
    "message": "Patient John Doe deleted successfully"
}
```

---

### 👨‍⚕️ Doctor Management APIs

#### 1. Create Doctor
**POST** `/api/doctors/`

**Headers:**
```
Content-Type: application/json
Authorization: Bearer YOUR_ACCESS_TOKEN
```

**Request Body:**
```json
{
    "first_name": "Sarah",
    "last_name": "Johnson",
    "email": "dr.sarah@hospital.com",
    "phone": "+1555123456",
    "license_number": "MD123456789",
    "specialization": "cardiology",
    "experience_years": 10,
    "qualification": "MD, Cardiology, Johns Hopkins",
    "hospital_name": "City General Hospital",
    "hospital_address": "456 Hospital Ave, Medical District",
    "city": "New York",
    "state": "NY",
    "consultation_fee": 250.00,
    "availability": "Mon-Fri 9AM-5PM, Sat 9AM-1PM",
    "bio": "Experienced cardiologist specializing in heart surgery and cardiac care."
}
```

**Specialization Options:**
- `cardiology` - Cardiology
- `dermatology` - Dermatology
- `endocrinology` - Endocrinology
- `gastroenterology` - Gastroenterology
- `general_medicine` - General Medicine
- `neurology` - Neurology
- `oncology` - Oncology
- `orthopedics` - Orthopedics
- `pediatrics` - Pediatrics
- `psychiatry` - Psychiatry
- `radiology` - Radiology
- `surgery` - Surgery
- `urology` - Urology
- `other` - Other

#### 2. List All Doctors
**GET** `/api/doctors/`

**Headers:**
```
Authorization: Bearer YOUR_ACCESS_TOKEN
```

**Query Parameters (Optional):**
- `specialization` - Filter by specialization: `/api/doctors/?specialization=cardiology`
- `city` - Filter by city: `/api/doctors/?city=New York`

#### 3. Get Doctor Details
**GET** `/api/doctors/<doctor_id>/`

#### 4. Update Doctor
**PUT** `/api/doctors/<doctor_id>/`

**Note:** Only the creator can update their own doctors.

#### 5. Delete Doctor
**DELETE** `/api/doctors/<doctor_id>/`

**Note:** Only the creator can delete their own doctors.

#### 6. Get Specializations
**GET** `/api/doctors/specializations/`

**Response:**
```json
{
    "specializations": [
        {"value": "cardiology", "label": "Cardiology"},
        {"value": "neurology", "label": "Neurology"}
    ]
}
```

---

### 🔗 Patient-Doctor Mapping APIs

#### 1. Create Mapping (Assign Doctor to Patient)
**POST** `/api/mappings/`

**Headers:**
```
Content-Type: application/json
Authorization: Bearer YOUR_ACCESS_TOKEN
```

**Request Body:**
```json
{
    "patient": 1,
    "doctor": 1,
    "status": "active",
    "notes": "Primary cardiologist for ongoing heart condition"
}
```

**Status Options:** `active`, `inactive`, `completed`

#### 2. List All Mappings
**GET** `/api/mappings/`

**Headers:**
```
Authorization: Bearer YOUR_ACCESS_TOKEN
```

**Query Parameters (Optional):**
- `status` - Filter by status: `/api/mappings/?status=active`

#### 3. Get Doctors for Specific Patient
**GET** `/api/mappings/<patient_id>/`

**Example:** `GET /api/mappings/1/`

#### 4. Update Mapping
**PUT** `/api/mappings/detail/<mapping_id>/`

**Request Body:**
```json
{
    "status": "completed",
    "notes": "Treatment completed successfully"
}
```

#### 5. Delete Mapping
**DELETE** `/api/mappings/detail/<mapping_id>/`

#### 6. Get Status Choices
**GET** `/api/mappings/status-choices/`

---

## 🔧 Example Usage Flow

### 1. Register and Login
```bash
# Register
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"myuser","email":"my@email.com","password":"mypass123","password_confirm":"mypass123","first_name":"My","last_name":"Name"}'

# Login
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"myuser","password":"mypass123"}'
```

### 2. Create Doctor
```bash
curl -X POST http://localhost:8000/api/doctors/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{"first_name":"Dr","last_name":"Smith","email":"dr@hospital.com","phone":"123456","license_number":"MD123","specialization":"cardiology","experience_years":5,"qualification":"MD","hospital_name":"Hospital","hospital_address":"123 St","city":"NYC","state":"NY","consultation_fee":200,"availability":"9-5"}'
```

### 3. Create Patient
```bash
curl -X POST http://localhost:8000/api/patients/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{"first_name":"John","last_name":"Doe","email":"john@example.com","phone":"123456","date_of_birth":"1990-01-01","gender":"M","address":"123 Main","city":"NYC","state":"NY","zip_code":"10001"}'
```

### 4. Assign Doctor to Patient
```bash
curl -X POST http://localhost:8000/api/mappings/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{"patient":1,"doctor":1,"status":"active","notes":"Primary care"}'
```

## 🗄️ Database Setup

### Development (Current Setup)
The project is currently configured to use SQLite for easy development.

### Production with PostgreSQL
1. Get your Neon DB connection string
2. Update the `.env` file:
   ```env
   DATABASE_URL=postgresql://username:password@hostname:5432/database_name
   ```
3. See `POSTGRESQL_SETUP.md` for detailed instructions

## 📁 Project Structure

```
healthcare/
├── healthcare_project/     # Main Django project
│   ├── settings.py        # Project settings
│   ├── urls.py           # Main URL configuration
│   └── wsgi.py           # WSGI configuration
│
├── authentication/        # User authentication app
│   ├── models.py         # User models (using Django's built-in)
│   ├── serializers.py    # API serializers
│   ├── views.py          # API views
│   └── urls.py           # URL routing
│
├── patients/             # Patient management app
│   ├── models.py         # Patient model
│   ├── serializers.py    # Patient serializers
│   ├── views.py          # Patient API views
│   ├── admin.py          # Admin configuration
│   └── management/       # Custom management commands
│
├── doctors/              # Doctor management app
│   ├── models.py         # Doctor model
│   ├── serializers.py    # Doctor serializers
│   ├── views.py          # Doctor API views
│   └── admin.py          # Admin configuration
│
├── mappings/             # Patient-Doctor mapping app
│   ├── models.py         # Mapping model
│   ├── serializers.py    # Mapping serializers
│   ├── views.py          # Mapping API views
│   └── admin.py          # Admin configuration
│
├── .env                  # Environment variables
├── requirements.txt      # Python dependencies
└── manage.py            # Django management script
```

## 🔑 Key Features Explained

### Authentication System
- JWT-based authentication using `djangorestframework-simplejwt`
- User registration with email validation
- Secure login with username/password
- Token refresh mechanism
- 1-hour access token lifetime, 24-hour refresh token

### Patient Management
- Complete patient profiles with medical history
- Blood group, allergies, and medical history tracking
- Address and contact information
- User isolation (users can only see their own patients)

### Doctor Management
- Comprehensive doctor profiles
- 14 medical specializations supported
- Hospital affiliation and consultation fees
- Public doctor directory (all users can view all doctors)
- License number validation

### Patient-Doctor Mapping
- Flexible assignment system
- Status tracking (active, inactive, completed)
- Assignment notes and history
- Prevents duplicate active assignments

### Security Features
- JWT authentication for all protected endpoints
- User data isolation
- Input validation and sanitization
- CORS configuration for frontend integration
- Environment variable configuration

## 🛠️ Development Commands

```bash
# Create new migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser for admin
python manage.py createsuperuser

# Run development server
python manage.py runserver

# Access admin interface
# http://localhost:8000/admin/
```

**Key Files for Reference:**
- `POSTGRESQL_SETUP.md` - Database setup instructions
- `.env` - Environment configuration

