Backend app for comfortable parking

## Technologies
### Backend
- Python: 3.12+

# #External dependencies
### Backend:
- fastapi: 0.114.1
- black: 24.8.0
- uvicorn: 0.30.6
- alembic: 1.13.2
- sqlalchemy: 2.0.34
- pydantic-settings: 2.5.2
- jwt: 1.3.1
- pyjwt: 2.9.0
- bcrypt: 4.2.0
- python-multipart: 0.0.9
- asyncpg: 0.29.0

To run, you need to:
- create two files with a private and a public key
  (certs/jwt-private.pem and certs/jwt-public.pem accordingly)
  ```
  cd src
  mkdir certs
  cd certs
  echo > jwt-private.pem
  echo > jwt-public.pem
  cd ..
  ```
  and write the key values in them
- create a file .env and specify the value of the fields
  ```
  DB_HOST=...
  DB_PORT=...
  DB_NAME=...
  DB_USER=...
  DB_PASS=...
  ```
  
- launching the application
  locally
  ```
  poetry install
  poetry scr/main.py
  ```
