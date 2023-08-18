#----------------------------------------------------------------------

    # Libraries
from PySide6.QtCore import Signal, QThread
import os

from data.lib.qtUtils import QBaseApplication, QUtilsColor
from ..LogType import LogType
from ..ProjectException import ProjectException
#----------------------------------------------------------------------

    # Class
class CompilerWorker(QThread):
    _color_link = QUtilsColor('#0000FF')

    done = Signal()
    error = Signal(str)
    log_simple = Signal(str, LogType, bool)
    log_complete = Signal(str, LogType, bool)

    @staticmethod
    def init(app: QBaseApplication) -> None:
        CompilerWorker._color_link = app.COLOR_LINK

    def __init__(self, data: dict) -> None:
        super(CompilerWorker, self).__init__()

        self._data = data

        path = os.path.abspath(data['path']).replace('\\', '/')

        self._project_path = os.path.basename(path)
        self._cwd = os.path.dirname(path)
        self._project_name = self._project_path.rstrip('.S').rstrip('.s')


    @property
    def _project_full_path(self) -> str:
        return f'{self._cwd}/{self._project_path}'


    def run(self) -> None:
        self.log_info_all('Starting compilation...', False)

        # todo: compile

        self.done.emit()

    def log_info(self, msg: str, invisible: bool = False) -> None:
        msg = msg.strip()
        if not msg: return
        self.log_complete.emit(msg, LogType.Info, invisible)

    def log_info_all(self, msg: str, invisible: bool = False) -> None:
        msg = msg.strip()
        if not msg: return
        self.log_complete.emit(msg, LogType.Info, invisible)
        self.log_simple.emit(msg, LogType.Info, invisible)

    def log_warning(self, msg: str, invisible: bool = False) -> None:
        msg = msg.strip()
        if not msg: return
        self.log_complete.emit(msg, LogType.Warning, invisible)
        self.log_simple.emit(msg, LogType.Warning, invisible)

    def log_error(self, msg: str, invisible: bool = False) -> None:
        msg = msg.strip()
        if not msg: return
        self.log_complete.emit(msg, LogType.Error, invisible)
        self.log_simple.emit(msg, LogType.Error, invisible)

    def log_success(self, msg: str, invisible: bool = False) -> None:
        msg = msg.strip()
        if not msg: return
        self.log_complete.emit(msg, LogType.Success, invisible)
        self.log_simple.emit(msg, LogType.Success, invisible)
#----------------------------------------------------------------------
