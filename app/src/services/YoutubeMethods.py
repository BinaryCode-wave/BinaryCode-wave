import src.services.YoutubeAPI as yt
import os
import json
import tempfile
from decouple import config

api_service_name = "youtube"
api_version = "v3"

client_credentials = json.loads(config('CLIENT_CREDENTIALS'))
client_secrets_file = "YOUR_CLIENT_SECRET_FILE.json"

with open(client_secrets_file, 'w') as json_file:
    json.dump(client_credentials, json_file)

scopes = scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]
youtube = yt.create_service(client_secrets_file, api_service_name, api_version, scopes)

os.remove(client_secrets_file)

# Recover plastlists
def get_playlists(youtube):
    request = youtube.playlists().list(
        part="snippet",
        mine=True
    )
    response = request.execute()
    return response

# Create playlist
def create_playlist(youtube, title):
    request = youtube.playlists().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": title
            },
            "status": {
                "privacyStatus": "unlisted"
            }
        }
    )
    response = request.execute()
    return response["id"]

# Delete playlist
def delete_playlist(youtube, playlist_id):
    request = youtube.playlists().delete(
        id=playlist_id
    )
    request.execute()

# Add video to playlist
def add_video(youtube, playlist_id, video_id):
    request = youtube.playlistItems().insert(
        part="snippet",
        body={
            "snippet": {
                "playlistId": playlist_id,
                "resourceId": {
                    "kind": "youtube#video",
                    "videoId": video_id
                }
            }
        }
    )
    response = request.execute()
    return response

def init(songs):
    playlist_id = ""
    playlists = get_playlists(youtube)["items"]
    for playlist in playlists:
        if playlist["snippet"]["title"] == "TempList":
            delete_playlist(youtube, playlist["id"])
            break

    playlist_id = create_playlist(youtube, "TempList")
    for song in songs:
        track = song.split("=")[1]
        add_video(youtube, playlist_id, track)

    print(playlist_id)
    return playlist_id
# run_local_server()