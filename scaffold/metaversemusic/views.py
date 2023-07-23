from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView
from .models import Playlist, Charts


class PlaylistListView(LoginRequiredMixin, ListView):
    model = Playlist
    template_name = 'metaversemusic/playlist_list.html'
    context_object_name = 'playlists'
    paginate_by = 10


class PlaylistDetailView(LoginRequiredMixin, DetailView):
    model = Playlist
    template_name = 'metaversemusic/playlist_detail.html'
    context_object_name = 'playlist'


class PlaylistCreateView(LoginRequiredMixin, CreateView):
    model = Playlist
    template_name = 'metaversemusic/playlist_create.html'
    fields = ['name', 'song_ids', 'tags']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ChartsListView(ListView):
    model = Charts
    template_name = 'metaversemusic/chart_list.html'
    context_object_name = 'charts'
    paginate_by = 10


class ChartsDetailView(DetailView):
    model = Charts
    template_name = 'metaversemusic/chart_detail.html'
    context_object_name = 'chart'
