#----------------------------------------------------------------------

    # Libraries
from PySide6.QtCore import Signal, QThread
import os, yaml, sys, traceback
from pathlib import Path

from data.lib.qtUtils import QBaseApplication
from ..LogType import LogType
from ..ProjectException import ProjectException
from .compiler import *
#----------------------------------------------------------------------

    # Class
class CompilerWorker(QThread):
    _devkitppc_path: str = None

    done = Signal()
    error = Signal(str)
    log_simple = Signal(str, LogType, bool)
    log_complete = Signal(str, LogType, bool)

    @staticmethod
    def init(app: QBaseApplication) -> None:
        CompilerWorker._devkitppc_path = 'D:/Programmes/devkitPro/devkitPPC/bin/' # todo: get from settings

    def __init__(self, data: dict) -> None:
        super(CompilerWorker, self).__init__()

        path = os.path.abspath(data['path']).replace('\\', '/')

        self._project_path = os.path.basename(path)
        self._cwd = os.path.dirname(path)
        self._project_name = self._project_path.rstrip('.yaml')

        self._base_version = 'pal'
        self._version_ids = (
            ({'pal2': 'P2'} if data.get('generatePAL', None) else {}) |
            ({'ntsc': 'E1'} if data.get('generateNTSC', None) else {}) |
            ({'ntsc2': 'E2'} if data.get('generateNTSC', None) else {}) |
            ({'jpn': 'J1'} if data.get('generateJP', None) else {}) |
            ({'jpn2': 'J2'} if data.get('generateJP', None) else {}) |
            ({'kor': 'K'} if data.get('generateKR', None) else {}) |
            ({'twn': 'W'} if data.get('generateTW', None) else {}) |
            ({'chn': 'C'} if data.get('generateCH', None) else {})
        )

        self._address_mapper_controller = AddressMapperController(self._cwd, self._project_path, self._base_version, self._version_ids)
        self._address_mapper_controller.log_simple.connect(self.log_simple)
        self._address_mapper_controller.log_complete.connect(self.log_complete)

        self._kamek_controller = KamekController(self._cwd, self._project_path, self._base_version, self._version_ids)
        self._kamek_controller.log_simple.connect(self.log_simple)
        self._kamek_controller.log_complete.connect(self.log_complete)


    @property
    def _project_full_path(self) -> str:
        return f'{self._cwd}/{self._project_path}'


    def run(self) -> None:
        ret = ('Starting compilation...', LogType.Info, False)
        self.log_simple.emit(*ret)
        self.log_complete.emit(*ret)

        with open(self._project_full_path, 'r', encoding = 'utf-8') as f:
            project_data = yaml.safe_load(f)

        if not isinstance(project_data, dict):
            ret = ('The project file is an invalid format (it should be a YAML mapping)', LogType.Error, False)

            self.log_simple.emit(*ret)
            self.log_complete.emit(*ret)
            return self.error.emit(ret[0])

        if 'output_dir' not in project_data:
            ret = ('Missing output_dir field in the project file', LogType.Error, False)

            self.log_simple.emit(*ret)
            self.log_complete.emit(*ret)
            return self.error.emit(ret[0])

        asm_folder = Path(project_data['output_dir'])


        gccpath = Path(self._devkitppc_path)

        if sys.platform == 'win32':
            # Running on Windows
            kamekopts = {'gcc_append_exe': True}

        else:
            proc_version = Path('/proc/version')
            if proc_version.is_file() and 'microsoft' in proc_version.read_text().lower():  # https://stackoverflow.com/a/38859331/4718769
                # Running on WSL
                kamekopts = {'gcc_append_exe': True}

            else:
                # Running on Mac/Linux
                kamekopts = {'use_wine': True}

        self.log_complete.emit(f'Mapping addresses for {self._project_name}...', LogType.Info, False)

        try: self._address_mapper_controller.run()
        except ProjectException as e:
            self.log_simple.emit(e.msg, e.type, False)
            self.log_complete.emit(e.msg, e.type, False)
            return self.error.emit(e.msg)


        self._kamek_controller.set_config( # todo: get from settings (maybe?)
            KamekConfig(
                show_cmd = True,
                use_rels = False,
                use_mw = True,
                gcc_path = self._devkitppc_path,
                gcc_type = 'powerpc-eabi',
                mw_path = 'tools/cw/',
                filt_path = 'tools/c++filt/',
                fast_hack = True,
                **kamekopts
            )
        )
        try: self._kamek_controller.run()

        except Exception as e:
            print(traceback.format_exc())
            self.log_simple.emit(str(e), LogType.Error, False)
            self.log_complete.emit(str(e), LogType.Error, False)
            return self.error.emit(str(e))


        ret = ('All done!', LogType.Success, False)
        self.log_simple.emit(*ret)
        self.log_complete.emit(*ret)
        self.done.emit()
#----------------------------------------------------------------------
