from django.urls import path
from .views import *

urlpatterns = [
    path("", index, name="user.index"),
    path("create/", create, name="user.create"),
    path("store/", store, name="user.store"),
    path("edit/<int:id>/", edit, name="user.edit"),
    path("update/<int:id>/", update, name="user.update"),
    path("delete/<int:id>/", delete, name="user.delete"),
]