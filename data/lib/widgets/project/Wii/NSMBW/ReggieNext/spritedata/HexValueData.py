#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QLabel
from PySide6.QtCore import QSize
from data.lib.QtUtils import QBaseApplication, QSaveData, QNamedLineEdit, QIconWidget
from .BaseItemData import BaseItemData
from .NybbleData import NybbleData
from ..sprites.HexValue import HexValue
#----------------------------------------------------------------------

    # Class
class HexValueData(BaseItemData):
    type: str = 'HexValue'
    child_cls = HexValue
    nybble_type = NybbleData.Type.All & (~NybbleData.Type.Bit)

    _sublang = {}

    _value_icon = None
    _icon_size = QSize(24, 24)

    def init(app: QBaseApplication) -> None:
        HexValueData._sublang = app.get_lang_data('QMainWindow.QSlidingStackedWidget.mainMenu.projects.projectWidget.Wii.NSMBW.ReggieNextWidget.SpriteWidget.HexValueData')
        HexValueData._value_icon = app.get_icon('baseitemdata/hexvalue.png', True, QSaveData.IconMode.Local)

        HexValueData.type = app.get_lang_data(f'QMainWindow.QSlidingStackedWidget.mainMenu.projects.projectWidget.Wii.NSMBW.ReggieNextWidget.type.{HexValue.name}')

    def __init__(self, data: HexValue, path: str) -> None:
        super().__init__(data, path)

        self._title_label = QLabel(self._data.title)
        self._title_label.setProperty('brighttitle', True)
        self._content_frame.grid_layout.addWidget(self._title_label, 0, 0)

        iw = QIconWidget(None, self._value_icon, self._icon_size, False)
        self._content_frame.grid_layout.addWidget(iw, 0, 1)

        self._content_frame.grid_layout.setColumnStretch(2, 1)

        self._property_last_frame.title_lineedit = QNamedLineEdit(None, '', self._sublang.get('QNamedLineEdit.title'))
        self._property_last_frame.title_lineedit.setText(self._data.title)
        self._property_last_frame.title_lineedit.line_edit.textChanged.connect(self._title_changed)
        self._property_last_frame.grid_layout.addWidget(self._property_last_frame.title_lineedit, 0, 0)


    def _title_changed(self) -> None:
        self._data.title = self._property_last_frame.title_lineedit.text()
        self._title_label.setText(self._data.title)
        self.data_changed.emit()
#----------------------------------------------------------------------
