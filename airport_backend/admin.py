from django.contrib import admin
from airport_backend.models import (Crew,
                                    Order,
                                    Airplane,
                                    AirplaneType,
                                    Airport,
                                    Route,
                                    Flight,
                                    Ticket)

admin.site.register(Crew)
admin.site.register(Order)
admin.site.register(Airport)
admin.site.register(Airplane)
admin.site.register(AirplaneType)
admin.site.register(Route)
admin.site.register(Flight)
admin.site.register(Ticket)