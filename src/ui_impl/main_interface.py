from ui_template.main_interface import Ui_MainWindow
from PyQt6 import QtWidgets, QtGui, QtCore
from asyncslot import asyncSlot

from models import Playlist

from playback.playbackEngine import PlaybackEngine
from sources import Youtube

import asyncio

class MainInterface(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.show()
        self.playbackEngine = PlaybackEngine.get_instance(self.songIconView.winId(), self.update_song)

        self.playlistView.setModel(self.playbackEngine.playlist)
        self.songName.setText(self.playbackEngine.now_playing.title if self.playbackEngine.now_playing else "Nothing playing")

        self.searchModel = Playlist()
        self.searchListView.setModel(self.searchModel)

        self.searchBtn.clicked.connect(asyncSlot(self.search))
        self.addButton.clicked.connect(self.add_to_queue)
        self.playButton.clicked.connect(self.play)
        self.nextButton.clicked.connect(self.skip)

        self.addButton.setEnabled(False)
        self.playButton.setEnabled(False)

    def update_song(self):
        self.songName.setText(self.playbackEngine.now_playing.__str__() if self.playbackEngine.now_playing else "Nothing playing")
        asyncio.create_task(self.update_thumbnail())

    async def update_thumbnail(self):
        pic = QtGui.QPixmap()
        thumb = await self.playbackEngine.now_playing.async_get_track_icon()
        pic.loadFromData(thumb)
        pic = pic.scaled(160, 90, QtCore.Qt.AspectRatioMode.KeepAspectRatio)
        self.songIconView.setScene(QtWidgets.QGraphicsScene())
        self.songIconView.scene().addPixmap(pic)


    async def search(self):
        query = self.searchBox.text()
        self.searchModel.clear()
        results = await Youtube().async_search(query)
        for result in results:
            self.searchModel.append(result)
        self.addButton.setEnabled(True)
        self.playButton.setEnabled(True)

    def add_to_queue(self):
        track = self.searchModel[self.searchListView.currentIndex().row()]
        self.playbackEngine.add_to_queue(track)

    def play(self):
        self.playbackEngine.resume()
        self.playButton.label.setText("Pause")
        self.playButton.clicked.disconnect()
        self.playButton.clicked.connect(self.pause)

    def pause(self):
        self.playbackEngine.pause()
        self.playButton.label.setText("Play")
        self.playButton.clicked.disconnect()
        self.playButton.clicked.connect(self.play)

    def skip(self):
        self.playbackEngine.skip()

    def stop(self):
        self.playbackEngine.stop()
        self.playButton.label.setText("Play")
        self.playButton.clicked.disconnect()
        self.playButton.clicked.connect(self.play)

    def clear_queue(self):
        self.playbackEngine.playlist.clear()

    def closeEvent(self, event):
        self.playbackEngine.stop()
        event.accept()

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MainInterface()
    app.exec()