#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QLabel
from PySide6.QtCore import Qt
from data.lib.qtUtils import QBaseApplication, QNamedLineEdit
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

        self._regiontype_label = QLabel()
        self._regiontype_label.setProperty('brighttitle', True)
        self._content_frame.grid_layout.addWidget(self._regiontype_label, 0, 0)

        self._regiontype_lineedit = QNamedLineEdit(None, '', self._lang.get_data('PropertyWidget.QNamedLineEdit.type'))
        self._regiontype_lineedit.setToolTip(self._lang.get_data('PropertyWidget.QToolTip.type'))
        self._regiontype_lineedit.line_edit.setText(self._data.type)
        self._regiontype_lineedit.line_edit.textChanged.connect(self._type_changed)
        self._regiontype_lineedit.line_edit.setMaxLength(1)
        self._property_frame.grid_layout.addWidget(self._regiontype_lineedit, 0, 0)

        self._update_text()


    def _update_text(self) -> None:
        self._regiontype_label.setText(self._lang.get_data('QLabel.type').replace('%s', self._data.type))
        self._regiontype_lineedit.line_edit.setText(self._data.type)


    def _type_changed(self, text: str) -> None:
        if not text: return

        text = text.upper()
        if not text in [chr(i) for i in range(ord('A'), ord('Z') + 1)]:
            return self._regiontype_lineedit.line_edit.setText('')

        self._data.type = text
        self._update_text()
        self.data_changed.emit()
#----------------------------------------------------------------------
