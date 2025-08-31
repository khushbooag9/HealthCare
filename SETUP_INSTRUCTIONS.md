# Healthcare Backend - Setup Instructions for Shared Project

## 🚀 Quick Setup After Download

### 1. Create Virtual Environment
```bash
python -m venv .venv
```

### 2. Activate Virtual Environment
```bash
# Windows
.\.venv\Scripts\activate

# Mac/Linux  
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment
```bash
# Copy the example environment file
copy .env.example .env

# Edit .env file with your own:
# - DATABASE_URL (your Neon DB connection string)
# - SECRET_KEY (generate a new one)
```

### 5. Run Migrations
```bash
python manage.py migrate
```

### 6. Create Superuser (Optional)
```bash
python manage.py createsuperuser
```

### 7. Start Server
```bash
python manage.py runserver
```

## 🔑 Important Notes

- **Never share your `.env` file** - it contains sensitive credentials
- **Generate a new SECRET_KEY** for your deployment
- **Use your own database** - don't use someone else's database URL
- **Review ALLOWED_HOSTS** for production deployment

## 📋 What You Need to Provide

1. **Database URL** - Get from Neon, PostgreSQL, or other provider
2. **Secret Key** - Generate using Django's `get_random_secret_key()`
3. **Environment Variables** - Update `.env` with your values

## 🛠️ Generate Secret Key
```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```
