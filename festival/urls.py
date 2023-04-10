from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("index", views.index, name="index"),
    path("festival/<int:festival_id>/", views.festival, name="festival"),
    path("artist", views.artist, name="artist"),
    path("test", views.test, name="test"),
    path("buy/<int:ticket_id>/", views.buy, name="buy"),
    path("artist/<int:artist_id>/", views.artist, name="artist"),

]
