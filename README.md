# 🚛 Logistical Company Trucks Maintenance API

Backend service for managing logistics truck maintenance records, schedules, and related operational data.
Built with FastAPI, structured for scalability and clarity.

### Project structure

```
    ├───alembic
    │   └───versions
    ├───app
    │   ├───api
    │   │   └───v1
    │   │       └───endpoints
    │   ├───core
    │   ├───db
    │   ├───models
    │   ├───schemas
    │   ├───services
    │   └───utils        
    │   .env
    │   .env.example
    │   .gitignore
    │   alembic.ini
    │   README.md
    │   requirements.txt
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
    git clone https://github.com/knarhar/Logistics-Trucks-Maintenance.git
    cd Logistics-Trucks-Maintenance
```

### 2. Create virtual environment

```bash
    python -m venv venv
    source venv/bin/activate  # On Linux/Mac
    venv\Scripts\activate     # On Windows
```

### 3. Install dependencies

```bash
  pip install -r requirements.txt
```

### 4. Create and run migrations

```bash
    alembic revision --autogenerate -m "Initial migration"
    alembic upgrade head
```

---

## 🚀 Running the Application

Start the development server with:

```bash
  uvicorn app.main:app --reload
```

App will be available at:
👉 [http://localhost:8000/api/v1/docs](http://localhost:8000/api/v1/docs)

---

## 🧰 Environment Variables

Create a `.env` file in the root directory and use .env.example for it's configuration:

```bash
  cp .env.example .env # On Linux/Mac
  copy .env.example .env # 0n Windows
```

---

## 🌍 API Endpoints

### Basic

| Method | Endpoint  | Description            |
|--------|-----------|------------------------|
| `GET`  | `/`       | Root health check      |
| `GET`  | `/health` | Detailed health status |

### Authentication

| Method | Endpoint               | Description             |
|--------|------------------------|-------------------------|
| `POST` | `/api/v1/auth/login`   | Login                   |
| `POST` | `/api/v1/auth/logout`  | Logout                  |
| `POST` | `/api/v1/auth/refresh` | Refreshing access token |

### Trucks

| Method   | Endpoint                          | Description                    |
|----------|-----------------------------------|--------------------------------|
| `POST`   | `/api/v1/trucks/add`              | Create a truck                 |
| `GET`    | `/api/v1/trucks?skip=0&limit=10 ` | Get truck list with pagination |
| `PATCH`  | `/api/v1/trucks/{truck_id} `      | Update truck                   |
| `DELETE` | `/api/v1/trucks/{truck_id} `      | Soft delete truck              |

### Mechanics

| Method   | Endpoint                          | Description                                  |
|----------|-----------------------------------|----------------------------------------------|
| `POST`   | `/api/v1/mechanics/add`           | Create a mechanic                            |
| `GET`    | `/api/v1/mechanics?search= `      | Get mechanic list with partial name matching |
| `PATCH`  | `/api/v1/mechanic/{mechanic_id} ` | Update mechanic                              |
| `DELETE` | `/api/v1/mechanic/{mechanic_id} ` | Delete mechanic                              |

### Incidents

| Method   | Endpoint                                            | Description                                        |
|----------|-----------------------------------------------------|----------------------------------------------------|
| `POST`   | `/api/v1/incidents/add`                             | Create an incident                                 |
| `GET`    | `/api/v1/incidents?status=&truck_id=&mechanic_id= ` | Get incidents list with optional filtration params |
| `PATCH`  | `/api/v1/incidents/{incident_id} `                  | Update incident                                    |
| `DELETE` | `/api/v1/incidents/{incident_id} `                  | Delete mechanic                                    |

### AI mechanic suggestion

AI suggests suitable mechanics based on the provided issue type and description.

| Method | Endpoint                      | Description                                                                                                                  |
|--------|-------------------------------|------------------------------------------------------------------------------------------------------------------------------|
| `POST` | `/api/v1/ai/suggest-mechanic` | Accepts JSON body with `issue_type` and `issue_description`, <br/> returns AI-suggested mechanics sorted by confidence score |

#### Request Body Example

```json
{
  "issue_type": "suspension",
  "issue_description": "Front suspension makes squeaking sound when turning sharply, uneven tire wear on the front axle"
}
```

---

## 🛠️ Tech Stack

* **FastAPI** — modern async Python web framework
* **Pydantic** — data validation
* **SQLAlchemy** — ORM
* **PostgreSQL** — database
* **Uvicorn** — ASGI server



