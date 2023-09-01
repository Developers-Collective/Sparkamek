#----------------------------------------------------------------------

    # Libraries
from PySide6.QtGui import QMouseEvent
from PySide6.QtWidgets import QLabel, QPushButton
from PySide6.QtCore import Qt
from data.lib.qtUtils import QGridWidget, QBaseApplication
from ..items.Region import Region
from .BaseItemData import BaseItemData
#----------------------------------------------------------------------

    # Class
class RegionData(BaseItemData):
    type: str = 'Region'
    child_cls: Region = Region

    _lang = {}

    def init(app: QBaseApplication) -> None:
        RegionData._lang = app.get_lang_data('QMainWindow.QSlidingStackedWidget.mainMenu.projects.RiivolutionWidget.WiiDiscWidget.IDWidget.RegionData')

    def __init__(self, data: Region, path: str) -> None:
        super().__init__(data, path)

        self._type_label = QLabel()
        self._type_label.setProperty('brighttitle', True)
        self._content_frame.grid_layout.addWidget(self._type_label, 0, 0)
        self._update_text()

    def _update_text(self) -> None:
        self._type_label.setText(self._lang.get_data('QLabel.type').replace('%s', self._data.type))
#----------------------------------------------------------------------
