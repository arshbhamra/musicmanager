# songs/forms.py

from django import forms
from .models import (
    Song, Artist, Genre, Language, Tag, Album, MyTag, ExternalId, SongArtist
)


class SongForm(forms.Form):
    """
    Why forms.Form and not ModelForm?

    Because our data is spread across MANY tables (songs, song_artists,
    song_genres, etc.). A ModelForm only handles ONE model.
    So we build a custom form and handle the saving logic ourselves in the view.
    """

    # ── Song basic info ──
    songName = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',         # Bootstrap CSS class
            'placeholder': 'Song name...'
        })
    )

    album = forms.CharField(
        max_length=200,
        required=False,                       # Not mandatory
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Album name...'
        })
    )

    year = forms.CharField(
        max_length=4,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '2024'
        })
    )

    songLength = forms.CharField(
        max_length=10,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '3:45'
        })
    )

    isrc = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'ISRC code...'
        })
    )

    source = forms.ChoiceField(
        choices=[
            ('manual', 'Manual'),
            ('youtube', 'YouTube'),
            ('spotify', 'Spotify'),
        ],
        initial='manual',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    filePath = forms.CharField(
        max_length=500,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '/path/to/file.mp3'
        })
    )

    # ── Artists ──
    # Free text, comma separated: "Eminem, Dr. Dre, 50 Cent"
    artists = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Artist1, Artist2, Artist3...'
        }),
        help_text='Comma separated artist names'
    )

    # ── Genres ──
    genres = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Hip-Hop, Rap, Pop...'
        }),
        help_text='Comma separated genres'
    )

    # ── Languages ──
    languages = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'en, hi, pa...'
        }),
        help_text='Comma separated language codes (en, hi, pa, etc.)'
    )

    # ── Tags ──
    tags = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'chill, workout, driving...'
        }),
        help_text='Comma separated tags'
    )

    # ── My Custom Tags ──
    my_tags = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'fav, top10, nostalgia...'
        }),
        help_text='Comma separated personal tags'
    )

    # ── External IDs ──
    youtube_id = forms.CharField(
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'dQw4w9WgXcQ'
        })
    )

    spotify_id = forms.CharField(
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'spotify:track:xxx'
        })
    )
