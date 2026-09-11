# songs/views.py
from datetime import date
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
import subprocess


from .models import (
    Song,
    Artist,
    Genre,
    Language,
    Tag,
    Album,
    MyTag,
    SongArtist,
    SongGenre,
    SongLanguage,
    SongTag,
    SongAlbum,
    SongMyTag,
    ExternalId,
)


def get_db_options():
    """Helper function to get all available options for our checkboxes"""
    return {
        "artists": Artist.objects.all().order_by("artistName"),
        "genres": Genre.objects.all().order_by("genreName"),
        "languages": Language.objects.all().order_by("langName"),
        "tags": Tag.objects.all().order_by("tagName"),
        "mytags": MyTag.objects.all().order_by("name"),
    }


def song_list(request):
    songs = (
        Song.objects.all()
        .order_by("-id")
        .prefetch_related(
            "artists", "genres", "languages", "tags", "mytags", "external_ids"
        )
    )
    context = {"songs": songs, **get_db_options()}
    return render(request, "songs/songList.html", context)


def add_song(request):
    if request.method == "POST":
        # 1. Create Song basic text fields
        song = Song.objects.create(
            songName=request.POST.get("songName"),
            album=request.POST.get("album", ""),
            year=request.POST.get("year", ""),
            songLength=request.POST.get("songLength", ""),
            isrc=request.POST.get("isrc", ""),
            addedDate=str(date.today()),
        )

        # 2. Save Relations using Checkbox IDs
        _save_relations(request, song)

        messages.success(request, f'🎵 "{song.songName}" added successfully!')
        return redirect("add_song")

    # GET request: show form
    return render(request, "songs/addSong.html", get_db_options())


def edit_song(request, song_id):
    if request.method == "POST":
        song = get_object_or_404(Song, id=song_id)

        # 1. Update basic text fields
        song.songName = request.POST.get("songName", song.songName)
        song.album = request.POST.get("album", song.album)
        song.year = request.POST.get("year", song.year)
        song.songLength = request.POST.get("songLength", song.songLength)
        song.isrc = request.POST.get("isrc", song.isrc)

        if request.POST.get("playCount", "").isdigit():
            song.playCount = int(request.POST["playCount"])

        song.save()

        # 2. Clear old relations and save new ones
        SongArtist.objects.filter(song=song).delete()
        SongGenre.objects.filter(song=song).delete()
        SongLanguage.objects.filter(song=song).delete()
        SongTag.objects.filter(song=song).delete()
        SongMyTag.objects.filter(song=song).delete()

        _save_relations(request, song)

        messages.success(request, f'"{song.songName}" updated successfully!')

    return redirect("song_list")


def _save_relations(request, song):
    """Helper function to read checkbox IDs and save them to bridge tables"""
    # .getlist() gets ALL checked boxes with that name
    for a_id in request.POST.getlist("artists"):
        artist = Artist.objects.filter(id=a_id).first()
        if artist:
            SongArtist.objects.create(song=song, artist=artist, role="primary")

    for g_id in request.POST.getlist("genres"):
        genre = Genre.objects.filter(id=g_id).first()
        if genre:
            SongGenre.objects.create(song=song, genre=genre)

    for l_id in request.POST.getlist("languages"):
        lang = Language.objects.filter(id=l_id).first()
        if lang:
            SongLanguage.objects.create(song=song, lang=lang)

    for t_id in request.POST.getlist("tags"):
        tag = Tag.objects.filter(id=t_id).first()
        if tag:
            SongTag.objects.create(song=song, tag=tag, tagType="myTag")

    for mt_id in request.POST.getlist("mytags"):
        mytag = MyTag.objects.filter(id=mt_id).first()
        if mytag:
            SongMyTag.objects.create(song=song, mytag=mytag)



def play_song(request):
    title = request.GET.get('title', '').strip()
    artist = request.GET.get('artist', '').strip()
    query = f"{title} {artist}".strip()

    if not title:
        return JsonResponse({"error": "No song selected"}, status=400)

    try:
        cmd = [
            "yt-dlp",
            "-f", "bestaudio",
            "-g",                     # get URL only, no download
            "--no-playlist",          # faster: don't parse playlists
            "--no-warnings",
            "--quiet",
            f"ytsearch1:{query}",
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=25)
        url = result.stdout.strip().split("\n")[0].strip()

        if url and url.startswith("http"):
            return JsonResponse({"url": url})
        return JsonResponse({"error": "No audio found"}, status=404)

    except subprocess.TimeoutExpired:
        return JsonResponse({"error": "yt-dlp timed out"}, status=504)
    except FileNotFoundError:
        return JsonResponse({"error": "yt-dlp not installed on server"}, status=500)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)