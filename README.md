# Todo Web Application

A full-stack task management system built with **FastAPI** and **PostgreSQL**, featuring JWT authentication, role-based access control, and a server-rendered frontend using Jinja2 templates. Deployed live on Railway.

🔗 **Live Demo:** [fastapi-production-e1cc.up.railway.app](http://fastapi-production-e1cc.up.railway.app)

---

## Features

- User registration and login with **JWT authentication**
- Each user sees and manages only their own todos
- Full **CRUD** for todos (create, read, update, delete)
- Todo priority levels (1–5)
- Todo completion status tracking
- **Role-based access control** — admin users can view and delete all todos across all users
- Change password endpoint
- Update phone number endpoint
- Server-side rendered pages with **Jinja2 templates**
- Static file serving (CSS, JS)
- Health check endpoint
- Database migrations with **Alembic**
- Tests with **pytest**

---

## Tech Stack

- **Backend:** Python, FastAPI
- **Database:** PostgreSQL (via Supabase), SQLite (local dev)
- **ORM:** SQLAlchemy
- **Migrations:** Alembic
- **Auth:** JWT (python-jose), bcrypt (passlib)
- **Frontend:** Jinja2 Templates, HTML, CSS, JavaScript
- **Testing:** pytest
- **Deployment:** Railway

---

## Project Structure

```
fastapi/
├── TodoApp/
│   ├── routers/
│   │   ├── auth.py       # Register, login, JWT token
│   │   ├── todos.py      # Todo CRUD (user-scoped)
│   │   ├── users.py      # Change password, update phone number
│   │   ├── admin.py      # Admin-only: view/delete all todos
│   │   └── api.py        # Health/test endpoint
│   ├── Templates/        # Jinja2 HTML templates
│   ├── static/           # CSS and JS files
│   ├── test/             # pytest test files
│   ├── alembic/          # Database migration scripts
│   ├── models.py         # SQLAlchemy User and Todo models
│   ├── database.py       # DB engine and session setup
│   └── main.py           # FastAPI app entry point
└── requirements.txt
```

---

## API Endpoints

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/` | Register a new user |
| POST | `/auth/token` | Login and get JWT token |
| GET | `/auth/me` | Get current logged-in user |

### Todos
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/todos/` | Get all todos for current user |
| GET | `/todos/todo/{id}` | Get single todo by ID |
| POST | `/todos/todo/` | Create a new todo |
| PUT | `/todos/todo/{id}` | Update a todo |
| DELETE | `/todos/todo/{id}` | Delete a todo |

### User
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/user/` | Get current user profile |
| PUT | `/user/password` | Change password |
| PUT | `/user/phonenumber/{phone}` | Update phone number |

### Admin (admin role required)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/admin/todo` | Get all todos (all users) |
| DELETE | `/admin/todo/{id}` | Delete any todo by ID |

---

## Setup & Installation

### 1. Clone the repository
```bash
git clone https://github.com/SherazHaider907/fastapi.git
cd fastapi
```

### 2. Create and activate a virtual environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure the database

In `TodoApp/database.py`, switch to SQLite for local development:
```python
SQLALCHEMY_DATABASE_URL = "sqlite:///./todosapp.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
```

Or set up a PostgreSQL connection string for production.

### 5. Run migrations
```bash
cd TodoApp
alembic upgrade head
```

### 6. Start the server
```bash
fastapi dev TodoApp/main.py
```

Visit `http://localhost:8000` in your browser.

---

## Running Tests

```bash
cd TodoApp
pytest test/
```

---

## Pages

| URL | Description |
|-----|-------------|
| `/home` | Landing page |
| `/login` | Login page |
| `/register` | Register page |
| `/todos` | Todo management page |
| `/healthy` | Health check |
| `/docs` | Swagger UI (auto-generated API docs) |
