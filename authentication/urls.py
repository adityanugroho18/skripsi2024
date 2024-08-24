from django.urls import path
from .views import AuthenticationView, LogoutView

urlpatterns = [
    path("", AuthenticationView.as_view(), name="root"),
    path("login/", AuthenticationView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout")
]
