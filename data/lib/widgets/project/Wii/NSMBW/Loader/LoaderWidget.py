#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QPushButton, QSystemTrayIcon
from PySide6.QtCore import Qt
from data.lib.QtUtils import QBaseApplication, QGridWidget, QNamedToggleButton, QTerminalWidget, QSlidingStackedWidget, QUtilsColor, QSaveData, QLangData, QLogsColor
from data.lib.widgets.NotificationManager import NotificationManager
from ....SubProjectWidgetBase import SubProjectWidgetBase
from ..NSMBW import NSMBW
from .LogsColor import LogsColor
from .CompilerWorker import CompilerWorker
#----------------------------------------------------------------------

    # Class
class LoaderWidget(SubProjectWidgetBase):
    type: str = NSMBW.Loader

    _compile_icon = None
    _stop_icon = None

    _lang: QLangData = QLangData.NoTranslation()

    _neutral_color = QUtilsColor.from_hex('#aaaaaa')
    _bracket_color = QUtilsColor.from_hex('#dddddd')

    def init(app: QBaseApplication) -> None:
        LoaderWidget._lang = app.get_lang_data('QMainWindow.QSlidingStackedWidget.mainMenu.projects.projectWidget.Wii.NSMBW.LoaderWidget')
        LoaderWidget._compile_icon = app.get_icon('pushbutton/play.png', True, QSaveData.IconMode.Local)
        LoaderWidget._stop_icon = app.get_icon('pushbutton/stop.png', True, QSaveData.IconMode.Local)

        CompilerWorker.init(app)

    def __init__(self, app: QBaseApplication, name: str, icon: str, data: dict) -> None:
        super().__init__(app, data)

        self._name = name
        self._icon = icon
        self._data = data

        self._output_file = self._data.get('outputFile', None)

        notifs = NotificationManager.get(f'{LoaderWidget.type}')

        self._compile_done_notif = notifs.get('compileDone', True)
        self._compile_error_notif = notifs.get('compileError', True)

        self._compile_thread = None

        frame = QGridWidget()
        frame.layout_.setContentsMargins(0, 0, 0, 0)
        frame.layout_.setSpacing(8)
        self._root.layout_.addWidget(frame, 0, 0, Qt.AlignmentFlag.AlignTop)

        self._compile_button = QPushButton(self._lang.get('QPushButton.compile'))
        self._compile_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self._compile_button.setIcon(self._compile_icon)
        self._compile_button.clicked.connect(self._compile)
        self._compile_button.setProperty('color', 'main')
        self._compile_button.setProperty('icon-padding', True)
        frame.layout_.addWidget(self._compile_button, 0, 0, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

        self._complete_view_toggle = QNamedToggleButton(None, self._lang.get('QNamedToggleButton.showCompleteLogs'))
        self._complete_view_toggle.toggle_button.toggled.connect(self._switch_logs_view)
        frame.layout_.addWidget(self._complete_view_toggle, 0, 1, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop)

        self._logs_slide_widget = QSlidingStackedWidget()
        self._root.layout_.addWidget(self._logs_slide_widget, 1, 0)

        self._simple_logs_terminal = QTerminalWidget(None, self._lang.get('QTerminalWidget.simpleLogs'), QLogsColor, LogsColor)
        self._logs_slide_widget.addWidget(self._simple_logs_terminal)

        self._complete_logs_terminal = QTerminalWidget(None, self._lang.get('QTerminalWidget.completeLogs'), QLogsColor, LogsColor)
        self._logs_slide_widget.addWidget(self._complete_logs_terminal)

    def _compile(self) -> None:
        if self._compile_thread is None:
            self._compile_button.setIcon(self._stop_icon)
            self._compile_button.setText(self._lang.get('QPushButton.stop'))

            self._simple_logs_terminal.clear()
            self._complete_logs_terminal.clear()

            self._compile_thread = CompilerWorker(self._data)
            self._compile_thread.done.connect(self._compile_done)
            self._compile_thread.error.connect(self._compile_error)
            self._compile_thread.log_simple.connect(self._log_simple)
            self._compile_thread.log_complete.connect(self._log_complete)
            self._compile_thread.start()

        else:
            self._compile_button.setIcon(self._compile_icon)
            self._compile_button.setText(self._lang.get('QPushButton.compile'))

            if self._compile_thread.isRunning(): self._compile_thread.terminate()
            self._compile_thread = None

    def _compile_done(self) -> None:
        self._compile_button.setIcon(self._compile_icon)
        self._compile_button.setText(self._lang.get('QPushButton.compile'))

        if self._compile_thread.isRunning(): self._compile_thread.terminate()
        self._compile_thread = None

        if self._compile_done_notif: self._app.sys_tray.showMessage(
            self._app.get_lang_data('QSystemTrayIcon.showMessage.game.Wii.NSMBW.LoaderWidget.compileDone.title').replace('%s', self._name),
            self._app.get_lang_data('QSystemTrayIcon.showMessage.game.Wii.NSMBW.LoaderWidget.compileDone.message'),
            QSystemTrayIcon.MessageIcon.Information,
            self._app.MESSAGE_DURATION
        )
        self._app.show_alert(
            self._app.get_lang_data('QSystemTrayIcon.showMessage.game.Wii.NSMBW.LoaderWidget.compileDone.message'),
            raise_duration = self._app.ALERT_RAISE_DURATION,
            pause_duration = self._app.ALERT_PAUSE_DURATION,
            fade_duration = self._app.ALERT_FADE_DURATION,
            color = 'main'
        )

    def _compile_error(self, error: str) -> None:
        self._compile_button.setIcon(self._compile_icon)
        self._compile_button.setText(self._lang.get('QPushButton.compile'))

        if self._compile_thread.isRunning(): self._compile_thread.terminate()
        self._compile_thread = None

        if self._compile_error_notif: self._app.sys_tray.showMessage(
            self._app.get_lang_data('QSystemTrayIcon.showMessage.game.Wii.NSMBW.LoaderWidget.compileError.title').replace('%s', self._name),
            self._app.get_lang_data('QSystemTrayIcon.showMessage.game.Wii.NSMBW.LoaderWidget.compileError.message'),
            QSystemTrayIcon.MessageIcon.Critical,
            self._app.MESSAGE_DURATION
        )
        self._app.show_alert(
            self._app.get_lang_data('QSystemTrayIcon.showMessage.game.Wii.NSMBW.LoaderWidget.compileError.message'),
            raise_duration = self._app.ALERT_RAISE_DURATION,
            pause_duration = self._app.ALERT_PAUSE_DURATION,
            fade_duration = self._app.ALERT_FADE_DURATION,
            color = 'main'
        )

    @property
    def task_is_running(self) -> bool:
        return self._compile_thread is not None

    def _switch_logs_view(self, value: bool) -> None:
        self._logs_slide_widget.slide_in_index(int(value))

    def _log_simple(self, msg: str, log_type: QLogsColor, invisible: bool = False, extra_logs: tuple[LogsColor] = tuple()) -> None:
        self._simple_logs_terminal.log(msg, *extra_logs, log_type, continuous = invisible)

    def _log_complete(self, msg: str, log_type: QLogsColor, invisible: bool = False, extra_logs: tuple[LogsColor] = tuple()) -> None:
        self._complete_logs_terminal.log(msg, *extra_logs, log_type, continuous = invisible)

    def terminate_task(self) -> None:
        if self._compile_thread is not None:
            self._compile_thread.terminate()
            self._compile_thread = None

    def export(self) -> dict:
        return super().export() | {
            'outputFile': self._output_file,
        }
#----------------------------------------------------------------------

    # Setup
NotificationManager.register(
    f'{LoaderWidget.type}',
    {
        'compileDone': True,
        'compileError': True,
    }
)
#----------------------------------------------------------------------
