#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QPushButton, QSystemTrayIcon
from PySide6.QtCore import Qt
from data.lib.QtUtils import QBaseApplication, QGridWidget, QNamedToggleButton, QNamedTextBrowser, QSlidingStackedWidget, QUtilsColor, QSaveData, QLangData
from data.lib.widgets.NotificationManager import NotificationManager
from ....SubProjectWidgetBase import SubProjectWidgetBase
from ....LogType import LogType
from ..NSMBW import NSMBW
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

        notifs = data.get('notifications', {})

        self._compile_done_notif = notifs.get('compileDone', True)
        self._compile_error_notif = notifs.get('compileError', True)

        self._compile_thread = None

        frame = QGridWidget()
        frame.grid_layout.setContentsMargins(0, 0, 0, 0)
        frame.grid_layout.setSpacing(8)
        self._root.scroll_layout.addWidget(frame, 0, 0, Qt.AlignmentFlag.AlignTop)

        self._compile_button = QPushButton(self._lang.get('QPushButton.compile'))
        self._compile_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self._compile_button.setIcon(self._compile_icon)
        self._compile_button.clicked.connect(self._compile)
        self._compile_button.setProperty('color', 'main')
        self._compile_button.setProperty('icon-padding', True)
        frame.grid_layout.addWidget(self._compile_button, 0, 0, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

        self._complete_view_toggle = QNamedToggleButton(None, self._lang.get('QNamedToggleButton.showCompleteLogs'))
        self._complete_view_toggle.toggle_button.toggled.connect(self._switch_logs_view)
        frame.grid_layout.addWidget(self._complete_view_toggle, 0, 1, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop)

        self._logs_slide_widget = QSlidingStackedWidget()
        self._root.scroll_layout.addWidget(self._logs_slide_widget, 1, 0)

        self._simple_logs_textbrowser = QNamedTextBrowser(None, '', self._lang.get('QNamedTextBrowser.simpleLogs'))
        self._simple_logs_textbrowser.setReadOnly(True)
        self._simple_logs_textbrowser.text_browser.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse |
            Qt.TextInteractionFlag.LinksAccessibleByMouse
        )
        self._simple_logs_textbrowser.text_browser.setOpenExternalLinks(True)
        self._logs_slide_widget.addWidget(self._simple_logs_textbrowser)

        self._complete_logs_textbrowser = QNamedTextBrowser(None, '', self._lang.get('QNamedTextBrowser.completeLogs'))
        self._complete_logs_textbrowser.setReadOnly(True)
        self._complete_logs_textbrowser.text_browser.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse |
            Qt.TextInteractionFlag.LinksAccessibleByMouse
        )
        self._complete_logs_textbrowser.text_browser.setOpenExternalLinks(True)
        self._logs_slide_widget.addWidget(self._complete_logs_textbrowser)

    def _compile(self) -> None:
        if self._compile_thread is None:
            self._compile_button.setIcon(self._stop_icon)
            self._compile_button.setText(self._lang.get('QPushButton.stop'))

            self._simple_logs_textbrowser.clear()
            self._complete_logs_textbrowser.clear()

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

    def _format_msg(self, msg: str, log_type: LogType, invisible: bool = False) -> str:
        l = self._lang.get(f'QNamedTextBrowser.{log_type.name.lower()}')
        if invisible:
            l = '<span>' + '&nbsp;' * (len(l) + 2) * 2 + '</span>'

        def gen_span(msg: str, color: QUtilsColor, bold: bool = False) -> str:
            bold_text = 'font-weight: 700;' if bold else 'font-weight: 400;'
            return f'<span style="color: {color.hex}; {bold_text};">{msg}</span>'

        if invisible: return f'{l} {gen_span(msg, self._neutral_color)}'
        return f'{gen_span("[", self._bracket_color, True)}{gen_span(l, log_type.value, True)}{gen_span("]", self._bracket_color, True)} {gen_span(msg, self._neutral_color)}'

    def _log_simple(self, msg: str, log_type: LogType, invisible: bool = False) -> None:
        self._simple_logs_textbrowser.append(self._format_msg(msg, log_type, invisible))

    def _log_complete(self, msg: str, log_type: LogType, invisible: bool = False) -> None:
        self._complete_logs_textbrowser.append(self._format_msg(msg, log_type, invisible))

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
