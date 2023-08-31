#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QPushButton
from PySide6.QtCore import Qt
from ..SubProjectWidgetBase import SubProjectWidgetBase
from data.lib.qtUtils import QBaseApplication, QGridWidget, QSaveData
from data.lib.widgets.ProjectKeys import ProjectKeys
from data.lib.storage.xml import XML
from .WiiDiscWidget import WiiDiscWidget
from .items import WiiDisc
#----------------------------------------------------------------------

    # Class
class RiivolutionWidget(SubProjectWidgetBase):
    type: ProjectKeys = ProjectKeys.Riivolution

    _load_icon = None
    _save_icon = None

    _lang = {}

    def init(app: QBaseApplication) -> None:
        RiivolutionWidget._app = app
        RiivolutionWidget._lang = app.get_lang_data('QMainWindow.QSlidingStackedWidget.mainMenu.projects.RiivolutionWidget')

        RiivolutionWidget._load_icon = app.get_icon('pushbutton/load.png', True, QSaveData.IconMode.Local)
        RiivolutionWidget._save_icon = app.get_icon('pushbutton/save.png', True, QSaveData.IconMode.Local)

        WiiDiscWidget.init(app)

    def __init__(self, app: QBaseApplication, name: str, icon: str, data: dict) -> None:
        super().__init__(app, data)

        topframe = QGridWidget()
        topframe.grid_layout.setContentsMargins(0, 0, 0, 0)
        topframe.grid_layout.setSpacing(8)
        self._root.scroll_layout.addWidget(topframe, 0, 0, Qt.AlignmentFlag.AlignTop)

        self._load_button = QPushButton(self._lang.get_data('QPushButton.load'))
        self._load_button.setIcon(self._load_icon)
        self._load_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self._load_button.setProperty('icon-padding', True)
        self._load_button.setProperty('color', 'main')
        self._load_button.clicked.connect(self._load)
        topframe.grid_layout.addWidget(self._load_button, 0, 0, Qt.AlignmentFlag.AlignLeft)

        self._save_button = QPushButton(self._lang.get_data('QPushButton.save'))
        self._save_button.setIcon(self._save_icon)
        self._save_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self._save_button.setProperty('icon-padding', True)
        self._save_button.setProperty('color', 'main')
        self._save_button.clicked.connect(self._save)
        topframe.grid_layout.addWidget(self._save_button, 0, 1, Qt.AlignmentFlag.AlignRight)


        self._wii_disc_widget = WiiDiscWidget(self._path)
        self._wii_disc_widget.setDisabled(True)
        self._root.scroll_layout.addWidget(self._wii_disc_widget, 1, 0)


    def _load(self) -> None:
        self._wii_disc_widget.wiidisc = WiiDisc(XML.parse_file(self._path))
        self._wii_disc_widget.setDisabled(False)

    def _save(self) -> None:
        pass
#----------------------------------------------------------------------
