# GNSS_WiFi_Tracker
Support authenticated user to manage multiple devices over AWS. Use RESTful API to request device detailed payload for frontend establishment on displaying device location over map.

# Technology Stacks
- python
- jwt
- pwdlib
- sqlalchemy
- postgres
- docker

# Project Structure
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
|   ├── location
|   ├── locationServices
├── map/
|   ├── wifi_loc
├── main
├── db
├── README.md
├── Dockerfile
└── docker-compose
```