# musicmanager/urls.py  (EDIT this existing file)

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('songs/', include('songs.urls')),
    # include() = "go look at songs/urls.py for more routes"
    # All songs app URLs will be under /songs/...
]