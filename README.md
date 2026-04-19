🚀 Profile Intelligence Service (HNG Stage 1)

A production-ready RESTful API built with Django and Django REST Framework that aggregates and processes demographic data from multiple external APIs to generate enriched user profiles.

📌 Objective

This service accepts a name, fetches data from external APIs, processes the results, and returns a structured profile containing gender, age, age group, and nationality.

🧠 Features
Profile creation with external API enrichment
Gender prediction, age estimation, nationality inference
Age group classification logic
Idempotent profile creation (no duplicates per name)
Robust validation and error handling
Clean architecture using service layer pattern
⚙️ Tech Stack
Django 6.x
Django REST Framework
SQLite (development) / PostgreSQL (production-ready)
Requests library
Gunicorn + Whitenoise
🔗 External APIs
https://api.genderize.io
 → Gender prediction
https://api.agify.io
 → Age estimation
https://api.nationalize.io
 → Nationality prediction
📂 Project Structure
backend_wizards_stage1/

├── profiles/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── services.py
│   ├── urls.py
│
├── config/
│   ├── settings.py
│   ├── urls.py
│
├── manage.py
└── requirements.txt
🧪 Business Logic
Age Group Classification
0–12 → child
13–19 → teenager
20–59 → adult
60+ → senior
Nationality Selection

The system selects the country with the highest probability returned from the Nationalize API.

Idempotency

If a profile already exists for a given normalized name, the existing record is returned instead of creating a duplicate.

📡 API Endpoints
Create Profile

POST /api/profiles/

Request
{
  "name": "alex"
}
Response (201)
{
  "id": "uuid",
  "name": "alex",
  "gender": "male",
  "gender_probability": 0.98,
  "sample_size": 1200,
  "age": 27,
  "age_group": "adult",
  "country_id": "US",
  "country_probability": 0.75,
  "created_at": "2026-04-19T12:00:00Z"
}
List Profiles

GET /api/profiles/

Retrieve Profile

GET /api/profiles/{id}/

❗ Error Handling
Missing or Empty Name
{
  "status": "error",
  "message": "Missing or empty name"
}
Invalid Type
{
  "status": "error",
  "message": "Invalid type"
}
No Prediction Available
{
  "status": "error",
  "message": "No prediction available for the provided name"
}
External API Failure
{
  "status": "error",
  "message": "External service unavailable"
}
🧪 Running Locally
Clone Repository
git clone https://github.com/Ebenezer96/backend_wizards_stage1.git
cd backend_wizards_stage1
Create Virtual Environment
python -m venv venv
venv\Scripts\activate
Install Dependencies
pip install -r requirements.txt
Run Migrations
python manage.py migrate
Start Server
python manage.py runserver
🧱 Architecture Decisions
Service layer (services.py) handles all external API logic
Views remain thin and focused on request/response
Serializers handle validation and normalization
Centralized error handling for consistent API responses
📈 Future Improvements
Add caching (Redis)
Add rate limiting
Add authentication
Add Swagger/OpenAPI documentation
Introduce async processing (Celery)
👨‍💻 Author

Ebenezer Amakato
Backend Developer | ICT Officer



This project is for educational and assessment purposes.
