# GNSS_WiFi_Tracker_Open
The GNSS_WiFi_Tracker_Open application serves as an initial step for users to establish a foundational IoT tracker. Understanding the location data each device collects before sending it to the cloud for analysis is essential.

The system offers basic rules for device location, enabling quick implementation. This data can also be integrated with third-party tools to visualize device locations on maps, create instant alerts, share locations with other users, and more—enhancing the intelligence and usefulness of the devices.

# Technology Stacks
- Python
- FastAPI
- Pydantic
- JWT
- PWDLIB
- SQLAlchemy
- PostgreSQL
- Docker
- Redis

# Installation / Setup
## Prerequisites
- Python 3.9+
- pip

# Getting Started
## 1. Clone Instructions
```
git clone https://github.com/timtsai805-usa/MoneyManager.git
```
```
cd MoneyManager
```

## 2. Environment Setup
- Windows
```
python -m venv venv
```
```
venv/Scripts/activate
```
- macOS / Linux
```
python3 -m venv venv
```
```
source venv/bin/activate
```

## 3. Install Requirements
`pip install -r requirements.txt`

## 4. Run Docker
4.1 Build docker
```
docker-compose build
```
4.2 Activate docker in background
```
docker-compose up -d
```
4.3 Check docker status
```
docker-compose ps
```

## 5. Run Server
`uvicorn app.main:app --reload`

Server will start at:
    http://127.0.0.1:8000

## 6. API Docs / Usage
Once the server is running, open:
- Swagger UI
    http://127.0.0.1:8000/docs
- ReDoc
    http://127.0.0.1:8000/redoc

You can test all endpoints directly from the browser.

# 7. Project Structure
```
app/
├── core/
|   ├── auth
|   ├── security
├── models/
|   ├── init
|   ├── user
|   ├── device
|   ├── location
├── schemas/
|   ├── init
|   ├── user
|   ├── device
|   ├── location
├── routers/
|   ├── init
|   ├── auth
|   ├── user
|   ├── device
|   ├── location
├── main
├── db
├── README.md
├── Dockerfile
└── docker-compose
```

## 8. Features
- Authentication
- User Management
- Device Management
- Device Location

