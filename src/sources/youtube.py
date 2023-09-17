from .common import StreamInterface
from models import PlaybackTrack, Playlist

import yt_dlp
import asyncio

class Youtube(StreamInterface):
    def __init__(self):
        # limit to 10 results for now
        self.ydl = yt_dlp.YoutubeDL({
            "format": "bestaudio/best",
            "quiet": True,
            "no_warnings": True,
            "nocheckcertificate": True,
            "ignoreerrors": True,
            "default_search": "ytsearch5",
            "flat-playlist": True,
        })

    def search(self, query: str) -> Playlist:
        results = self.ydl.extract_info(query, download=False)
        playlist = Playlist()
        for result in results["entries"]:
            track = PlaybackTrack(
                id=result["id"],
                name=result["title"],
                url=result["webpage_url"],
                artist=result["artist"] if "artist" in result else "",
                album=result["album"] if "album" in result else "",
                duration=result["duration"],
                icon_url=result["thumbnail"] if "thumbnail" in result else ""
            )
            playlist.append(track)
        return playlist
    
    async def async_search(self, query: str) -> Playlist:
        return await asyncio.get_event_loop().run_in_executor(None, lambda: self.search(query))