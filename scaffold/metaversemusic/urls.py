from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import PlaylistListView, PlaylistDetailView, PlaylistCreateView, ChartsListView, ChartsDetailView

app_name = "metaversemusic"

urlpatterns = [
    path('playlists/', PlaylistListView.as_view(), name='playlist-list'),
    path('playlists/<int:pk>/', PlaylistDetailView.as_view(), name='playlist-detail'),
    path('playlists/create/', PlaylistCreateView.as_view(), name='playlist-create'),
    path('charts/', ChartsListView.as_view(), name='charts-list'),
    path('charts/<int:pk>/', ChartsDetailView.as_view(), name='charts-detail'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
