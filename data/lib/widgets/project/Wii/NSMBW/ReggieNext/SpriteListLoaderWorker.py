#----------------------------------------------------------------------

    # Libraries
from PySide6.QtCore import Signal, QThread
import os, traceback

from data.lib.qtUtils import QBaseApplication
from data.lib.storage import XML
from .sprites import *
#----------------------------------------------------------------------

    # Class
class SpriteListLoaderWorker(QThread):
    done = Signal()
    error = Signal(str)

    found_item = Signal(Sprite)

    @staticmethod
    def init(app: QBaseApplication) -> None:
        pass

    def __init__(self, path: str) -> None:
        super(SpriteListLoaderWorker, self).__init__()

        self._path = path

    def run(self) -> None:
        try:
            if not os.path.isfile(self._path):
                self.error.emit(f'Path does not exist: {self._path}')
                return
            
            content = XML.parse_file(self._path)

            if content is None:
                self.error.emit(f'Failed to parse file: {self._path}')
                return

            sprites = Sprites(content)

            for sprite in sprites.children:
                self.found_item.emit(sprite)

        except Exception as e:
            traceback.print_exc()
            self.error.emit(str(e))
            return

        self.done.emit()
#----------------------------------------------------------------------
