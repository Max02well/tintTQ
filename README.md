# TintTQ AI Backend

AI-Powered Car Tint Visualization and Auto Styling Platform.

TintTQ AI is a modern AI-driven platform designed to help users preview car tint styles, receive intelligent tint recommendations, and manage automotive customization workflows.

Built with FastAPI and designed for future AI/computer vision integrations.

---

## Features

* AI-powered tint visualization
* Car tint recommendation engine
* FastAPI backend architecture
* RESTful API endpoints
* Middleware request timing
* CORS-enabled API
* Modular route structure
* Ready for AI/ML integrations
* Scalable backend foundation

---

## Tech Stack

### Backend

* Python 3.13+
* FastAPI
* Uvicorn
* Pydantic

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
│   ├── middleware/
│   │   └── timer.py
│   │
│   ├── routes/
│      ├── products.py
│      └── users.py
│   
│
├── main.py
├── pyproject.toml
├── requirements.txt
├── README.md
├── pyproject.toml
├── uv.lock
├── .env
└── .gitignore

```

---

## Installation

### Clone the Repository

```bash
git clone https://github.com/yourusername/tintTQAI.git
cd tintTQAI
```

---

## 1.Using uv sync

### Method 1 -- Install dependencies at once

```bash
uv sync

## 2.Create Virtual Environment

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

Create a `.env` file in the project root.

Example:

```env
OPENAI_API_KEY=
DATABASE_URL=
JWT_SECRET=
```

---

## Requirements

* Python 3.13+
* FastAPI
* Uvicorn

---

## Author

Built by Max Gogo.

---

## License

This project is licensed under the MIT License.
