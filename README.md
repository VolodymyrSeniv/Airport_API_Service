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
<img width="1250" height="1271" alt="image" src="https://github.com/user-attachments/assets/a8f6d9d2-1715-42ce-b3e6-36464b1fe5a5" />

- Crew Model list endpoint
<img width="1883" height="1039" alt="image" src="https://github.com/user-attachments/assets/3aa7d5c1-a144-4fbd-a886-8cae4cee4d52" />

- Route list endpoint
<img width="1140" height="1097" alt="image" src="https://github.com/user-attachments/assets/1935c8af-806b-4132-9094-33bbdab36930" />

- Countries list endpoint
<img width="765" height="972" alt="image" src="https://github.com/user-attachments/assets/b3defdef-08a2-4ddc-ae0e-b6a80c612ecf" />

- Cities list endpoint
<img width="1133" height="1127" alt="image" src="https://github.com/user-attachments/assets/f7b41a82-94a6-42b8-982f-8cd3b9f8bf14" />

- Cities retreive endpoint
<img width="1213" height="1056" alt="image" src="https://github.com/user-attachments/assets/8ef48537-cd24-42ed-8556-9144669f506f" />

## *Database ER diagram*








