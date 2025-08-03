from django.db import models
from datetime import datetime
from airport_service import settings
from airport_backend.utils import create_custom_path
from django.core.exceptions import ValidationError

class Crew(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    image = models.ImageField(null=True, upload_to=create_custom_path)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class AirplaneType(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"Airplane type: {self.name}"


class Airplane(models.Model):
    name = models.CharField(max_length=100)
    rows = models.IntegerField(null=False, blank=False)
    seats_in_row = models.IntegerField(null=False, blank=False)
    airplane_type = models.ForeignKey(
        AirplaneType,
        on_delete=models.CASCADE,
        related_name="airplane_type"
    )
    image = models.ImageField(null=True, upload_to=create_custom_path)

    @property
    def total_seats(self):
        return self.rows * self.seats_in_row
    
    def __str__(self):
        return (f"Airplane: {self.name}. "
                f"Rows: {self.rows}. Seats per Row: {self.seats_in_row}. "
                f"Type: {self.airplane_type.name}")
    

class Country(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"{self.name}"


class City(models.Model):
    name = models.CharField(max_length=100, unique=True)
    country = models.ForeignKey(
        Country,
        on_delete=models.CASCADE,
        related_name="city_country"
    )
    image = models.ImageField(null=True, upload_to=create_custom_path)

    def __str__(self):
        return f"{self.name}, {self.country}"


class Airport(models.Model):
    name = models.CharField(max_length=100, unique=True)
    closest_big_city = models.ForeignKey(
        City,
        on_delete=models.CASCADE,
        related_name="airport_city",
        default="0"
    )

    def __str__(self):
        return f"Airport: {self.name}, {self.closest_big_city.name}"


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
        return f"{self.source} - {self.destination}"


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
    crew = models.ManyToManyField(Crew, related_name="flights_orders")
    departure_time = models.DateTimeField(unique=True)
    arrival_time = models.DateTimeField(unique=True)

    def __str__(self):
        return (f"Flight: {self.route}. Plane: {self.airplane}. "
                f"Crew: {self.crew}. "
                f"Departure time: {self.departure_time}. Arrival time: {self.arrival_time}")


class Order(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name = "order"
    )

    @property
    def created_at(self):
        return datetime.now()
    
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
        related_name="tickets"
    )

    class Meta:
        unique_together = ("seat", "row")
        ordering = ("row", "seat",)

    def __str__(self):
        return (f"Ticket - Row: {self.row}. Seat: {self.seat}. "
                f"Flight: {self.flight.route}")
    
    @staticmethod
    def validate_seat(seat, seats_in_row, error_to_raise):
        if not (1 <= seat <= seats_in_row):
            raise error_to_raise({
                "seat": f"seat must be in range [1, {seats_in_row}]"
                })
    
    @staticmethod
    def validate_row(row, rows_in_plane, error_to_raise):
        if not (1 <= row <= rows_in_plane):
            raise error_to_raise({
            "rows": f"row must be in range [1, {rows_in_plane}]"   
            })


    def clean(self):
        Ticket.validate_seat(self.seat,
                             self.flight.airplane.seats_in_row,
                             ValidationError)
        Ticket.validate_row(self.row,
                            self.flight.airplane.rows,
                            ValidationError)