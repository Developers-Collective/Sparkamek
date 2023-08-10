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

        self._data = data

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
        self.log_info_all('Starting compilation...', False)

        with open(self._project_full_path, 'r', encoding = 'utf-8') as f:
            project_data = yaml.safe_load(f)

        if not isinstance(project_data, dict):
            msg = 'The project file is an invalid format (it should be a YAML mapping)'
            self.log_error(msg, False)
            return self.error.emit(msg)

        if 'output_dir' not in project_data:
            msg = 'Missing output_dir field in the project file'
            self.log_error(msg, False)
            return self.error.emit(msg)

        self._asm_folder = Path(project_data['output_dir'])


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

        self.log_info(f'Mapping addresses for {self._project_name}...', False)

        try: self._address_mapper_controller.run()
        except ProjectException as e:
            self.log_error(e.msg, False)
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
            self.log_error(str(e), False)
            return self.error.emit(str(e))

        self._build_folder = Path(f'{self._cwd}/Build_{self._project_name}')

        self.log_info('&nbsp;', True)

        if self._data.get('generatePAL', None):
            self.log_info('Renaming PAL files...', False)
            self._copy_files('pal', 'EU_1')
            self._copy_files('pal2', 'EU_2')

        if self._data.get('generateNTSC', None):
            self.log_info('Renaming NTSC files...', False)
            self._copy_files('ntsc', 'US_1')
            self._copy_files('ntsc2', 'US_2')

        if self._data.get('generateJP', None):
            self.log_info('Renaming JP files...', False)
            self._copy_files('jpn', 'JP_1')
            self._copy_files('jpn2', 'JP_2')

        if self._data.get('generateKR', None):
            self.log_info('Renaming KR files...', False)
            self._copy_files('kor', 'KR_3')

        if self._data.get('generateTW', None):
            self.log_info('Renaming TW files...', False)
            self._copy_files('twn', 'TW_4')

        if self._data.get('generateCH', None):
            self.log_info('Renaming CH files...', False)
            self._copy_files('chn', 'CN_5')

        self.log_info_all('&nbsp;', True)
        self.log_success('All done!', False)
        self.done.emit()

    def _copy_files(self, version_name_1: str, version_name_2: str) -> None:
        (Path(self._cwd) / self._asm_folder / f'n_{version_name_1}_loader.bin').replace(self._build_folder / f'System{version_name_2}.bin')
        (Path(self._cwd) / self._asm_folder / f'n_{version_name_1}_dlcode.bin').replace(self._build_folder / f'DLCode{version_name_2}.bin')
        (Path(self._cwd) / self._asm_folder / f'n_{version_name_1}_dlrelocs.bin').replace(self._build_folder / f'DLRelocs{version_name_2}.bin')

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
