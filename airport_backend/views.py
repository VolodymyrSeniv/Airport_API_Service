
from airport_backend.models import (Crew,
                                    AirplaneType,
                                    Airplane, 
                                    Airport,
                                    Route,
                                    Flight,
                                    Order,
                                    Ticket,
                                    Country,
                                    City)
from airport_backend.pagination import SmallClassesPagination, HugeClassesPagination
from django.contrib.auth import get_user_model
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
from airport_backend.serializers import (CrewSerializer,
                                         AirplaneTypeSerializer,
                                         AirplaneSerializer,
                                         AirplaneListSerializer,
                                         AirplaneRetrieveSerializer,
                                         AirportSerializer,
                                         RouteSerializer,
                                         RouteListSerializer,
                                         RouteRetrieveSerializer,
                                         FlightSerializer,
                                         FlightListSerializer,
                                         FlightRetrieveSerialzier,
                                         UserSerializer,
                                         OrderSerializer,
                                         OrderListSerializer,
                                         OrderRetrieveSerializer,
                                         TicketSerializer,
                                         TicketListSerializer,
                                         CrewImageSerializer,
                                         CrewListSerializer,
                                         AirplaneImageSerializer,
                                         CountrySerializer,
                                         CitySerializer,
                                         CityListSerializer,
                                         CityImageSerializer,
                                         CityRetreiveSerializer,
                                         AirportListSerializer,
                                         AirportRetreiveSerializer)
from rest_framework import viewsets
from airport_backend.permission import (IsAdminOrIfAuthenticatedReadOnly, 
                                        OnlyAdminPermnissions,
                                        IsAuthenticated)
from django.db.models import F, Count
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes


class CrewModelViewSet(viewsets.ModelViewSet):
    serializer_class = CrewSerializer
    queryset = Crew.objects.all()
    pagination_class = SmallClassesPagination
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)

    def get_serializer_class(self):
        if self.action == "list":
            return CrewListSerializer
        if self.action == "upload_image":
            return CrewImageSerializer
        return CrewSerializer
    
    @action(
            methods={"POST"},
            detail=True,
            permission_classes=(OnlyAdminPermnissions,),
            url_path="upload-image",
    )
    def upload_image(self, request, pk=None):
        crew = self.get_object()
        serializer = CrewImageSerializer(crew, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CountryViewSet(viewsets.ModelViewSet):
    serializer_class = CountrySerializer
    queryset = Country.objects.all()
    pagination_class = SmallClassesPagination
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)


class CityViewSet(viewsets.ModelViewSet):
    serializer_class = CitySerializer
    queryset = City.objects.all()
    pagination_class = SmallClassesPagination
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)

    def get_serializer_class(self):
        if self.action == "list":
            return CityListSerializer
        if self.action == "upload_image":
            return CityImageSerializer
        if self.action == "retrieve":
            return CityRetreiveSerializer
        return CitySerializer
    

    @action(
        methods={"POST"},
        detail=True,
        permission_classes=(OnlyAdminPermnissions,),
        url_path="upload-image",
    )
    def upload_image(self, request, pk=None):
        city = self.get_object()
        serializer = CityImageSerializer(city, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get_queryset(self):
        queryset = self.queryset
        if self.action in ("list", "retrieve"):
            queryset = queryset.select_related("country")
        return queryset


class AirplaneTypeViewSet(viewsets.ModelViewSet):
    serializer_class = AirplaneTypeSerializer
    queryset = AirplaneType.objects.all()
    pagination_class = SmallClassesPagination
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)


class AirplaneViewSet(viewsets.ModelViewSet):
    serializer_class = AirplaneSerializer
    queryset = Airplane.objects.all()
    pagination_class = SmallClassesPagination
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)

    def get_serializer_class(self):
        if self.action == "list":
            return AirplaneListSerializer
        if self.action == "retrieve":
            return AirplaneRetrieveSerializer
        if self.action == "upload_image":
            return AirplaneImageSerializer
        return AirplaneSerializer
    
    @action(
            methods={"POST"},
            detail=True,
            permission_classes=(OnlyAdminPermnissions,),
            url_path="upload-image",
    )
    def upload_image(self, request, pk=None):
        airplane = self.get_object()
        serializer = AirplaneImageSerializer(airplane, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        queryset = self.queryset
        if self.action in ("list", "retrieve"):
            queryset = queryset.select_related("airplane_type")
        return queryset


class AirportViewSet(viewsets.ModelViewSet):
    serializer_class = AirportSerializer
    queryset = Airport.objects.all()
    pagination_class = SmallClassesPagination
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)

    def get_serializer_class(self):
        if self.action == "list":
            return AirportListSerializer
        if self.action == "retreive":
            return AirportRetreiveSerializer
        return AirportSerializer
    
    def get_queryset(self):
        queryset = self.queryset
        if self.action in ("list", "retrieve"):
            queryset = queryset.select_related("closest_big_city")
        return queryset


class RouteViewSet(viewsets.ModelViewSet):
    serializer_class = RouteSerializer
    queryset = Route.objects.select_related("source", "destination")
    pagination_class = SmallClassesPagination
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)

    def get_serializer_class(self):
        if self.action == "list":
            return RouteListSerializer
        if self.action == "retrieve":
            return RouteRetrieveSerializer
        return RouteSerializer


class FlightViewSet(viewsets.ModelViewSet):
    serializer_class = FlightSerializer
    queryset = (
        Flight.objects
        # join Flight → Route → source Airport
        .select_related("route__source")
        # join Flight → Route → destination Airport
        .select_related("route__destination")
        # join Flight → Airplane → AirplaneType
        .select_related("airplane__airplane_type")
        # prefetch the M2M “crew” in one extra query
        .prefetch_related("crew")
    )
    pagination_class = HugeClassesPagination
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)

    def get_serializer_class(self):
        if self.action == "list":
            return FlightListSerializer
        if self.action == "retrieve":
            return FlightRetrieveSerialzier
        return FlightSerializer
    

    @staticmethod
    def _params_to_ints(qs):
        return [int(str_id) for str_id in qs.split(",")]
    

    def get_queryset(self):
        queryset = self.queryset
        source = self.request.query_params.get("source")
        destination = self.request.query_params.get("destination")
        departure_time = self.request.query_params.get("departure_time")
        arrival_time = self.request.query_params.get("arrival_time")

        if source and destination:
            source_ids = self._params_to_ints(source)
            destination_ids = self._params_to_ints(destination)
            queryset =  queryset.filter(
                route__source__id__in=source_ids,
                route__destination__id__in=destination_ids
            )

        if source:
            source_ids = self._params_to_ints(source)
            queryset =  queryset.filter(route__source__id__in=source_ids)

        if destination:
            destination_ids = self._params_to_ints(destination)
            queryset =  queryset.filter(route__destination__id__in=destination_ids)
        
        if departure_time:
            date = datetime.strptime(date, "%Y-%m-%d").date()
            queryset = queryset.filter(departure_time__date=date)
        
        if arrival_time:
            arrival_time = datetime.strptime(date, "%Y-%m-%d").date()
            queryset = queryset.filter(arrival_time__date=date)

        if self.action in("list", "retrieve"):
            queryset = queryset.select_related(
            "route__source",
            "route__destination",
            "airplane__airplane_type",
        ).prefetch_related(
                "crew"
                ).annotate(
                    tickets_available=(F("airplane__rows") * F("airplane__seats_in_row")) - Count("ticket_flight")
                    )
        return queryset
    
    @extend_schema(
        parameters=[
            OpenApiParameter(
                "source",
                type=OpenApiTypes.INT,
                description="Filter by source id (ex. ?source=2)",
            ),
            OpenApiParameter(
                "destination",
                type=OpenApiTypes.INT,
                description=(
                    "Filter by destination id (ex. ?destination=2) "
                ),
            ),
            OpenApiParameter(
                "departure_time",
                type=OpenApiTypes.DATE,
                description=(
                    "Filter by daparture date of a Flight"
                    "(ex. ?departure_time=2022-10-23)"
                ),
            ),
            OpenApiParameter(
                "arrival_time",
                type=OpenApiTypes.DATE,
                description=(
                    "Filter by arrival date of a Flight"
                    "(ex. ?arrival_time=2022-10-23)"
                ),
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = get_user_model().objects.all()
    pagination_class = SmallClassesPagination
    permission_classes = (OnlyAdminPermnissions,)


class TicketViewSet(viewsets.ModelViewSet):
    serializer_class = TicketSerializer
    queryset = Ticket.objects.all()
    pagination_class = HugeClassesPagination
    permission_classes = (OnlyAdminPermnissions,)


    def get_serializer_class(self):
        if self.action == "list":
            return TicketListSerializer
        return TicketSerializer
    
    def get_queryset(self):
        queryset = self.queryset
        if self.action == "list":
            queryset = queryset.select_related("flight__airplane__airplane_type",
                                               "flight__route__source",
                                               "flight__route__destination"
                                               ).prefetch_related("flight__crew",)
        return queryset


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    pagination_class = HugeClassesPagination
    permission_classes = (IsAuthenticated,)


    def get_serializer_class(self):
        if self.action == "list":
            return OrderListSerializer
        if self.action == "retrieve":
            return OrderRetrieveSerializer
        return OrderSerializer
    
    def get_queryset(self):
        queryset = self.queryset.filter(user = self.request.user)
        if self.action in ("list", "retrieve"):
            queryset = queryset.select_related("user", ).prefetch_related("tickets__flight__airplane__airplane_type",
                                                                        "tickets__flight__crew",
                                                                        "tickets__flight__route__source",
                                                                        "tickets__flight__route__destination")
        return queryset
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
