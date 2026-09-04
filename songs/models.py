# songs/models.py

from django.db import models
from django.utils import timezone


class Artist(models.Model):
    """
    Each artist is a unique person/band.
    Maps to your 'artists' table.
    """
    artistName = models.TextField(unique=True)
    place = models.TextField(default='', blank=True)

    class Meta:
        db_table = 'artists'  # ← Forces Django to use YOUR existing table name
        # Without this, Django would create 'songs_artist'

    def __str__(self):
        # What shows up when you print an Artist object
        return self.artistName


class Genre(models.Model):
    """Maps to 'genres' table"""
    genreName = models.TextField(unique=True)

    class Meta:
        db_table = 'genres'

    def __str__(self):
        return self.genreName


class Language(models.Model):
    """Maps to 'languages' table"""
    langCode = models.TextField(unique=True)
    langName = models.TextField()

    class Meta:
        db_table = 'languages'

    def __str__(self):
        return f"{self.langName} ({self.langCode})"


class Tag(models.Model):
    """Maps to 'tags' table"""
    tagName = models.TextField(unique=True)

    class Meta:
        db_table = 'tags'

    def __str__(self):
        return self.tagName


class Album(models.Model):
    """Maps to 'album' table"""
    name = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'album'

    def __str__(self):
        return self.name or 'Unknown Album'


class Playlist(models.Model):
    """Maps to 'playlist' table"""
    playlist_id = models.AutoField(primary_key=True)
    name = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'playlist'

    def __str__(self):
        return self.name or 'Unnamed Playlist'


class MyTag(models.Model):
    """Maps to 'mytags' table"""
    name = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'mytags'

    def __str__(self):
        return self.name or ''


class Song(models.Model):
    """
    The MAIN table. Maps to 'songs' table.

    ManyToManyField = Django's way of handling junction/bridge tables
    (like song_artists, song_genres, etc.)
    """
    songName = models.TextField()
    album = models.TextField(default='', blank=True)
    year = models.TextField(default='', blank=True)
    songLength = models.TextField(default='', blank=True)
    playCount = models.IntegerField(default=0)
    isrc = models.TextField(default='', blank=True)

    SOURCE_CHOICES = [
        ('manual', 'Manual'),
        ('youtube', 'YouTube'),
        ('spotify', 'Spotify'),
    ]
    source = models.TextField(default='manual')
    filePath = models.TextField(default='', blank=True)
    addedDate = models.TextField(default='', blank=True)

    # ── Many-to-Many Relationships ──
    # These use YOUR existing bridge tables

    artists = models.ManyToManyField(
        Artist,
        through='SongArtist',       # ← tells Django to use our custom bridge table
        related_name='songs',        # ← lets you do: artist.songs.all()
        blank=True,
    )

    genres = models.ManyToManyField(
        Genre,
        through='SongGenre',
        related_name='songs',
        blank=True,
    )

    languages = models.ManyToManyField(
        Language,
        through='SongLanguage',
        related_name='songs',
        blank=True,
    )

    tags = models.ManyToManyField(
        Tag,
        through='SongTag',
        related_name='songs',
        blank=True,
    )

    albums = models.ManyToManyField(
        Album,
        through='SongAlbum',
        related_name='songs',
        blank=True,
    )

    playlists = models.ManyToManyField(
        Playlist,
        through='SongPlaylist',
        related_name='songs',
        blank=True,
    )

    mytags = models.ManyToManyField(
        MyTag,
        through='SongMyTag',
        related_name='songs',
        blank=True,
    )

    class Meta:
        db_table = 'songs'

    def __str__(self):
        return self.songName


# ══════════════════════════════════════════
#  BRIDGE / JUNCTION TABLES (Many-to-Many)
# ══════════════════════════════════════════
# These are the "through" models — they map to your existing bridge tables.

class SongArtist(models.Model):
    """
    Maps to 'song_artists' table.
    'through' model = custom bridge table with extra fields (like 'role').
    """
    song = models.ForeignKey(Song, on_delete=models.CASCADE, db_column='song_id')
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, db_column='artist_id')

    ROLE_CHOICES = [
        ('primary', 'Primary'),
        ('featured', 'Featured'),
        ('producer', 'Producer'),
        ('composer', 'Composer'),
    ]
    role = models.TextField(default='primary')

    class Meta:
        db_table = 'song_artists'
        unique_together = ('song', 'artist')
        # unique_together = composite primary key
        # Means: same artist can't be linked to same song twice

    def __str__(self):
        return f"{self.song.songName} - {self.artist.artistName} ({self.role})"


class SongGenre(models.Model):
    """Maps to 'song_genres' table"""
    song = models.ForeignKey(Song, on_delete=models.CASCADE, db_column='song_id')
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, db_column='genre_id')

    class Meta:
        db_table = 'song_genres'
        unique_together = ('song', 'genre')


class SongLanguage(models.Model):
    """Maps to 'song_languages' table"""
    song = models.ForeignKey(Song, on_delete=models.CASCADE, db_column='song_id')
    lang = models.ForeignKey(Language, on_delete=models.CASCADE, db_column='lang_id')

    class Meta:
        db_table = 'song_languages'
        unique_together = ('song', 'lang')


class SongTag(models.Model):
    """Maps to 'song_tags' table"""
    song = models.ForeignKey(Song, on_delete=models.CASCADE, db_column='song_id')
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, db_column='tag_id')
    tagType = models.TextField(default='myTag')

    class Meta:
        db_table = 'song_tags'
        unique_together = ('song', 'tag')


class SongAlbum(models.Model):
    """Maps to 'song_album' table"""
    song = models.ForeignKey(Song, on_delete=models.CASCADE, db_column='song_id')
    album = models.ForeignKey(Album, on_delete=models.CASCADE, db_column='album_id')

    class Meta:
        db_table = 'song_album'
        unique_together = ('song', 'album')


class SongPlaylist(models.Model):
    """Maps to 'song_playlist' table"""
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE, db_column='playlist_id')
    song = models.ForeignKey(Song, on_delete=models.CASCADE, db_column='song_id')

    class Meta:
        db_table = 'song_playlist'
        unique_together = ('playlist', 'song')


class SongMyTag(models.Model):
    """Maps to 'song_mytags' table"""
    song = models.ForeignKey(Song, on_delete=models.CASCADE, db_column='song_id')
    mytag = models.ForeignKey(MyTag, on_delete=models.CASCADE, db_column='mytags')

    class Meta:
        db_table = 'song_mytags'
        unique_together = ('song', 'mytag')


class ExternalId(models.Model):
    """Maps to 'external_ids' table"""
    song = models.ForeignKey(Song, on_delete=models.CASCADE, db_column='song_id',
                             related_name='external_ids')
    PLATFORM_CHOICES = [
        ('youtube', 'YouTube'),
        ('spotify', 'Spotify'),
        ('apple', 'Apple Music'),
        ('soundcloud', 'SoundCloud'),
    ]
    platform = models.TextField()
    externalID = models.TextField()

    class Meta:
        db_table = 'external_ids'
        unique_together = ('song', 'platform')

    def __str__(self):
        return f"{self.platform}: {self.externalID}"
