from .playbackTrack import PlaybackTrack
from PyQt6.QtCore import QAbstractListModel, QModelIndex, Qt


class Playlist(QAbstractListModel):
    def __init__(self):
        super().__init__()
        self.tracks = []

    def __getitem__(self, index):
        return self.tracks[index]

    def __len__(self):
        return len(self.tracks)

    def append(self, track: PlaybackTrack):
        self.beginInsertRows(QModelIndex(), len(self.tracks), len(self.tracks))
        self.tracks.append(track)
        self.endInsertRows()

    def remove(self, track: PlaybackTrack):
        index = self.tracks.index(track)
        self.beginRemoveRows(QModelIndex(), index, index)
        self.tracks.remove(track)
        self.endRemoveRows()

    def clear(self):
        self.beginResetModel()
        self.tracks = []
        self.endResetModel()

    def data(self, index: QModelIndex, role: int) -> any:
        if role == Qt.ItemDataRole.DisplayRole:
            return str(self.tracks[index.row()])

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        return len(self.tracks)

    def flags(self, index: QModelIndex) -> Qt.ItemFlag:
        return Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled
