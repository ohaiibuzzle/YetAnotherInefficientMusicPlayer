import sys

from PyQt6 import QtWidgets
from ui_impl.main_interface import MainInterface
from asyncslot import AsyncSlotRunner


if __name__ == "__main__":
    with AsyncSlotRunner():
        app = QtWidgets.QApplication(sys.argv)
        main_interface = MainInterface()
        sys.exit(app.exec())