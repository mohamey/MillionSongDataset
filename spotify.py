#! /usr/bin/python3

from os import environ
import spotipy
import spotipy.util as util

class SpotifyWrapper:
    def __init__(self, config):
        # Set Environment Variables
        environ["SPOTIPY_CLIENT_ID"] = config["spotify"]["client_id"]
        environ["SPOTIPY_CLIENT_SECRET"] = config["spotify"]["client_secret"]
        environ["SPOTIPY_REDIRECT_URI"] = config["spotify"]["redirect_uri"]

        self.scope = config["spotify"]["scope"]
        self.username = config["spotify"]["username"]
        self.spotify = None
        self.filtered_artists = set()

        self.song_uri_dict = {}

    # String formatting for artists, reduce collaborations to single artist
    def format_artist(self, artist):
        final_artist_string = artist
        stop_words = ["/", " Feat", " feat ", " ft ", " Vs", " vs"]

        for stop_word in stop_words:
            if stop_word in final_artist_string:
                end = final_artist_string.index(stop_word)
                final_artist_string = final_artist_string[:end].strip()

        return final_artist_string

    def format_song(self, song):
        final_song_string = song
        stop_words = ["/", " Feat", " feat ", " ft ", " Vs", " vs", '(', '[', '?', '!']

        for stop_word in stop_words:
            if stop_word in final_song_string:
                end = final_song_string.index(stop_word)
                final_song_string = final_song_string[:end].strip()

        return final_song_string

    def authorize_user(self):
        print("Authorizing")
        token = util.prompt_for_user_token(self.username, self.scope)
        print(token)
        self.spotify = spotipy.Spotify(auth=token)

    def get_artist_uris(self, artists):
        print(artists)
        return [self.get_artist_uri(artist) for artist in artists]

    def get_artist_uri(self, artist):
        if not self.spotify:
            print("Spotify Object not yet authorized")
            return

        try:
            results = self.spotify.search(q=artist, type="artist")
        except spotipy.client.SpotifyException:
            self.authorize_user()
            results = self.spotify.search(q=artist, type="artist")

        artist_uri = None
        for artist_result in results["artists"]["items"]:
            if artist_result["name"].lower() == artist.lower():
                artist_uri = artist_result["uri"]
                break

        if not artist_uri:
            for artist_result in results["artists"]["items"]:
                if artist.lower() in artist_result["name"].lower():
                    artist_uri = artist_result["uri"]

        print(artist_uri)
        return artist_uri

    def get_song_uri(self, song_artist_key):
        if not self.spotify:
            print("Spotify Object not yet authorized")
            return

        song, artist = map(str.strip, song_artist_key.split("<SEP>"))
        song = self.format_song(song)
        artist = self.format_artist(artist)
        # print(song)
        # print(artist)

        if not song:
            return None

        try:
            results = self.spotify.search(q=song, type="track")
        except spotipy.client.SpotifyException:
            self.authorize_user()
            results = self.spotify.search(q=song, type="track")

        song_uri = None
        for item in results["tracks"]["items"]:
            # if item["name"].lower() == song.lower():
            for artist_item in item["artists"]:
                if self.format_artist(artist_item["name"]).lower() == artist.lower():
                    song_uri = item["uri"].split(":")[2]
                    break

        return song_uri

    def get_recommendations(self, artist_uris, num_artists=100):
        if not self.spotify:
            print("Spotify object not yet authorized")
            return

        artist_uris = [ar for ar in artist_uris if ar]
        seed_uris = artist_uris[:5]
        print(seed_uris)

        recommended_artists = set()
        while len(recommended_artists) < num_artists:
            print("Need {} more artists".format(num_artists - len(recommended_artists)))
            try:
                recommendations = self.spotify.recommendations(seed_artists=seed_uris, limit=100)
            except spotipy.client.SpotifyException:
                self.authorize_user()
                recommendations = self.spotify.recommendations(seed_artists=seed_uris, limit=100)

            for track in recommendations["tracks"]:
                artist = track["artists"][0]
                artist_name = artist["name"]
                artist_uri = artist["uri"]
                if not self.check_new_artist(artist_uri, name=artist_name):
                    recommended_artists.add(artist_name)
                else:
                    self.filtered_artists.add(artist_name)

                if len(recommended_artists) == num_artists:
                    break
                elif len(recommended_artists) == num_artists / 2:
                    seed_uris = artist_uris[-5:]
                    print(seed_uris)
                    break

        return recommended_artists

    def check_new_artist(self, artist_uri, name=None):
        if name and name in self.filtered_artists:
            return True

        try:
            albums = self.spotify.artist_albums(artist_uri)
        except spotipy.client.SpotifyException:
            self.authorize_user()
            albums = self.spotify.artist_albums(artist_uri)

        result = True
        for album in albums["items"]:
            release_year = int(album["release_date"][:4])
            if release_year < 2012:
                result = False
                break

        return result

    def filter_new_artists(self, artists):
        valid_artists = []
        for artist in artists:
            id = self.get_artist_uri(artist)
            if not self.check_new_artist(id, name=artist):
                valid_artists.append(artist)
            else:
                self.filtered_artists.add(artist)

        return valid_artists
