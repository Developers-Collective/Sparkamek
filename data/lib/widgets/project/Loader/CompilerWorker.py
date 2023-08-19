#----------------------------------------------------------------------

    # Libraries
from PySide6.QtCore import Signal, QThread
import os, subprocess, sys, shutil

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
        self._output_file = self._data.get('outputFile', None)

        path = os.path.abspath(data['path']).replace('\\', '/')

        self._project_path = os.path.basename(path)
        self._cwd = os.path.dirname(path)
        self._project_name = self._project_path.rstrip('.S').rstrip('.s')


    @property
    def _project_full_path(self) -> str:
        return f'{self._cwd}/{self._project_path}'


    def run(self) -> None:
        self.log_info_all('Starting compilation...', False)


        command = [f'{self._cwd}/powerpc-eabi-as.exe', '-mregnames', self._project_full_path, '-o', f'{self._cwd}/{self._project_name}.o']

        try:
            self.log_info_all('Assembling...', False)
            self.log_info(f'Executing command: {command}', False)
            p = subprocess.Popen(command, stdout = subprocess.PIPE)
            output = p.communicate()[0].decode('utf-8')
            error_val = p.poll()

        except Exception as e:
            self.log_error(f'Error while compiling: {e}')
            self.error.emit(str(e))
            return
        
        if error_val != 0:
            self.log_error(f'Error while compiling: {output}')
            self.error.emit(output)
            return


        command = [f'{self._cwd}/powerpc-eabi-ld.exe', '-Ttext', '0x800046F0', '--oformat', 'binary', f'{self._cwd}/{self._project_name}.o', '-o', f'{self._cwd}/{self._project_name}.bin'] # todo: add address to settings

        try:
            self.log_info_all('Linking...', False)
            self.log_info(f'Executing command: {command}', False)
            p = subprocess.Popen(command, stdout = subprocess.PIPE)
            output = p.communicate()[0].decode('utf-8')
            error_val = p.poll()

        except Exception as e:
            self.log_error(f'Error while linking: {e}')
            self.error.emit(str(e))
            return
        
        if error_val != 0:
            self.log_error(f'Error while linking: {output}')
            self.error.emit(output)
            return


        try:
            os.remove(f'{self._cwd}/{self._project_name}.o')

        except Exception as e:
            self.log_warning(f'Error while deleting .o file: {e}')

        if self._output_file:
            try:
                shutil.copyfile(f'{self._cwd}/{self._project_name}.bin', self._output_file)

            except Exception as e:
                self.log_warning(f'Error while copying output file: {e}')

        self.log_success('Compilation completed successfully!')
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
