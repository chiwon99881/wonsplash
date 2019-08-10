from django.urls import path
from . import views

app_name = "collects"
urlpatterns = [
    path("", view=views.Feed.as_view(), name="feed")
]
