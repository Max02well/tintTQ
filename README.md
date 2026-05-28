# TintTQ AI Backend --> planned project(June 2026)

AI-Powered Car Tint Visualization and Auto Styling Platform.

TintTQ AI is a modern AI-driven platform designed to help users preview car tint styles, receive intelligent tint recommendations, and manage automotive customization workflows.

Built with FastAPI and designed for future AI/computer vision integrations.

---

## Features

* AI-powered Vehicle tint visualization system (planned)
* Car tint recommendation engine (planned)
* RESTful API endpoints
* Middleware request timing
* CORS-enabled API
* Modular route structure
* Ready for AI/ML integrations

* User authentication & authorization (JWT)
* Vehicle Tint booking management system
* Modular FastAPI architecture
* Async database operations (SQLAlchemy 2.0)
* Alembic database migrations
* CORS-enabled backend
* Scalable service-layer architecture

---
## Planned AI Capabilities

* Car tint simulation from uploaded images
* Smart tint recommendations based on:
  - vehicle type
  - lighting conditions
  - legal tint limits
* Damage detection & car condition analysis
* Automated quotation generation
* AI assistant for tint selection
* Computer vision-based preview engine (OpenCV / YOLO)

---

## Tech Stack

### Backend

* Python 3.13+
* FastAPI
* Uvicorn
* Pydantic
* SQLAlchemy 2.0 (Async)
* Alembic (Migrations)
* PostgreSQL
* Psycopg2 / asyncpg
* OAuth(planned)
* JWT

### AI/ML (Planned)

* OpenCV
* YOLOv8
* TensorFlow / PyTorch

### Future Integrations

* Computer vision tint preview
* Damage detection
* Smart quotation generation
* Vehicle customization AI

---

## Project Structure

```bash
tintTQAI/
│
├── app/
│   ├── config/              # Settings, DB config etc
│   │   ├── settings.py
│   │   └── database.py
│   │
│   ├── db/
│   │   ├── session.py       # async session
│   │   ├── base.py          # Base model registry
│   │   └── migrations/      # Alembic setup
│   │
│   ├── models/              # SQLAlchemy models
│   │   ├── user.py
│   │   ├── vehicle.py
│   │   ├── tint.py
│   │   └── booking.py
│   │
│   ├── schemas/            # pydantic models
│   │   ├── tint_schema.py
│   │   ├── auth_schema.py
│   │   └── user_schema.py
│   │
│   ├── repositories/            # Schemas
│   │   ├── tint_repository.py
│   │   ├── booking_repository.py
│   │   └── user_repository.py
│   │
│   ├── services/            # Business logic layer
│   │   ├── auth_service.py
│   │   ├── tint_service.py
│   │   └── user_service.py
│   │
│   ├── routes/              # API endpoints
│   │   ├── auth.py
│   │   ├── users.py
│   │   ├── tint.py
│   │   ├── bookings.py
│   │   └── health.py
│   │
│   ├── generated/            #for AI 
│   │
│   ├── utils/               # Helpers (JWT, hashing, etc.)
│   │
│   └── middleware  
│          # FastAPI entry point
├── models/
├── scripts/
├── alembic.ini
├── pyproject.toml
├── uv.lock
├── requirements.txt
├── .env
├── .env-example
├── README.md
└── .gitignore

---

## Installation

### Clone the Repository

```bash
git clone https://github.com/Max02well/tintTQAI.git
cd tintTQAI
```

---

## 1.Create Virtual Environment

### Using uv

```bash
uv venv
```

Activate the environment:

#### Windows

```bash
.venv\Scripts\activate
```

#### Linux / macOS

```bash
source .venv/bin/activate
```

---

## Install Dependencies

### Using uv

```bash
uv sync

or using pip

uv pip install -r requirements.txt
```

---

## Run the Development Server

### Using Uvicorn

```bash
uvicorn main:app --reload
```

### Or Using FastAPI CLI

```bash
fastapi dev main.py
```

---

## API Endpoints

### Root Endpoint

```http
GET /
```

Response:

```json
{
  "message": "Welcome to the tintTQ API"
}
```

---

## Interactive API Docs

FastAPI automatically generates API documentation.

### Swagger UI

```bash
http://127.0.0.1:8000/docs
```

### ReDoc

```bash
http://127.0.0.1:8000/redoc
```

---

## Middleware

### Timing Middleware

The application includes a custom timing middleware that measures request execution time.

Location:

```bash
app/middleware/timer.py
```

---

## CORS Configuration

CORS is enabled to allow frontend applications to communicate with the backend API.

```python
allow_origins=["*"]
```

---

## Planned AI Features

* AI tint simulation from uploaded car images
* Smart tint recommendations
* Vehicle damage detection
* Paint condition analysis
* Auto-detailing recommendations
* AI-generated quotations
* Legal tint compliance checker

---

## Environment Variables

Create a `.env` file in the project root.(as per .env-example)

Example:

```env
OPENAI_API_KEY=
DATABASE_URL=
SYNC_DB_URL=
SECRET=

```

---

## Requirements

* Python 3.13+
* FastAPI
* Uvicorn

---

## Author

Built by Max Gogo - Building one code at a time -

---

## License

This project is licensed under the MIT License.
