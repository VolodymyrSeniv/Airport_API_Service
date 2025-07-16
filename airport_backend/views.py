
from airport_backend.models import (Crew,
                                    AirplaneType,
                                    Airplane, 
                                    Airport,
                                    Route,
                                    Flight,
                                    Order,
                                    Ticket)
from airport_backend.pagination import SmallClassesPagination, HugeClassesPagination
from django.contrib.auth import get_user_model
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
                                         TicketListSerializer)
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from airport_backend.permission import (IsAdminOrIfAuthenticatedReadOnly, 
                                        OnlyAdminPermnissions,
                                        IsAuthenticated)
from django.db.models import F, Count


class CrewModelViewSet(viewsets.ModelViewSet):
    serializer_class = CrewSerializer
    queryset = Crew.objects.all()
    pagination_class = SmallClassesPagination
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)


class AirplaneTypeViewSet(viewsets.ModelViewSet):
    serializer_class = AirplaneTypeSerializer
    queryset = AirplaneType.objects.all()
    pagination_class = SmallClassesPagination
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)


class AirplaneViewSet(viewsets.ModelViewSet):
    serializer_class = AirplaneSerializer
    queryset = Airplane.objects.all()
    pagination_class = SmallClassesPagination
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)

    def get_serializer_class(self):
        if self.action == "list":
            return AirplaneListSerializer
        if self.action == "retrieve":
            return AirplaneRetrieveSerializer
        return AirplaneSerializer

    def get_queryset(self):
        queryset = self.queryset
        if self.action in ("list", "retrieve"):
            queryset = queryset.select_related("airplane_type")
        return queryset


class AirportViewSet(viewsets.ModelViewSet):
    serializer_class = AirportSerializer
    queryset = Airport.objects.all()
    pagination_class = SmallClassesPagination
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)


class RouteViewSet(viewsets.ModelViewSet):
    serializer_class = RouteSerializer
    queryset = Route.objects.select_related("source", "destination")
    pagination_class = SmallClassesPagination
    authentication_classes = (TokenAuthentication,)
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
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)

    def get_serializer_class(self):
        if self.action == "list":
            return FlightListSerializer
        if self.action == "retrieve":
            return FlightRetrieveSerialzier
        return FlightSerializer
    
    def get_queryset(self):
        queryset = self.queryset
        crew = self.request.query_params.get("crew")

        if crew:
            crew_ids = [int(str_id) for str_id in crew.split(",")]
            queryset =  queryset.filter(crew__id__in=crew_ids)

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


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = get_user_model().objects.all()
    pagination_class = SmallClassesPagination
    authentication_classes = (TokenAuthentication,)
    permission_classes = (OnlyAdminPermnissions,)


class TicketViewSet(viewsets.ModelViewSet):
    serializer_class = TicketSerializer
    queryset = Ticket.objects.all()
    pagination_class = HugeClassesPagination
    authentication_classes = (TokenAuthentication,)
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
    authentication_classes = (TokenAuthentication,)
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
