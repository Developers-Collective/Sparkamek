#----------------------------------------------------------------------

    # Libraries
from PySide6.QtCore import Signal, QThread
import time

from .LogType import LogType
#----------------------------------------------------------------------

    # Class
class CompilerWorker(QThread):
    done = Signal()
    error = Signal(str)
    log_simple = Signal(str, LogType)
    log_complete = Signal(str, LogType)

    def __init__(self) -> None:
        super(CompilerWorker, self).__init__()

    def run(self) -> None:
        time.sleep(1)
        self.log_simple.emit('test', LogType.Error)
        self.log_simple.emit('test', LogType.Warning)
        self.log_simple.emit('test', LogType.Success)
        self.log_complete.emit('test', LogType.Error)
        self.log_complete.emit('test', LogType.Warning)
        self.log_complete.emit('test', LogType.Success)
        self.log_complete.emit('test', LogType.Info)
        for i in range(100):
            self.log_simple.emit(f'test {i}', LogType.Info)
            self.log_complete.emit(f'test {i}', LogType.Info)
            time.sleep(0.1)
        self.done.emit()
#----------------------------------------------------------------------
