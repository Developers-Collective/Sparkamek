#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QPushButton, QDockWidget, QSystemTrayIcon
from PySide6.QtCore import Qt
from data.lib.qtUtils import QBaseApplication, QSaveData, QGridWidget, QNamedToggleButton, QNamedTextBrowser, QSlidingStackedWidget, QUtilsColor, QLangData
from ..SubProjectWidgetBase import SubProjectWidgetBase
from data.lib.widgets.ProjectKeys import ProjectKeys
from .SpritesAndActorsDockWidget import SpritesAndActorsDockWidget
from .SymbolsDockWidget import SymbolsDockWidget
from .AddressConverterDockWidget import AddressConverterDockWidget
from .CompilerWorker import CompilerWorker
from .CopyType import CopyType
from ..LogType import LogType
#----------------------------------------------------------------------

    # Class
class KamekWidget(SubProjectWidgetBase):
    type: ProjectKeys = ProjectKeys.Kamek

    _compile_icon = None
    _stop_icon = None

    _neutral_color = QUtilsColor.from_hex('#aaaaaa')
    _bracket_color = QUtilsColor.from_hex('#dddddd')

    _lang: QLangData = QLangData.NoTranslation()

    def init(app: QBaseApplication) -> None:
        KamekWidget._lang = app.get_lang_data('QMainWindow.QSlidingStackedWidget.mainMenu.projects.KamekWidget')
        KamekWidget._compile_icon = app.get_icon('pushbutton/play.png', True, QSaveData.IconMode.Local)
        KamekWidget._stop_icon = app.get_icon('pushbutton/stop.png', True, QSaveData.IconMode.Local)

        SpritesAndActorsDockWidget.init(app)
        CompilerWorker.init(app)
        SymbolsDockWidget.init(app)
        AddressConverterDockWidget.init(app)

    def __init__(self, app: QBaseApplication, name: str, icon: str, data: dict) -> None:
        super().__init__(app, data)
        self._app = app
        self._name = name
        self._icon = icon
        self._data = data

        dockwidgets = data.get('dockwidgets', {})
        self._build_folder = data.get('buildFolder', None)
        self._copy_type = CopyType(data.get('copyType', 1))
        self._output_folder = data.get('outputFolder', None)
        self._generate_pal_v1 = data.get('generatePALv1', True) or data.get('generatePAL', True)
        self._generate_pal_v2 = data.get('generatePALv2', False) or data.get('generatePAL', False)
        self._generate_ntsc_v1 = data.get('generateNTSCv1', False) or data.get('generateNTSC', False)
        self._generate_ntsc_v2 = data.get('generateNTSCv2', False) or data.get('generateNTSC', False)
        self._generate_jp_v1 = data.get('generateJPv1', False) or data.get('generateJP', False)
        self._generate_jp_v2 = data.get('generateJPv2', False) or data.get('generateJP', False)
        self._generate_kr = data.get('generateKR', False)
        self._generate_tw = data.get('generateTW', False)
        self._generate_cn = data.get('generateCN', False)
        self._nintendo_driver_mode = data.get('nintendoDriverMode', False)

        self._sprites_and_actors_dock_widget = SpritesAndActorsDockWidget(app, name, icon, data)
        self._symbols_dock_widget = SymbolsDockWidget(app, name, icon, data)
        self._address_converter_dock_widget = AddressConverterDockWidget(app, name, icon, data)

        if 'spritesAndActors' in dockwidgets: self._sprites_and_actors_dock_widget.load_dict(self, dockwidgets['spritesAndActors'])
        else: self.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, self._sprites_and_actors_dock_widget)

        if 'symbols' in dockwidgets: self._symbols_dock_widget.load_dict(self, dockwidgets['symbols'])
        else: self.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, self._symbols_dock_widget)

        if 'addressConverter' in dockwidgets: self._address_converter_dock_widget.load_dict(self, dockwidgets['addressConverter'])
        else: self.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, self._address_converter_dock_widget)

        if 'spritesAndActors' not in dockwidgets and 'symbols' not in dockwidgets and 'addressConverter' not in dockwidgets:
            self.tabifyDockWidget(self._sprites_and_actors_dock_widget, self._symbols_dock_widget)
            self.tabifyDockWidget(self._symbols_dock_widget, self._address_converter_dock_widget)
            self._sprites_and_actors_dock_widget.raise_()


        self._devkitppc_path: str = app.save_data.devkitppc_path

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


    @property
    def task_is_running(self) -> bool:
        return (
            self._sprites_and_actors_dock_widget.task_is_running or
            self._symbols_dock_widget.task_is_running or
            self._address_converter_dock_widget.task_is_running or
            self._compile_thread is not None
        )


    def _compile(self) -> None:
        if self._compile_thread is None:
            self._compile_button.setIcon(self._stop_icon)
            self._compile_button.setText(self._lang.get('QPushButton.stop'))

            self._simple_logs_textbrowser.clear()
            self._complete_logs_textbrowser.clear()

            self._compile_thread = CompilerWorker(self._data, self._devkitppc_path, self._copy_type)
            self._compile_thread.done.connect(self._compile_done)
            self._compile_thread.error.connect(self._compile_error)
            self._compile_thread.log_simple.connect(self._log_simple)
            self._compile_thread.log_complete.connect(self._log_complete)
            self._compile_thread.new_symbols.connect(self._symbols_dock_widget.set_symbols)
            self._compile_thread.start()

        else:
            self._compile_button.setIcon(self._compile_icon)
            self._compile_button.setText(self._lang.get('QPushButton.compile'))

            if self._compile_thread.isRunning(): self._compile_thread.terminate()
            self._compile_thread = None

    def _compile_done(self, missing_symbols: bool) -> None:
        self._compile_button.setIcon(self._compile_icon)
        self._compile_button.setText(self._lang.get('QPushButton.compile'))

        if self._compile_thread.isRunning(): self._compile_thread.terminate()
        self._compile_thread = None

        k = 'MissingSymbols' if missing_symbols else 'Done'
        b = self._app.save_data.kamek_compile_missing_symbols_notif if missing_symbols else self._app.save_data.kamek_compile_done_notif

        if b: self._app.sys_tray.showMessage(
            self._app.get_lang_data(f'QSystemTrayIcon.showMessage.KamekWidget.compile{k}.title').replace('%s', self._name),
            self._app.get_lang_data(f'QSystemTrayIcon.showMessage.KamekWidget.compile{k}.message'),
            QSystemTrayIcon.MessageIcon.Information,
            self._app.MESSAGE_DURATION
        )
        self._app.show_alert(
            self._app.get_lang_data(f'QSystemTrayIcon.showMessage.KamekWidget.compile{k}.message'),
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

        if self._app.save_data.kamek_compile_error_notif: self._app.sys_tray.showMessage(
            self._app.get_lang_data('QSystemTrayIcon.showMessage.KamekWidget.compileError.title').replace('%s', self._name),
            self._app.get_lang_data('QSystemTrayIcon.showMessage.KamekWidget.compileError.message'),
            QSystemTrayIcon.MessageIcon.Critical,
            self._app.MESSAGE_DURATION
        )
        self._app.show_alert(
            self._app.get_lang_data('QSystemTrayIcon.showMessage.KamekWidget.compileError.message'),
            raise_duration = self._app.ALERT_RAISE_DURATION,
            pause_duration = self._app.ALERT_PAUSE_DURATION,
            fade_duration = self._app.ALERT_FADE_DURATION,
            color = 'main'
        )

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


    def _save_dock_widgets(self) -> dict:
        if self._compile_thread is not None:
            self._compile_thread.terminate()

        self._sprites_and_actors_dock_widget.terminate_task()

        dockwidgets = {}

        for dw in self.findChildren(QDockWidget):
            dockwidgets[dw.objectName()] = dw.to_dict()

        return dockwidgets

    def export(self) -> dict:
        return super().export() | {
            'buildFolder': self._build_folder,
            'outputFolder': self._output_folder,
            'copyType': self._copy_type.value,
            'generatePALv1': self._generate_pal_v1,
            'generatePALv2': self._generate_pal_v2,
            'generateNTSCv1': self._generate_ntsc_v1,
            'generateNTSCv2': self._generate_ntsc_v2,
            'generateJPv1': self._generate_jp_v1,
            'generateJPv2': self._generate_jp_v2,
            'generateKR': self._generate_kr,
            'generateTW': self._generate_tw,
            'generateCN': self._generate_cn,
            'nintendoDriverMode': self._nintendo_driver_mode,
        }

    def reset_dock_widgets(self) -> None:
        for dw in [self._sprites_and_actors_dock_widget, self._symbols_dock_widget, self._address_converter_dock_widget]:
            dw.setVisible(True)
            dw.setFloating(False)

        self.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, self._sprites_and_actors_dock_widget)
        self.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, self._symbols_dock_widget)
        self.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, self._address_converter_dock_widget)

        if self._sprites_and_actors_dock_widget not in self.tabifiedDockWidgets(self._symbols_dock_widget):
            self.tabifyDockWidget(self._symbols_dock_widget, self._sprites_and_actors_dock_widget)

        if self._symbols_dock_widget not in self.tabifiedDockWidgets(self._address_converter_dock_widget):
            self.tabifyDockWidget(self._address_converter_dock_widget, self._symbols_dock_widget)

    def settings_updated(self, settings: QSaveData) -> None:
        self._devkitppc_path = settings.devkitppc_path
        return super().settings_updated(settings)
#----------------------------------------------------------------------
