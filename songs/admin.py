# songs/admin.py
from django.contrib import admin
from .models import Artist, Genre, Language, Tag, MyTag, Album

# This registers your tables so they appear in the Admin Panel
admin.site.register(Artist)
admin.site.register(Genre)
admin.site.register(Language)
admin.site.register(Tag)
admin.site.register(MyTag)
admin.site.register(Album)
