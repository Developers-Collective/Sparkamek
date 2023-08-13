#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QLabel
from PySide6.QtCore import QSize
from data.lib.qtUtils import QBaseApplication, QSaveData, QNamedLineEdit, QIconWidget
from .BaseItemData import BaseItemData
from ..sprites.CheckBox import CheckBox
#----------------------------------------------------------------------

    # Class
class CheckBoxData(BaseItemData):
    type: str = 'Check Box'

    _sublang = {}

    _checkbox_icon = None
    _icon_size = QSize(16, 16)

    def init(app: QBaseApplication) -> None:
        CheckBoxData._sublang = app.get_lang_data('QMainWindow.QSlidingStackedWidget.mainMenu.projects.ReggieNextWidget.SpriteWidget.CheckBoxData')
        CheckBoxData._checkbox_icon = app.get_icon('baseitemdata/checkbox.png', True, QSaveData.IconMode.Local)

    def __init__(self, data: CheckBox) -> None:
        super().__init__(data)

        self._title_label = QLabel(self._data.title)
        self._title_label.setProperty('brighttitle', True)
        self._content_frame.grid_layout.addWidget(self._title_label, 0, 0)

        iw = QIconWidget(None, self._checkbox_icon, self._icon_size, False)
        self._content_frame.grid_layout.addWidget(iw, 0, 1)

        self._content_frame.grid_layout.setColumnStretch(2, 1)

        self._property_last_frame.title_lineedit = QNamedLineEdit(None, '', self._sublang.get_data('QNamedLineEdit.title'))
        self._property_last_frame.title_lineedit.setText(self._data.title)
        self._property_last_frame.title_lineedit.line_edit.textChanged.connect(self._title_changed)
        self._property_last_frame.grid_layout.addWidget(self._property_last_frame.title_lineedit, 0, 0)


    def _title_changed(self) -> None:
        self._data.title = self._property_last_frame.title_lineedit.text()
        self._title_label.setText(self._data.title)
        self.data_changed.emit()
#----------------------------------------------------------------------
