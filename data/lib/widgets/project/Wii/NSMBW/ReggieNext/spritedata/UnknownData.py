#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QLabel
from PySide6.QtCore import QSize
from data.lib.QtUtils import QBaseApplication, QSaveData, QNamedLineEdit, QIconWidget
from .BaseItemData import BaseItemData
from .NybbleData import NybbleData
from ..sprites.Unknown import Unknown
#----------------------------------------------------------------------

    # Class
class UnknownData(BaseItemData):
    type: str = 'Unknown'
    child_cls = Unknown
    nybble_type = NybbleData.Type.All & (~NybbleData.Type.Bit)

    _value_icon = None
    _icon_size = QSize(24, 24)

    def init(app: QBaseApplication) -> None:
        UnknownData._value_icon = app.get_icon('baseitemdata/unknown.png', True, QSaveData.IconMode.Local)

        UnknownData.type = app.get_lang_data(f'QMainWindow.QSlidingStackedWidget.mainMenu.projects.projectWidget.Wii.NSMBW.ReggieNextWidget.type.{Unknown.name}')

    def __init__(self, data: Unknown, path: str) -> None:
        super().__init__(data, path)

        self._title_label = QLabel(self._data.title)
        self._title_label.setProperty('brighttitle', True)
        self._content_frame.grid_layout.addWidget(self._title_label, 0, 0)

        iw = QIconWidget(None, self._value_icon, self._icon_size, False)
        self._content_frame.grid_layout.addWidget(iw, 0, 1)

        self._content_frame.grid_layout.setColumnStretch(2, 1)
#----------------------------------------------------------------------
