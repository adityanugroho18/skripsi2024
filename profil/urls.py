from django.urls import path
from .views import *

urlpatterns = [
    path("", index, name="profile.index"),
    path("save", save, name="profile.save"),
    path("change-password", change_password, name="profile.change_password"),
    path("change-password/save", save_password, name="profile.change_password_save"),
]
