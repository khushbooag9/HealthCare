# PostgreSQL Configuration Instructions

## Setting up PostgreSQL with Neon DB

### 1. Get your Neon DB Connection String
After creating a database on Neon, you'll get a connection string like:
```
postgresql://username:password@hostname:5432/database_name
```

### 2. Update Environment Variables
Edit the `.env` file and uncomment/update the DATABASE_URL:

```env
# Database Configuration - Uncomment and update with your Neon DB URL
DATABASE_URL=postgresql://your_username:your_password@your_host:5432/your_database

# Security
SECRET_KEY=your-secret-key-here
DEBUG=True

# JWT Configuration
JWT_ACCESS_TOKEN_LIFETIME=60
JWT_REFRESH_TOKEN_LIFETIME=1440

# Allowed hosts
ALLOWED_HOSTS=localhost,127.0.0.1
```

### 3. Update Settings.py
In `healthcare_project/settings.py`, uncomment the PostgreSQL configuration:

Replace the DATABASES section with:
```python
# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASE_URL = config('DATABASE_URL', default=None)

if DATABASE_URL and DATABASE_URL.startswith('postgresql://'):
    import urllib.parse as urlparse
    url = urlparse.urlparse(DATABASE_URL)
    port = url.port
    if port is None:
        port = 5432
    
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': url.path[1:],
            'USER': url.username,
            'PASSWORD': url.password,
            'HOST': url.hostname,
            'PORT': port,
        }
    }
else:
    # Fallback to SQLite for development
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
```

### 4. Run Migrations on PostgreSQL
After updating the configuration:

```bash
# Create new migrations (if needed)
python manage.py makemigrations

# Apply migrations to PostgreSQL
python manage.py migrate

# Create a superuser for admin access
python manage.py createsuperuser
```

### 5. Test the Connection
Start the server and test your APIs:
```bash
python manage.py runserver
```

The application will now use PostgreSQL instead of SQLite.

## Security Notes for Production

1. **Never commit your .env file** - Add it to .gitignore
2. **Use a strong SECRET_KEY** - Generate a new one for production
3. **Set DEBUG=False** in production
4. **Update ALLOWED_HOSTS** with your domain names
5. **Use HTTPS** in production
6. **Set up proper CORS** configuration for your frontend domain

## Backup Commands

### Backup Data
```bash
python manage.py dumpdata > backup.json
```

### Restore Data
```bash
python manage.py loaddata backup.json
```
