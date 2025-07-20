from rest_framework import serializers
from airport_backend.models import (Crew,
                    AirplaneType,
                    Airplane,
                    Airport,
                    Route,
                    Flight,
                    Order,
                    Ticket)
from user.serializers import UserSerializer
from django.contrib.auth import get_user_model
from django.db import transaction


class CrewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crew
        fields = "__all__"
        read_only_fields=("id", "image")


class CrewImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crew
        fields = ("id", "image")


class AirplaneTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AirplaneType
        fields = "__all__"


class AirplaneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airplane
        fields = "__all__"
        read_only_fields=("id", "image")


class AirplaneListSerializer(serializers.ModelSerializer):
    type = serializers.CharField(source="airplane_type.name", read_only=True)
    total_seats = serializers.ReadOnlyField()

    class Meta:
        model = Airplane
        fields = ("id",
                  "name",
                  "rows",
                  "seats_in_row",
                  "type",
                  "total_seats",
                  "image",)


class AirplaneRetrieveSerializer(AirplaneSerializer):
    airplane_type = AirplaneTypeSerializer(many=False, read_only=True)


class AirplaneImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airplane
        fields = ("id", "image")


class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = "__all__"


class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route 
        fields = "__all__"


class RouteListSerializer(serializers.ModelSerializer):
    source_name = serializers.CharField(source="source.name", read_only=True)
    source_city = serializers.CharField(source="source.closest_big_city", read_only=True)
    dest_name = serializers.CharField(source="destination.name", read_only=True)
    dest_city = serializers.CharField(source="destination.closest_big_city", read_only=True)
    class Meta:
        model = Route 
        fields = ("id",
                  "source_name",
                  "source_city",
                  "dest_name",
                  "dest_city",
                  "distance"
                  )


class RouteRetrieveSerializer(RouteSerializer):
    source = AirportSerializer(many=False, read_only=True)
    destination = AirportSerializer(many=False, read_only=True)


class FlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = ("id",
                  "route",
                  "airplane",
                  "departure_time",
                  "arrival_time",
                  "crew")


class FlightListSerializer(serializers.ModelSerializer):
    route_source = serializers.CharField(source="route.source.name", read_only=True)
    route_destination = serializers.CharField(source="route.destination.name", read_only=True)
    route_distance = serializers.IntegerField(source="route.distance", read_only=True)
    airplane_type_name = serializers.CharField(source="airplane.airplane_type.name", read_only=True)
    airplane_name = serializers.CharField(source="airplane.name", read_only=True)
    crew = serializers.SlugRelatedField(many=True,
                                        read_only=True,
                                        slug_field = "first_name",)
    tickets_available = serializers.IntegerField(read_only=True)
    class Meta:
        model = Flight
        fields = ("id",
                  "route_source",
                  "route_destination",
                  "route_distance",
                  "airplane_type_name",
                  "airplane_name",
                  "departure_time",
                  "arrival_time",
                  "crew",
                  "tickets_available")


class FlightRetrieveSerialzier(FlightSerializer):
    route = RouteListSerializer(many=False, read_only=True)
    airplane = AirplaneListSerializer(many=False, read_only=True)
    crew = CrewSerializer(many=True, read_only = True)
    taken_seats = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="seat",
        source="ticket_flight"
    )
    class Meta:
        model = Flight
        fields = ("id",
                  "route",
                  "airplane",
                  "departure_time",
                  "arrival_time",
                  "crew",
                  "taken_seats")


class TicketSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        data = super(TicketSerializer, self).validate(attrs)
        Ticket.validate_seat(
            attrs["seat"],
            attrs["flight"].airplane.seats_in_row,
            serializers.ValidationError
        )
        Ticket.validate_row(
            attrs["row"],
            attrs["flight"].airplane.rows,
            serializers.ValidationError
        )
        return data

    class Meta:
        model = Ticket
        fields = ("id", "seat", "row", "flight")


class TicketListSerializer(TicketSerializer):
    flight = FlightListSerializer(read_only = True)



class OrderSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(many=True, read_only=False, allow_empty=False)
    created_at = serializers.ReadOnlyField()

    class Meta:
        model = Order
        fields = ["id", "created_at", "tickets"]
    
    def create(self, validated_data):
        with transaction.atomic():
            tickets_data = validated_data.pop("tickets")
            order = Order.objects.create(**validated_data)
            for ticket_data in tickets_data:
                Ticket.objects.create(order=order, **ticket_data)
            return order


class OrderListSerializer(OrderSerializer):
    created_at = serializers.ReadOnlyField()
    tickets = TicketListSerializer(read_only=True, many=True)

    class Meta:
        model = Order
        fields = ["id",
                  "created_at",
                  "tickets"]


class OrderRetrieveSerializer(OrderSerializer):
    user = UserSerializer(many = False, read_only = True)
    tickets = TicketListSerializer(read_only=True, many=True)

    class Meta:
        model = Order
        fields = ["id",
                  "created_at",
                  "tickets",
                  "user"]