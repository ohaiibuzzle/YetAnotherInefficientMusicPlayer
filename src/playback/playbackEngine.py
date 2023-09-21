import mpv
from models import PlaybackTrack, Playlist
from threading import Thread
import time
import asyncio


class PlaybackEngine:
    instance = None
    playlist = Playlist()
    now_playing: PlaybackTrack = None
    _now_playing_time = 0
    next_track_callback = None
    next_track = asyncio.Event()

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
            wid=str(int(wid)) if wid else None,
        )

    @staticmethod
    def get_instance(wid=None, next_track_callback=None):
        if not PlaybackEngine.instance:
            PlaybackEngine.instance = PlaybackEngine(
                wid, next_track_callback
            )
        return PlaybackEngine.instance

    async def begin_playback(self):
        next_track = asyncio.Event()
        started_playing = asyncio.Event()
        def wait_until_playing():
            self.mpv.wait_until_playing()
            Thread(target=self.update_playback).start()
            started_playing.set()

        def wait_for_next_track():
            self.mpv.wait_for_playback()
            next_track.set()

        while self.playlist.__len__() > 0:
            self.now_playing = self.playlist[0]
            self.playlist.remove(self.now_playing)
            next_track.clear()
            
            if self.next_track_callback:
                self.next_track_callback()
            self.mpv.play(self.now_playing.url)
            Thread(target=wait_until_playing).start()
            await started_playing.wait()
            
            Thread(target=wait_for_next_track).start()
            await next_track.wait()
        else:
            self.now_playing = None

    def update_playback(self):
        current_song = self.now_playing
        self._now_playing_time = 0
        time_secs = self._human_time_to_seconds(self.now_playing.duration)
        while self.now_playing == current_song and self._now_playing_time < time_secs:
            self._now_playing_time += 1
            time.sleep(1)

    async def add_to_queue(self, track: PlaybackTrack):
        self.playlist.append(track)
        if len(self.playlist) == 1 and not self.now_playing:
            asyncio.create_task(self.begin_playback())

    def skip(self):
        # stop current track (it will move on automatically)
        self.mpv.stop()

    def pause(self):
        self.mpv.pause = True

    def resume(self):
        self.mpv.pause = False

    def stop(self):
        self.mpv.stop()
        self.playlist.clear()

    def seek(self, seconds: int):
        self.mpv.seek(seconds, reference="absolute", precision="exact")
        self._now_playing_time = seconds

    @property
    def playback_time(self):
        return self._now_playing_time if self.now_playing else 0
    
    @playback_time.setter
    def playback_time(self, seconds: int):
        self.seek(seconds)

    @property
    def playback_duration(self):
        return self._human_time_to_seconds(self.now_playing.duration) if self.now_playing else 0
    
    @property
    def human_readable_playback_time(self):
        return self._seconds_to_human_time(self.playback_time)
    
    @property
    def human_readable_playback_duration(self):
        return self._seconds_to_human_time(self.playback_duration)

    def _human_time_to_seconds(self, human_time: str) -> int:
        """
        Convert time from HH:MM:SS or MM:SS to seconds
        """
        if len(human_time.split(":")) == 3:
            hours, minutes, seconds = human_time.split(":")
            return int(hours) * 3600 + int(minutes) * 60 + int(seconds)
        elif len(human_time.split(":")) == 2:
            minutes, seconds = human_time.split(":")
            return int(minutes) * 60 + int(seconds)
        else:
            return int(human_time)
        
    def _seconds_to_human_time(self, seconds: int) -> str:
        """
        Convert time from seconds to HH:MM:SS
        """
        minutes, seconds = divmod(seconds, 60)
        # Pad as necessary
        minutes = str(minutes).zfill(2)
        seconds = str(seconds).zfill(2)

        return f"{minutes}:{seconds}"