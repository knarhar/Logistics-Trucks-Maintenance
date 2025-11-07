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
    │   ├───utils
    ├───logs
    └───scripts          
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

| Method   | Endpoint                          | Description                    |
|----------|-----------------------------------|--------------------------------|
| `GET`    | `/`                               | Root health check              |
| `GET`    | `/health`                         | Detailed health status         |

### Authentication
| Method   | Endpoint                          | Description                    |
|----------|-----------------------------------|--------------------------------|
|          |                                   |                                |
| `POST`   | `/api/v1/auth/login`              | Login                          |
| `POST`   | `/api/v1/auth/logout`             | Logout                         |
| `POST`   | `/api/v1/auth/refresh`            | Refreshing access token        |


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

---

## 🛠️ Tech Stack

* **FastAPI** — modern async Python web framework
* **Pydantic** — data validation
* **SQLAlchemy** — ORM
* **PostgreSQL** — database
* **Uvicorn** — ASGI server

---

## 📦 Future Features

* Truck maintenance scheduling
* Driver and fleet management


