# songs/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path("", views.song_list, name="song_list"),
    path("add/", views.add_song, name="add_song"),
    path("edit/<int:song_id>/", views.edit_song, name="edit_song"),
    path('play/', views.play_song, name='play_song'),  # <-- ADD THIS

]
