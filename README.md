# DRF - Django Rest Framework 

This repository contains code examples covering **Basic to Advanced concepts of Django Rest Framework (DRF)**.  
The topics include:
- What is API?  
- API Methods (GET, POST, PUT, PATCH, DELETE)  
- Function-based views (`@api_view`)  
- Serializers (Model Serializer, Basic Serializer)  
- Serializer Validation & Custom Validators  
- Class-based views (APIView, Generic Views, Mixins, Concrete View Classes, ModelViewSet)  
- Actions  
- Authentication in DRF  
- Default Permissions  
- Pagination & Custom Pagination  
- Throttling & Custom Throttling  

---
Also Event Project ecomm_dash
- Login and Logout
- You book an event
- View an event
- Add an event
- We have tickets, Event and Booking models

## Installation Prerequisites

### 1. Install Python  
Install python-3.7.2 or above and python-pip.  
Reference: [Python Installation Guide](https://docs.python-guide.org/starting/installation/)  

### 2. Install PostgreSQL  
Install PostgreSQL (recommended version 13+).  
Reference: [PostgreSQL Installation Guide](https://www.postgresql.org/download/)  

### 3. Install Postman  
Download and install Postman for API testing.  
Reference: [Postman Download](https://www.postman.com/downloads/)  

### 4. Setup Virtual Environment  

#### For macOS/Linux:
```bash
# Install virtual environment
sudo pip install virtualenv

# Make a directory for environments
mkdir envs

# Create virtual environment
virtualenv ./envs/

# Activate virtual environment
source envs/bin/activate
```

#### For Windows (PowerShell):
```bash
# Install virtual environment
pip install virtualenv

# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate
```

### 5. Clone Git Repository  
```bash
git clone "https://github.com/abbasabro/DRF.git"
```

### 6. Install Requirements  
```bash
cd djrest
pip install -r requirements.txt
```

---

## Project Settings

Open `settings.py` and update the following configurations:

```python
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.ScopedRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'author': '10/min'
    }
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'djrest', # Open pgAdmin and create a database with this name
        'USER' : 'postgres',
        'PASSWORD' : 'admin',
        'HOST' : 'localhost',
        'PORT' : '5432'
    }
}

INSTALLED_APPS = [
    'home',
    'rest_framework.authtoken', # For Token Based Authentication
    'event_project',
    'rest_framework', # Rest Framework Ready to go!
]
```

---

## Run the Server

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

Server will start at: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

## Test URLs in Postman

### Home App URLs:
- `http://127.0.0.1:8000/`  
- `http://127.0.0.1:8000/api/author/`  
- `http://127.0.0.1:8000/api/author/v1/`  
- `http://127.0.0.1:8000/api/author/v2/`  
- `http://127.0.0.1:8000/create_records/`  
- `http://127.0.0.1:8000/view_records/`  
- `http://127.0.0.1:8000/update_records/`  
- `http://127.0.0.1:8000/delete_records/<id>/`  
- `http://127.0.0.1:8000/create_book/`  
- `http://127.0.0.1:8000/view_book/`  
- `http://127.0.0.1:8000/create_user/`  
- `http://127.0.0.1:8000/api/v2/student/`  
- `http://127.0.0.1:8000/api/v3/student/<int:pk>/`  
- `http://127.0.0.1:8000/api/product/`  
- `http://127.0.0.1:8000/api/register/`  
- `http://127.0.0.1:8000/api/login/`  
- `http://127.0.0.1:8000/product/v2/`  

### Ecomm Project URLs:
- `http://127.0.0.1:8000/register/`  
- `http://127.0.0.1:8000/login/`  
- `http://127.0.0.1:8000/private/event/`  
- `http://127.0.0.1:8000/public/event/`  
- `http://127.0.0.1:8000/booking/`  

---

Now you are good to go 🚀
