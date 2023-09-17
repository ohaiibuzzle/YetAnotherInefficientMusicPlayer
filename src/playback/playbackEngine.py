import mpv
from models import PlaybackTrack, Playlist

class PlaybackEngine:
    instance = None
    playlist = Playlist()
    now_playing: PlaybackTrack = None
    next_track_callback = None

    def __init__(self, wid, next_track_callback):
        self.next_track_callback = next_track_callback
        self.mpv = mpv.MPV(
            ytdl=True, 
            input_default_bindings=True, 
            input_vo_keyboard=True, 
            osc=True, 
            idle=True, 
            log_handler=print,
            video=False,
            wid=str(int(wid)) if wid else None
        )

    @staticmethod 
    def get_instance(wid = None, next_track_callback = None):
        if not PlaybackEngine.instance:
            PlaybackEngine.instance = PlaybackEngine(wid, next_track_callback)
        return PlaybackEngine.instance
    
    def begin_playback(self):
        while self.playlist:
            self.now_playing = self.playlist[0]
            self.mpv.play(self.now_playing.url)
            if self.next_track_callback:
                self.next_track_callback()
            self.playlist.remove(self.now_playing)

    def add_to_queue(self, track: PlaybackTrack):
        self.playlist.append(track)
        if len(self.playlist) == 1 and not self.now_playing:
            self.begin_playback()

    def skip(self):
        # stop current track
        self.mpv.stop()
        # play next track
        self.begin_playback()

    def pause(self):
        self.mpv.pause = True

    def resume(self):
        self.mpv.pause = False

    def stop(self):
        self.mpv.stop()
        self.playlist.clear()