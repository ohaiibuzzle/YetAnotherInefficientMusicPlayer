from .common import StreamInterface
from models import PlaybackTrack, Playlist

import youtube_search
import asyncio


class Youtube(StreamInterface):
    def __init__(self):
        pass

    def search(self, query: str) -> Playlist:
        results = youtube_search.YoutubeSearch(query, max_results=25).to_dict()
        playlist = Playlist()
        for result in results:
            track = PlaybackTrack(
                id=result["id"],
                name=result["title"],
                artist=result["channel"],
                duration=result["duration"],
                url=f"https://youtube.com{result['url_suffix']}",
                icon_url=result["thumbnails"][0],
            )
            playlist.append(track)
        return playlist

    async def async_search(self, query: str) -> Playlist:
        return await asyncio.get_event_loop().run_in_executor(
            None, lambda: self.search(query)
        )
