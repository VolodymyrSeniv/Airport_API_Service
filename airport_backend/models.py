from django.db import models
from django.contrib.auth.models import AbstractUser
from airport_service import settings

class Crew(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    def __str__(self):
        return f"Crew member: {self.first_name} {self.last_name}"


class AirplaneType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"Airplane type: {self.name}"



class Airplane(models.Model):
    name = models.CharField(max_length=100)
    rows = models.IntegerField(null=False, blank=False)
    seats_in_row = models.IntegerField(null=False, blank=False)
    airplane_type = models.ForeignKey(
        AirplaneType,
        on_delete=models.CASCADE,
        related_name="airplane"
    )

    def __str__(self):
        return (f"Airplane: {self.name}. "
                f"Rows: {self.rows}. Seats per Row: {self.seats_in_row}. "
                f"Type: {self.airplane_type.name}")
    

class Airport(models.Model):
    name = models.CharField(max_length=100)
    closest_big_city = models.CharField(max_length=100)

    def __str__(self):
        return f"Airport: {self.name}, {self.closest_big_city}"


class Route(models.Model):
    source = models.ForeignKey(
        Airport,
        on_delete=models.CASCADE,
        related_name="route_source",
    )
    destination = models.ForeignKey(
        Airport,
        on_delete=models.CASCADE,
        related_name="route_destination"
    )
    distance = models.IntegerField(blank=False, null=False)

    def __str__(self):
        return (f"Route: From: {self.source.name} - To: {self.destination.name}. "
                f"Distance: {self.distance}.")


class Flight(models.Model):
    route = models.ForeignKey(
        Route,
        on_delete=models.CASCADE,
        related_name="flight_route"
    )
    airplane = models.ForeignKey(
        Airplane,
        on_delete=models.CASCADE,
        related_name="flight_airplane"
    )
    crew = models.ManyToManyField(Crew, related_name="flights")
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()

    def __str__(self):
        return (f"Flight: {self.route}. Plane: {self.airplane}. "
                f"Crew: {self.crew}. "
                f"Departure time: {self.departure_time}. Arrival time: {self.arrival_time}")


class Order(models.Model):
    created_at = models.DateTimeField()
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name = "order"
    )

    def __str__(self):
        return f"Time: {self.created_at}"



class Ticket(models.Model):
    row = models.IntegerField(null=False, blank=False)
    seat = models.IntegerField(null=False, blank=False)
    flight = models.ForeignKey(
        Flight,
        on_delete=models.CASCADE,
        related_name="ticket_flight"
    )
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="ticket_order"
    )

    def __str__(self):
        return (f"Ticket - Row: {self.row}. Seat: {self.seat}. "
                f"Flight: {self.flight.route}")
