from django.urls import path, include
from airport_backend.views import (AirplaneTypeViewSet,
                                   CrewModelViewSet,
                                   AirplaneViewSet,
                                   AirportViewSet,
                                   RouteViewSet,
                                   FlightViewSet,
                                   UserViewSet,
                                   OrderViewSet,
                                   TicketViewSet,
                                   CountryViewSet,
                                   CityViewSet)
from rest_framework import routers

app_name = "airport_backend"

router = routers.DefaultRouter()
router.register("crews", CrewModelViewSet)
router.register("airplane_types", AirplaneTypeViewSet)
router.register("airplanes", AirplaneViewSet)
router.register("airports", AirportViewSet)
router.register("routes", RouteViewSet)
router.register("flights", FlightViewSet)
router.register("users", UserViewSet)
router.register("orders", OrderViewSet)
router.register("tickets", TicketViewSet)
router.register("countries", CountryViewSet)
router.register("cities", CityViewSet)
urlpatterns = [
    path("", include(router.urls))
]