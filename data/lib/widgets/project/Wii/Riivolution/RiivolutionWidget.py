#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QPushButton, QDockWidget, QLabel
from PySide6.QtCore import Qt
from ...SubProjectWidgetBase import SubProjectWidgetBase
from data.lib.QtUtils import QBaseApplication, QGridWidget, QSaveData, QLangData
from ..Wii import Wii
from data.lib.storage.xml import XML
from .WiiDiscWidget import WiiDiscWidget
from .items import WiiDisc
from .ItemDataPropertyDockWidget import ItemDataPropertyDockWidget
import os
#----------------------------------------------------------------------

    # Class
class RiivolutionWidget(SubProjectWidgetBase):
    type: str = Wii.Riivolution

    _load_icon = None
    _save_icon = None

    _lang: QLangData = QLangData.NoTranslation()

    def init(app: QBaseApplication) -> None:
        RiivolutionWidget._app = app
        RiivolutionWidget._lang = app.get_lang_data('QMainWindow.QSlidingStackedWidget.mainMenu.projects.projectWidget.Wii.RiivolutionWidget')

        RiivolutionWidget._load_icon = app.get_icon('pushbutton/load.png', True, QSaveData.IconMode.Local)
        RiivolutionWidget._save_icon = app.get_icon('pushbutton/save.png', True, QSaveData.IconMode.Local)

        WiiDiscWidget.init(app)

    def __init__(self, app: QBaseApplication, name: str, icon: str, data: dict) -> None:
        super().__init__(app, data)

        self.layout_.setSpacing(20)

        dockwidgets = data.get('dockwidgets', {})

        self._item_data_property_dock_widget = ItemDataPropertyDockWidget(app, name, icon, data)

        if 'itemDataProperty' in dockwidgets: self._item_data_property_dock_widget.load_dict(self, dockwidgets['itemDataProperty'])
        else: self.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, self._item_data_property_dock_widget)

        topframe = QGridWidget()
        topframe.layout_.setContentsMargins(0, 0, 0, 0)
        topframe.layout_.setSpacing(8)
        self._root.layout_.addWidget(topframe, 0, 0, Qt.AlignmentFlag.AlignTop)

        self._load_button = QPushButton(self._lang.get('QPushButton.load'))
        self._load_button.setIcon(self._load_icon)
        self._load_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self._load_button.setProperty('icon-padding', True)
        self._load_button.setProperty('color', 'main')
        self._load_button.clicked.connect(self._load)
        topframe.layout_.addWidget(self._load_button, 0, 0, Qt.AlignmentFlag.AlignLeft)

        self._save_button = QPushButton(self._lang.get('QPushButton.save'))
        self._save_button.setIcon(self._save_icon)
        self._save_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self._save_button.setProperty('icon-padding', True)
        self._save_button.setProperty('color', 'main')
        self._save_button.clicked.connect(self._save)
        topframe.layout_.addWidget(self._save_button, 0, 1, Qt.AlignmentFlag.AlignRight)


        topframe = QGridWidget()
        topframe.layout_.setContentsMargins(0, 0, 0, 0)
        topframe.layout_.setSpacing(8)
        self._root.layout_.addWidget(topframe, 1, 0, Qt.AlignmentFlag.AlignTop)

        label = QLabel(self._lang.get('QLabel.description')
            .replace('%s', f'<a href="https://riivolution.github.io/wiki/Patch_Format/" style="color: {self._app.COLOR_LINK.hex}; text-decoration: none;">Riivolution Patch Format Wiki</a>', 1)
            .replace('%s', f'<a href="https://riivolution.github.io/wiki/RiiFS/" style="color: {self._app.COLOR_LINK.hex}; text-decoration: none;">RiiFS Wiki</a>', 1)
        )
        label.setOpenExternalLinks(True)
        label.setWordWrap(True)
        label.setProperty('brighttitle', True)
        topframe.layout_.addWidget(label, 0, 0)


        self._wii_disc_widget = WiiDiscWidget(self._path)
        self._wii_disc_widget.property_entry_selected.connect(self._item_data_property_dock_widget.set_widget)
        self._wii_disc_widget.setDisabled(True)
        self._root.layout_.addWidget(self._wii_disc_widget, 2, 0)

        self._wii_disc_widget.wiidisc = WiiDisc(WiiDisc.create().export())
        self._wii_disc_widget.setDisabled(False)
        self._item_data_property_dock_widget.set_widget(None)


    @property
    def task_is_running(self) -> bool:
        return False


    def _save_dock_widgets(self) -> dict:
        dockwidgets = {}

        for dw in self.findChildren(QDockWidget):
            dockwidgets[dw.objectName()] = dw.to_dict()

        return dockwidgets


    def reset_dock_widgets(self) -> None:
        for dw in [self._item_data_property_dock_widget]:
            dw.setVisible(True)
            dw.setFloating(False)

        self.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, self._item_data_property_dock_widget)


    def export(self) -> dict:
        return super().export()


    def _load(self) -> None:
        self._wii_disc_widget.wiidisc = WiiDisc(XML.parse_file(self._path))
        self._wii_disc_widget.setDisabled(False)
        self._item_data_property_dock_widget.set_widget(None)

    def _save(self) -> None:
        if self._wii_disc_widget.wiidisc is None: return

        try:
            path = f'{self.path}'
            if not os.path.exists(f'{path}.bak'):
                os.rename(path, f'{path}.bak')

                s = str(self._wii_disc_widget.wiidisc.export().export(indent = 4)) # If an error occurs, the old file won't be overwritten

            with open(path, 'w', encoding = 'utf-8') as f:
                f.write(s)

            self._app.show_alert(
                self._app.get_lang_data('QSystemTrayIcon.showMessage.game.Wii.RiivolutionWidget.successfullySaved.message'),
                raise_duration = self._app.ALERT_RAISE_DURATION,
                pause_duration = self._app.ALERT_PAUSE_DURATION,
                fade_duration = self._app.ALERT_FADE_DURATION,
                color = 'main'
            )

        except Exception as e:
            self._app.show_alert(
                self._app.get_lang_data('QSystemTrayIcon.showMessage.game.Wii.RiivolutionWidget.errorWhileSaving.message').replace('%s', str(e)),
                raise_duration = self._app.ALERT_RAISE_DURATION,
                pause_duration = self._app.ALERT_PAUSE_DURATION,
                fade_duration = self._app.ALERT_FADE_DURATION,
                color = 'main'
            )
#----------------------------------------------------------------------
