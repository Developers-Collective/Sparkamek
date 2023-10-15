#----------------------------------------------------------------------

    # Libraries
from PySide6.QtCore import Signal, QThread
import os, subprocess, shutil

from data.lib.qtUtils import QBaseApplication, QUtilsColor
from ..LogType import LogType
#----------------------------------------------------------------------

#   Setup
startupinfo = subprocess.STARTUPINFO()
startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
startupinfo.wShowWindow = subprocess.SW_HIDE
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
            p = subprocess.Popen(command, stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell = True, startupinfo = startupinfo)
            output = p.communicate()[1].decode('utf-8')
            error_val = p.poll()

        except Exception as e:
            self.log_error(f'Error while compiling: {e}')
            self.error.emit(str(e))
            return

        if error_val != 0:
            output_lines = output.replace('\r', '').split('\n')
            self.log_error(f'Error while compiling:')

            for line in output_lines:
                if not line:
                    self.log_error('&nbsp;', True)
                    continue

                if line.endswith('Assembler messages:'): continue

                try:
                    new_line = line.replace('`', '\'').replace(f'{self._project_full_path}:', '').strip()
                    args = new_line.split(':')
                    args.pop(1)
                    args = [arg.strip() for arg in args]
                    line_nb = int(args.pop(0))
                    new_line = ': '.join(args)

                    func_name = new_line.split('\'')[1]
                    new_line = new_line.replace(f'\'{func_name}\'', f'<span style="font-style: italic; background-color: #55{LogType.Error.value.hex[1:]}">{func_name}</span>')

                    self.log_error(f'<span style="font-style: italic">Line {line_nb}</span>', True)
                    self.log_error(f'&nbsp;&nbsp;&nbsp;&nbsp;{new_line}', True)

                except Exception as e:
                    self.log_error(line, True)

            self.error.emit(output)
            return


        command = [f'{self._cwd}/powerpc-eabi-ld.exe', '-Ttext', '0x800046F0', '--oformat', 'binary', f'{self._cwd}/{self._project_name}.o', '-o', f'{self._cwd}/{self._project_name}.bin'] # todo: add address to settings

        try:
            self.log_info_all('Linking...', False)
            self.log_info(f'Executing command: {command}', False)
            p = subprocess.Popen(command, stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell = True, startupinfo = startupinfo)
            output = p.communicate()[1].decode('utf-8')
            error_val = p.poll()

        except Exception as e:
            self.log_error(f'Error while linking: {e}')
            self.error.emit(str(e))
            return

        if error_val != 0:
            output_lines = output.replace('\r', '').split('\n')
            self.log_error(f'Error while linking:')

            for line in output_lines:
                if not line:
                    self.log_error('&nbsp;', True)
                    continue

                if line.startswith(command[0]):
                    try:
                        new_line = line.split(':')[-2].replace('`', '\'').strip()
                        new_line = new_line[0].upper() + new_line[1:]

                        func_name = new_line.split('\'')[1]
                        new_line = new_line.replace(f'\'{func_name}\'', f'<span style="font-style: italic; background-color: #55{LogType.Error.value.hex[1:]}">{func_name}</span>')

                        self.log_error(f'{new_line}:', True)

                    except Exception as e:
                        self.log_error(line, True)

                    continue

                new_line = line.replace('`', '\'').strip()

                func_name = new_line.split('\'')[1]
                new_line = new_line.replace(func_name, f'<span style="font-style: italic; background-color: #55{LogType.Error.value.hex[1:]}">{func_name}</span>')

                self.log_error(f'&nbsp;&nbsp;&nbsp;&nbsp;{new_line}', True)

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
