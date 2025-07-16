from django.urls import path, include
from rest_framework import routers
from rest_framework.authtoken import views
from user.views import CreateUserView, LoginUserView


from rest_framework import routers

app_name = "user"

urlpatterns = [
    path("registration/", CreateUserView.as_view(), name="create"),
    path("login/", LoginUserView.as_view(), name="get_token")
]