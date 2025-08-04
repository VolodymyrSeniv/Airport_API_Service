from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework.test import APIClient
from rest_framework import status
from airport_backend.models import Crew
from airport_backend.serializers import (CrewSerializer,
                                         CrewListSerializer)


CREW_LIST_URL = reverse("airport_backend:crew-list")


def sample_crew(**params) -> Crew:
    defaults = {
        "first_name": "Volodymyr",
        "last_name": "Seniv",
    }
    defaults.update(params)
    return Crew.objects.create(**defaults)


def detail_crew_url(crew_id):
    return reverse("airport_backend:crew-detail", args=(crew_id,))


class TestNotAuthenticated(TestCase):

    def setUp(self):
        self.client = APIClient()
    

    def test_list_crews(self):
        res = self.client.get(CREW_LIST_URL)
        self.assertEqual(res.status_code,
                         status.HTTP_401_UNAUTHORIZED)
        

class TestAuthenticated(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@test.test", password="testpassword"
        )
        self.client.force_authenticate(self.user)
    

    def test_list_crew(self):
        res = self.client.get(CREW_LIST_URL)
        crews = Crew.objects.all()
        serializer = CrewListSerializer(crews, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["results"], serializer.data)
    

    def test_create_crew(self):
        payload = {
            "first_name": "Martha",
            "last_name": "Dumych",
        }
        res = self.client.post(CREW_LIST_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
    

    def test_retrieve(self):
        crew = sample_crew()
        res = self.client.get(detail_crew_url(crew.id))

        ser_crew = CrewSerializer(crew)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, ser_crew.data)


class Test_Is_Authenticated_Admin(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="admin@admin.admin",
            password="admintestpassword",
            is_staff=True
        )
        self.client.force_authenticate(self.user)
    
    def test_create_crew(self):
        payload = {
            "first_name": "Martha",
            "last_name": "Dumych",
        }
        res = self.client.post(CREW_LIST_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        