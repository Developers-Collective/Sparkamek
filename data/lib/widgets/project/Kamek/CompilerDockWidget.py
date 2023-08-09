#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QFrame, QPushButton
from PySide6.QtGui import QTextBlockFormat, QTextCursor
from PySide6.QtCore import Qt
from data.lib.qtUtils import QScrollableGridWidget, QBaseApplication, QSavableDockWidget, QSaveData, QGridWidget, QNamedToggleButton, QNamedTextEdit, QUtilsColor
from .CompilerWorker import CompilerWorker
from ..LogType import LogType
#----------------------------------------------------------------------

    # Class
class CompilerDockWidget(QSavableDockWidget):
    _compile_icon = None
    _stop_icon = None

    _lang = {}

    _neutral_color = QUtilsColor.from_hex('#aaaaaa')
    _bracket_color = QUtilsColor.from_hex('#dddddd')

    def init(app: QBaseApplication) -> None:
        CompilerDockWidget._lang = app.get_lang_data('QMainWindow.QSlidingStackedWidget.mainMenu.projects.KamekWidget.CompilerDockWidget')
        CompilerDockWidget._compile_icon = app.get_icon('pushbutton/play.png', True, QSaveData.IconMode.Local)
        CompilerDockWidget._stop_icon = app.get_icon('pushbutton/stop.png', True, QSaveData.IconMode.Local)

        CompilerWorker.init(app)

    def __init__(self, app: QBaseApplication, name: str, icon: str, data: dict) -> None:
        super().__init__(self._lang.get_data('title').replace('%s', name))

        self._name = name
        self._icon = icon
        self._data = data

        self._root = QScrollableGridWidget()
        self._root.setProperty('wide', True)
        self._root.setMinimumWidth(200)
        self._root.setMinimumHeight(100)
        self._root.setFrameShape(QFrame.Shape.NoFrame)
        self._root.scroll_widget.setProperty('QDockWidget', True)
        self.setObjectName('compiler')
        self.setWidget(self._root)

        self._compile_thread = None

        frame = QGridWidget()
        frame.grid_layout.setContentsMargins(0, 0, 0, 0)
        frame.grid_layout.setSpacing(8)
        self._root.scroll_layout.addWidget(frame, 0, 0, Qt.AlignmentFlag.AlignTop)

        self._compile_button = QPushButton(self._lang.get_data('QPushButton.compile'))
        self._compile_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self._compile_button.setIcon(self._compile_icon)
        self._compile_button.clicked.connect(self._compile)
        self._compile_button.setProperty('color', 'main')
        self._compile_button.setProperty('icon-padding', True)
        frame.grid_layout.addWidget(self._compile_button, 0, 0, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

        self._complete_view_toggle = QNamedToggleButton(None, self._lang.get_data('QNamedToggleButton.showCompleteLogs'))
        self._complete_view_toggle.toggle_button.toggled.connect(self._switch_logs_view)
        frame.grid_layout.addWidget(self._complete_view_toggle, 0, 1, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop)

        self._simple_logs_textedit = QNamedTextEdit(None, '', self._lang.get_data('QNamedTextEdit.simpleLogs'))
        self._simple_logs_textedit.setReadOnly(True)
        self._root.scroll_layout.addWidget(self._simple_logs_textedit, 1, 0)

        self._complete_logs_textedit = QNamedTextEdit(None, '', self._lang.get_data('QNamedTextEdit.completeLogs'))
        self._complete_logs_textedit.setReadOnly(True)
        self._root.scroll_layout.addWidget(self._complete_logs_textedit, 2, 0)
        self._complete_logs_textedit.hide()

    def _compile(self) -> None:
        if self._compile_thread is None:
            self._compile_button.setIcon(self._stop_icon)
            self._compile_button.setText(self._lang.get_data('QPushButton.stop'))

            self._simple_logs_textedit.clear()
            self._complete_logs_textedit.clear()

            self._compile_thread = CompilerWorker(self._data)
            self._compile_thread.done.connect(self._compile_done)
            self._compile_thread.error.connect(self._compile_error)
            self._compile_thread.log_simple.connect(self._log_simple)
            self._compile_thread.log_complete.connect(self._log_complete)
            self._compile_thread.start()

        else:
            self._compile_button.setIcon(self._compile_icon)
            self._compile_button.setText(self._lang.get_data('QPushButton.compile'))

            if self._compile_thread.isRunning(): self._compile_thread.terminate()
            self._compile_thread = None

    def _compile_done(self) -> None:
        self._compile_button.setIcon(self._compile_icon)
        self._compile_button.setText(self._lang.get_data('QPushButton.compile'))

        if self._compile_thread.isRunning(): self._compile_thread.terminate()
        self._compile_thread = None

    def _compile_error(self, error: str) -> None:
        self._compile_button.setIcon(self._compile_icon)
        self._compile_button.setText(self._lang.get_data('QPushButton.compile'))

        if self._compile_thread.isRunning(): self._compile_thread.terminate()
        self._compile_thread = None

    @property
    def task_is_running(self) -> bool:
        return self._compile_thread is not None

    def _switch_logs_view(self, value: bool) -> None:
        if value:
            self._simple_logs_textedit.hide()
            self._complete_logs_textedit.show()
        else:
            self._complete_logs_textedit.hide()
            self._simple_logs_textedit.show()

    def _format_msg(self, msg: str, log_type: LogType, invisible: bool = False) -> str:
        l = self._lang.get_data(f'QNamedTextEdit.{log_type.name.lower()}')
        if invisible:
            l = '<span>' + '&nbsp;' * (len(l) + 2) * 2 + '</span>'

        def gen_span(msg: str, color: QUtilsColor, bold: bool = False) -> str:
            bold_text = 'font-weight: 700;' if bold else 'font-weight: 400;'
            return f'<span style="color: {color.hex}; {bold_text};">{msg}</span>'

        if invisible: return f'{l} {gen_span(msg, self._neutral_color)}'
        return f'{gen_span("[", self._bracket_color, True)}{gen_span(l, log_type.value, True)}{gen_span("]", self._bracket_color, True)} {gen_span(msg, self._neutral_color)}'

    def _log_simple(self, msg: str, log_type: LogType, invisible: bool = False) -> None:
        self._simple_logs_textedit.append(self._format_msg(msg, log_type, invisible))

    def _log_complete(self, msg: str, log_type: LogType, invisible: bool = False) -> None:
        self._complete_logs_textedit.append(self._format_msg(msg, log_type, invisible))
#----------------------------------------------------------------------
