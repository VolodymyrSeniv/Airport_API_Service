from rest_framework import serializers
from models import (Crew,
                    AirplaneType,
                    Airplane,
                    Airport,
                    Route,
                    Flight,
                    Order,
                    Ticket)
from user.models import User
from django.contrib.auth import get_user_model


# class CrewSerializer(serializers.Serializer):
#     first_name = serializers.CharField(max_length=100)
#     last_name = serializers.CharField(max_length=100)

#     def create(self, validated_data):
#         return Crew.objects.create(**validated_data)
    
#     def update(self, instance, validated_data):
#         instance.first_name = validated_data.get("first_name",
#                                                  instance.first_name)
#         instance.last_name = validated_data.get("last_name",
#                                                 instance.last_name)
#         instance.save()
#         return instance

class CrewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crew
        fields = "__all__"
    

# class AirplaneTypeSerializer(serializers.Serializer):
#     name = serializers.CharField(max_length=100)

#     def create(self, validated_data):
#         return AirplaneType.objects.create(**validated_data)
    
#     def update(self, instance, validated_data):
#         instance.first_name = validated_data.get("name")
#         instance.save()
#         return instance


class AirplaneTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AirplaneType
        fields = "__all__"


class AirplaneSerializer(serializers.ModelSerializer):
    airplane_type = AirplaneTypeSerializer()

    class Meta:
        model = Airplane
        fields = "__all__"


class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = "__all__"


class RouteSerializer(serializers.ModelSerializer):
    source = AirportSerializer()
    destination = AirportSerializer()
    
    class Meta:
        model = Route 
        fields = "__all__"


class FlightSerializer(serializers.ModelSerializer):
    route = RouteSerializer()
    airplane = AirplaneSerializer()
    crew = CrewSerializer(many=True)

    class Meta:
        model = Flight
        fields = "__all__"
    

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class OrderSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Order
        fields = "__all__"


class TicketSerializer(serializers.ModelSerializer):
    flight = FlightSerializer()
    order = OrderSerializer()

    class Meta:
        model = Ticket
        Fields = "__all__"

