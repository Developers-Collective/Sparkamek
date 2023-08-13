#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QLabel
from PySide6.QtCore import QSize
from data.lib.qtUtils import QGridWidget, QBaseApplication, QSaveData, QNamedLineEdit, QIconWidget
from .BaseItemData import BaseItemData
from ..sprites.Value import Value
#----------------------------------------------------------------------

    # Class
class ValueData(BaseItemData):
    type: str = 'Value'

    _sublang = {}

    _value_icon = None
    _icon_size = QSize(120, 16)

    def init(app: QBaseApplication) -> None:
        ValueData._sublang = app.get_lang_data('QMainWindow.QSlidingStackedWidget.mainMenu.projects.ReggieNextWidget.SpriteWidget.ValueData')
        ValueData._value_icon = app.get_icon('baseitemdata/value.png', True, QSaveData.IconMode.Local)

    def __init__(self, data: Value) -> None:
        super().__init__(data)

        self._title_label = QLabel(self._data.title)
        self._title_label.setProperty('brighttitle', True)
        self._content_frame.grid_layout.addWidget(self._title_label, 0, 0)

        self._idtype_label = QLabel(self._data.idtype)
        self._idtype_label.setProperty('indice', True)
        self._content_frame.grid_layout.addWidget(self._idtype_label, 0, 1)

        iw = QIconWidget(None, self._value_icon, self._icon_size, False)
        self._content_frame.grid_layout.addWidget(iw, 0, 2)

        self._content_frame.grid_layout.setColumnStretch(3, 1)

        self._property_last_frame.title_lineedit = QNamedLineEdit(None, '', self._sublang.get_data('QNamedLineEdit.title'))
        self._property_last_frame.title_lineedit.setText(self._data.title)
        self._property_last_frame.title_lineedit.line_edit.textChanged.connect(self._title_changed)
        self._property_last_frame.grid_layout.addWidget(self._property_last_frame.title_lineedit, 0, 0)

        self._property_last_frame.idtype_lineedit = QNamedLineEdit(None, '', self._sublang.get_data('QNamedLineEdit.idtype'))
        self._property_last_frame.idtype_lineedit.setText(self._data.idtype)
        self._property_last_frame.idtype_lineedit.line_edit.textChanged.connect(self._idtype_changed)
        self._property_last_frame.grid_layout.addWidget(self._property_last_frame.idtype_lineedit, 0, 1)


    def _title_changed(self) -> None:
        self._data.title = self._property_last_frame.title_lineedit.text()
        self._title_label.setText(self._data.title)
        self.data_changed.emit()

    def _idtype_changed(self) -> None:
        self._data.idtype = self._property_last_frame.idtype_lineedit.text()
        self._idtype_label.setText(self._data.idtype)
        self.data_changed.emit()
#----------------------------------------------------------------------