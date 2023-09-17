from models import PlaybackTrack, Playlist

class StreamInterface:
    """
    Base class for a streaming interface

    Includes the following methods (for now):
        - search: take in a search query and return a list of playbackTracks
    """

    def __init__(self):
        raise NotImplementedError

    def search(self, query: str) -> Playlist:
        raise NotImplementedError

    async def async_search(self, query: str) -> Playlist:
        raise NotImplementedError