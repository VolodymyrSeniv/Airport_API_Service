from django.urls import path, include
from rest_framework import routers
from user.views import CreateUserView


from rest_framework import routers

app_name = "user"

urlpatterns = [
    path("registration/", CreateUserView.as_view(), name="create")
]