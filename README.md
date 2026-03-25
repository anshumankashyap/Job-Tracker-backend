# AI Job Tracker — Backend

Django REST API powering the AI-Powered Job Application Tracker.

## Tech Stack
- **Django 4.x** + Django REST Framework
- **PostgreSQL** — primary database
- **SimpleJWT** — stateless JWT authentication
- **OpenAI GPT-4o** — AI resume analysis
- **pypdf** — PDF text extraction
- **Gunicorn** + **Whitenoise** — production server
- **Railway** — deployment platform

## Features
- JWT authentication (register, login, token refresh)
- Job application CRUD with PDF resume upload
- AI-powered resume vs job description analysis
- User-scoped data with IDOR prevention
- 12-factor app configuration

## Local Setup
```bash
# Clone and setup
git clone https://github.com/YOUR_USERNAME/job-tracker-backend.git
cd job-tracker-backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your values

# Run migrations
python manage.py migrate

# Start server
python manage.py runserver
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register/` | Register new user |
| POST | `/api/auth/login/` | Login, get JWT tokens |
| GET | `/api/auth/me/` | Get current user |
| GET | `/api/applications/` | List user's applications |
| POST | `/api/applications/` | Create application |
| PATCH | `/api/applications/{id}/` | Update application |
| DELETE | `/api/applications/{id}/` | Delete application |
| POST | `/api/ai-analyzer/{id}/analyze/` | Run AI analysis |

## Deployment
Deployed on Railway with PostgreSQL. See `Procfile` and `railway.json`.