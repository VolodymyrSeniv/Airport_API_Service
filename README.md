# **Airport API**
API service for airport management written in DRF

## **Installing using GitHub**
Install PostgresSQL and create db
```
git clone https://github.com/VolodymyrSeniv/Airport_API_Service.git
cd Airport_API_Service
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
set DB_HOST=<your db hostname>
set DB_NAME=<you db name>
set DB_user=<you db username>
set DB_PASSWORD=<you db user password>
set SECRET_KEY=<your secret key>
python manage.py migrate
python manage.py runserver
```

## **Run with docker**
Docker should be installed
```
docker-compose build
docker compose up
```

## **Getting access**
- create user via `/api/user/register/`
- get access token via `/api/user/token/`
