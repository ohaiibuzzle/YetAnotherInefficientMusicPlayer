import asyncio
import requests

class PlaybackTrack:
    def __init__(self, id: str, name: str, url: str, artist: str = "", album: str = "", duration: int = "", icon_url: str = ""):
        self.id = id
        self.name = name
        self.artist = artist
        self.album = album
        self.duration = duration
        self.url = url
        self.icon_url = icon_url
    
    def __str__(self):
        return f"{self.artist} - {self.name}"
    
    def get_track_icon(self):
        return requests.get(self.icon_url).content
    
    async def async_get_track_icon(self):
        return await asyncio.get_event_loop().run_in_executor(None, lambda: self.get_track_icon())