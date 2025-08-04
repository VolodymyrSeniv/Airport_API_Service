from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework.test import APIClient
from rest_framework import status
from airport_backend.models import (Flight,
                                    Route,
                                    Airplane,
                                    Airport,
                                    City,
                                    Country,
                                    AirplaneType, Crew)
from airport_backend.serializers import (FlightListSerializer,
                                         FlightRetrieveSerialzier)

FLIGHTS_LIST_URL = reverse("airport_backend:flight-list")

def sample_flight(**params) -> Flight:
    defaults = {
        "route": Route.objects.create(
                source = Airport.objects.create(
                    name = "Something",
                    closest_big_city = City.objects.create(
                        name = "Barcelona",
                        country = Country.objects.create(
                            name = "Spain"
                        )
                    )
                ),
                destination = Airport.objects.create(
                    name = "Anything",
                    closest_big_city = City.objects.create(
                        name = "Madrid",
                        country = Country.objects.get(pk=1)
                    )
                ),
                distance=600,
            ),
        "airplane": Airplane.objects.create(name="Jack",
                                     rows=50,
                                     seats_in_row=50,
                                     airplane_type=AirplaneType.objects.create(
                                         name="Some"
                                     )),
        "departure_time": "2025-08-10T08:00:00Z",
        "arrival_time": "2025-08-10T12:30:00Z"
    }
    defaults.update(params)
    return Flight.objects.create(**defaults)

def detail_flight_url(bus_id):
    return reverse("airport_backend:flight-detail", args=(bus_id,))

class TestNotAuthenticated(TestCase):

    def setUp(self):
        self.client = APIClient()
    

    def test_list_flights(self):
        res = self.client.get(FLIGHTS_LIST_URL)
        self.assertEqual(res.status_code,
                         status.HTTP_401_UNAUTHORIZED)
        

class TestAuthenticated(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@test.test", password="testpassword"
        )
        self.client.force_authenticate(self.user)
    

    def test_list_flight(self):
        res = self.client.get(FLIGHTS_LIST_URL)
        flights = Flight.objects.all()
        serializer = FlightListSerializer(flights, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["results"], serializer.data)
    

    def test_create_flight(self):
        payload = {
            "departure_time": "2025-08-10T08:00:00Z",
            "arrival_time": "2025-08-10T12:30:00Z"
        }
        res = self.client.post(FLIGHTS_LIST_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
    

    def test_filtering_flights_by_source_destination_and_both(self):
        country = Country.objects.create(name="Spain")
        city1 = City.objects.create(name="Barcelona", country=country)
        city2 = City.objects.create(name="Madrid", country=country)
        city3 = City.objects.create(name="Valencia", country=country)

        source1 = Airport.objects.create(name="Airport A", closest_big_city=city1)
        destination1 = Airport.objects.create(name="Airport B", closest_big_city=city2)
        destination2 = Airport.objects.create(name="Airport C", closest_big_city=city3)

        route1 = Route.objects.create(source=source1, destination=destination1, distance=500)
        route2 = Route.objects.create(source=source1, destination=destination2, distance=600)
        route3 = Route.objects.create(source=destination1, destination=destination2, distance=300)

        airplane_type = AirplaneType.objects.create(name="Airbus A320")
        airplane = Airplane.objects.create(name="Plane 1", rows=20, seats_in_row=6, airplane_type=airplane_type)

        flight1 = Flight.objects.create(
            route=route1,
            airplane=airplane,
            departure_time="2025-08-10T08:00:00Z",
            arrival_time="2025-08-10T10:00:00Z"
        )
        flight2 = Flight.objects.create(
            route=route2,
            airplane=airplane,
            departure_time="2025-08-11T08:00:00Z",
            arrival_time="2025-08-11T10:00:00Z"
        )
        flight3 = Flight.objects.create(
            route=route3,
            airplane=airplane,
            departure_time="2025-08-12T08:00:00Z",
            arrival_time="2025-08-12T09:00:00Z"
        )

        # Filter by source only
        res_source = self.client.get(FLIGHTS_LIST_URL, {"source": source1.id})
        source_ids = [flight["id"] for flight in res_source.data["results"]]
        self.assertIn(flight1.id, source_ids)
        self.assertIn(flight2.id, source_ids)
        self.assertNotIn(flight3.id, source_ids)

        # Filter by destination only
        res_destination = self.client.get(FLIGHTS_LIST_URL, {"destination": destination2.id})
        dest_ids = [flight["id"] for flight in res_destination.data["results"]]
        self.assertIn(flight2.id, dest_ids)
        self.assertIn(flight3.id, dest_ids)
        self.assertNotIn(flight1.id, dest_ids)

        # Filter by both source and destination
        res_both = self.client.get(FLIGHTS_LIST_URL, {
            "source": source1.id,
            "destination": destination2.id
        })
        both_ids = [flight["id"] for flight in res_both.data["results"]]
        self.assertIn(flight2.id, both_ids)
        self.assertNotIn(flight1.id, both_ids)
        self.assertNotIn(flight3.id, both_ids)

    

    def test_retrieve(self):
        flight = sample_flight()
        print(flight)
        res = self.client.get(detail_flight_url(flight.id))

        ser_movie = FlightRetrieveSerialzier(flight)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, ser_movie.data)


class Test_Is_Authenticated_Admin(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="admin@admin.admin",
            password="admintestpassword",
            is_staff=True
        )
        self.client.force_authenticate(self.user)
    
    def test_create_flight(self):
        spain = Country.objects.create(name="Spain")
        barcelona = City.objects.create(name="Barcelona", country=spain)
        madrid = City.objects.create(name="Madrid", country=spain)

        source_airport = Airport.objects.create(name="Source Airport", closest_big_city=barcelona)
        destination_airport = Airport.objects.create(name="Destination Airport", closest_big_city=madrid)

        route = Route.objects.create(source=source_airport, destination=destination_airport, distance=600)

        airplane_type = AirplaneType.objects.create(name="Boeing 737")
        airplane = Airplane.objects.create(name="Plane A", rows=20, seats_in_row=6, airplane_type=airplane_type)

        payload = {
            "route": route.id,
            "airplane": airplane.id,
            "departure_time": "2025-08-10T08:00:00Z",
            "arrival_time": "2025-08-10T12:30:00Z"
        }

        res = self.client.post(FLIGHTS_LIST_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)