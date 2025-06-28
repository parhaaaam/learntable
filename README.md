# LearnTable - Learning Management System API

LearnTable is a comprehensive Learning Management System (LMS) built with Django REST Framework. It provides a robust API for managing courses, users, assessments, and educational content with role-based access control.

## 🚀 Features

### Core Features
- **User Authentication & Authorization**: JWT-based authentication with role-based permissions
- **User Management**: Complete user profile management with email verification
- **Role-Based Access Control**: Custom role system with granular permissions
- **Course Management**: Create, update, and manage courses and course instances
- **Assessment System**: Create and manage assessments with submissions
- **Calendar Integration**: Event management for scheduling classes and activities
- **Content Management**: Organize and manage course content

### Technical Features
- **RESTful API**: Full REST API with OpenAPI/Swagger documentation
- **JWT Authentication**: Secure token-based authentication
- **MySQL Database**: Production-ready database backend
- **Docker Support**: Containerized deployment
- **Background Tasks**: Celery integration for async operations
- **Caching**: Redis-based caching system

## 📋 Prerequisites

Before you begin, ensure you have the following installed:
- Python 3.8+
- Docker and Docker Compose
- MySQL (if running locally)
- Redis (for caching and Celery)

## 🛠️ Installation & Setup

### ⚠️ MacOS Setup & Troubleshooting (Read First!)

#### 1. Install Homebrew (if not already installed)
```sh
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

#### 2. Install system dependencies for Python MySQL support
```sh
brew install mysql
brew install pkg-config
```

#### 3. (Optional but recommended) Use Python 3.10+
- This project is tested with Python 3.9, but Django 5.x requires Python 3.10+.
- If you use Python 3.9, make sure to use Django 4.2.x (already set in requirements.txt).
- You can install Python 3.10+ with Homebrew:
  ```sh
  brew install python@3.10
  ```

#### 4. If you see errors about missing `pkg-config` or `mysqlclient`:
- Make sure `pkg-config` is in your PATH:
  ```sh
  which pkg-config
  # Should output something like /opt/homebrew/bin/pkg-config
  ```
- If not, add Homebrew to your PATH (add to your ~/.zshrc or ~/.bash_profile):
  ```sh
  export PATH="/opt/homebrew/bin:$PATH"
  source ~/.zshrc  # or source ~/.bash_profile
  ```
- Then try again:
  ```sh
  pip install mysqlclient
  ```

#### 5. If you see errors about missing Python packages (e.g., `celery`, `drf_spectacular`, `whitenoise`, `django-debug-toolbar`):
- Run:
  ```sh
  pip install -r requirements.txt
  # Or install missing packages individually
  pip install celery drf-spectacular whitenoise django-debug-toolbar
  ```

#### 6. If you see errors about `socket.gethostbyname_ex` in `settings.py`:
- This is now handled gracefully, but if you modify settings, ensure you wrap hostname lookups in try/except blocks.

#### 7. If you see errors about MySQLdb:
- Make sure you have run `brew install mysql` and `pip install mysqlclient`.
- If you are on Apple Silicon (M1/M2), you may need to install Rosetta or use the correct architecture for Homebrew and Python.

---

### Option 1: Using Docker (Recommended)

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd learntable
   ```

2. **Create environment file**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Start the services**
   ```bash
   docker-compose up -d
   ```

4. **Run migrations**
   ```bash
   docker-compose exec web python manage.py migrate
   ```

5. **Create superuser**
   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```

6. **Collect static files**
   ```bash
   docker-compose exec web python manage.py collectstatic
   ```

### Option 2: Local Development

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd learntable
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your local database settings
   ```

5. **Set up database**
   ```bash
   python manage.py migrate
   ```

6. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server**
   ```bash
   python manage.py runserver
   ```

## 🆘 Troubleshooting Checklist
- [ ] Homebrew is installed and up to date
- [ ] `pkg-config` and `mysql` are installed via Homebrew
- [ ] Python version is compatible (3.9 for Django 4.2.x, 3.10+ for Django 5.x)
- [ ] All Python dependencies are installed (`pip install -r requirements.txt`)
- [ ] If you see `No module named ...`, install the missing package with pip
- [ ] If you see MySQLdb errors, check `mysqlclient` and `pkg-config` installation
- [ ] If you see hostname errors, ensure settings.py wraps hostname lookups in try/except
- [ ] If you see staticfiles/whitenoise errors, ensure `whitenoise` is installed

## 🐳 Docker Troubleshooting
- [ ] Docker and Docker Compose are installed and running
- [ ] If Docker build fails with PyPI mirror errors, the Dockerfile has been updated to use default PyPI
- [ ] If you see permission errors, try `sudo docker compose up --build`
- [ ] If build is slow, ensure you have good internet connection
- [ ] If containers fail to start, check if ports 8000, 3306, 6379 are available
- [ ] If database connection fails, ensure MySQL container is healthy before web container starts

## 🏁 First-Time Setup on MacOS (Step-by-Step)
1. Install Homebrew
2. `brew install mysql pkg-config`
3. (Optional) `brew install python@3.10`
4. `python3 -m venv venv && source venv/bin/activate`
5. `pip install -r requirements.txt`
6. `python3 manage.py migrate`
7. `python3 manage.py createsuperuser`
8. `python3 manage.py runserver`

---

## 🗄️ Database Setup

### Using Docker (Automatic)
The Docker setup automatically creates and configures the MySQL database.

### Manual Setup
1. Create a MySQL database
2. Update the database settings in `learntable/settings.py` or use environment variables:
   ```bash
   export MYSQL_DATABASE=learntable
   export MYSQL_USER=learntable_user
   export MYSQL_PASSWORD=your_password
   export MYSQL_HOST=localhost
   export MYSQL_PORT=3306
   ```

## 🔐 Authentication

The API uses JWT (JSON Web Tokens) for authentication. Here's how to use it:

### 1. Register a new user
```bash
curl -X POST http://localhost:8000/api/core/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepassword123",
    "password_confirmation": "securepassword123",
    "name": "John Doe",
    "gender": "male",
    "birth": "1990-01-01"
  }'
```

### 2. Login to get tokens
```bash
curl -X POST http://localhost:8000/api/core/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepassword123"
  }'
```

### 3. Use the access token
```bash
curl -X GET http://localhost:8000/api/core/auth/profile/ \
  -H "Authorization: Bearer <your_access_token>"
```

## 📚 API Endpoints

### Authentication Endpoints
- `POST /api/core/auth/register/` - Register new user
- `POST /api/core/auth/login/` - Login and get JWT tokens
- `POST /api/core/auth/token/refresh/` - Refresh access token
- `POST /api/core/auth/verify-email/` - Verify email address
- `GET /api/core/auth/profile/` - Get user profile
- `PUT /api/core/auth/change-password/` - Change password

### User Management
- `GET /api/core/users/` - List users (Admin only)
- `GET /api/core/users/{id}/` - Get user details
- `PUT /api/core/users/{id}/` - Update user (Admin only)
- `DELETE /api/core/users/{id}/` - Delete user (Admin only)
- `POST /api/core/users/{id}/assign_role/` - Assign role to user
- `POST /api/core/users/{id}/remove_role/` - Remove role from user

### Role Management
- `GET /api/core/roles/` - List roles
- `POST /api/core/roles/` - Create role (Admin only)
- `GET /api/core/roles/{id}/` - Get role details
- `PUT /api/core/roles/{id}/` - Update role (Admin only)
- `DELETE /api/core/roles/{id}/` - Delete role (Admin only)
- `POST /api/core/roles/{id}/assign_permissions/` - Assign permissions to role

### Permission Management
- `GET /api/core/permissions/` - List permissions
- `GET /api/core/permissions/{id}/` - Get permission details

### Course Management
- `GET /api/courses/` - List courses
- `POST /api/courses/` - Create course
- `GET /api/courses/{id}/` - Get course details
- `PUT /api/courses/{id}/` - Update course
- `DELETE /api/courses/{id}/` - Delete course

### Assessment Management
- `GET /api/assessment/` - List assessments
- `POST /api/assessment/` - Create assessment
- `GET /api/assessment/{id}/` - Get assessment details
- `PUT /api/assessment/{id}/` - Update assessment
- `DELETE /api/assessment/{id}/` - Delete assessment

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the project root with the following variables:

```env
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database Settings
MYSQL_DATABASE=learntable
MYSQL_USER=learntable_user
MYSQL_PASSWORD=your_password
MYSQL_HOST=localhost
MYSQL_PORT=3306

# Redis Settings
REDIS_URL=redis://localhost:6379/0

# Email Settings (for email verification)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

### JWT Settings
JWT tokens are configured with the following defaults:
- Access Token Lifetime: 60 minutes
- Refresh Token Lifetime: 1 day
- Algorithm: HS256

## 🧪 Testing

Run the test suite:
```bash
# Using Docker
docker-compose exec web python manage.py test

# Local development
python manage.py test
```

## 📖 API Documentation

Once the server is running, you can access the API documentation:

- **Swagger UI**: http://localhost:8000/api/schema/swagger-ui/
- **ReDoc**: http://localhost:8000/api/schema/redoc/
- **OpenAPI Schema**: http://localhost:8000/api/schema/

## 🚀 Deployment

### Production Deployment

1. **Update settings for production**
   - Set `DEBUG = False`
   - Configure `ALLOWED_HOSTS`
   - Use environment variables for sensitive data
   - Set up proper database credentials

2. **Collect static files**
   ```bash
   python manage.py collectstatic --noinput
   ```

3. **Run migrations**
   ```bash
   python manage.py migrate
   ```

4. **Set up a production web server** (e.g., Gunicorn with Nginx)

### Docker Production
```bash
# Build production image
docker build -t learntable:production .

# Run with production settings
docker run -d -p 8000:8000 --env-file .env.prod learntable:production
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/your-repo/learntable/issues) page
2. Create a new issue with detailed information
3. Contact the development team

## 🔄 Project Structure

```
learntable/
├── app/                    # Laravel-style container structure
│   └── Containers/        # Feature containers
├── apps/                   # Django apps
│   ├── courses/           # Course management
│   ├── assessment/        # Assessment system
│   └── calendar_event/    # Calendar functionality
├── core/                   # Core functionality
│   ├── models.py          # User, Role, Permission models
│   ├── views.py           # Authentication and user views
│   ├── serializers.py     # API serializers
│   └── urls.py            # URL routing
├── learntable/            # Django project settings
├── templates/             # HTML templates
├── static/                # Static files
├── media/                 # User uploaded files
├── requirements.txt       # Python dependencies
├── docker-compose.yml     # Docker configuration
└── README.md             # This file
```

## 🎯 Quick Start Checklist

- [ ] Clone the repository
- [ ] Set up environment variables
- [ ] Install dependencies
- [ ] Run database migrations
- [ ] Create superuser
- [ ] Start the development server
- [ ] Access the API documentation
- [ ] Test authentication endpoints
- [ ] Create your first course
