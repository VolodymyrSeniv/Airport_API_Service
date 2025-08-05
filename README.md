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

## **Features**
- JWT authentication
- Admin panel /admin/
- Documentation is located at /api/doc/swagger/
- Orders and tickets management
- Creating, Updating and Deleting crew members
- Creating, Updating and Deleting countryes
- Creating, Updating and Deleting cities
- Creating, Updating and Deleting airplane types
- Creating, Updating and Deleting airplanes
- Creating, Updating and Deleting airports
- Creating, Updating and Deleting flights
- Creating, Updating and Deleting routes
- Filtering Flights by source, destination, deaprture time and arrival time

## **Screenshots**
- All routes of the application
<img width="1265" height="945" alt="image" src="https://github.com/user-attachments/assets/38968236-eca5-434f-8161-8f2a9283a745" />
- Flights list ednpoint

