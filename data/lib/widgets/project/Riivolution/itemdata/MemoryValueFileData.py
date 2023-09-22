#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QLabel, QPushButton
from PySide6.QtCore import Qt
from data.lib.qtUtils import QBaseApplication, QNamedLineEdit, QGridWidget, QSaveData, QNamedHexSpinBox, QNamedTextEdit
from ..items.MemoryValueFile import MemoryValueFile
from .BaseSubItemData import BaseSubItemData
#----------------------------------------------------------------------

    # Class
class MemoryValueFileData(BaseSubItemData):
    type: str = 'Memory Value File'
    child_cls: MemoryValueFile = MemoryValueFile

    _back_icon = None

    _lang = {}

    def init(app: QBaseApplication) -> None:
        MemoryValueFileData._lang = app.get_lang_data('QMainWindow.QSlidingStackedWidget.mainMenu.projects.RiivolutionWidget.WiiDiscWidget.PatchData.PropertyWidget.MemoryData.MemoryValueFileData')

        MemoryValueFileData._back_icon = app.get_icon('pushbutton/back.png', True, QSaveData.IconMode.Local)

    def __init__(self, data: MemoryValueFile, path: str) -> None:
        super().__init__(data, path)

        self._disable_send = False
        self._current_widget = None

        self._text_label = QLabel()
        self._text_label.setProperty('brighttitle', True)
        self._content_frame.grid_layout.addWidget(self._text_label, 0, 0)


        self._back_button = QPushButton()
        self._back_button.setIcon(self._back_icon)
        self._back_button.setText(self._lang.get_data('QPushButton.back'))
        self._back_button.setProperty('color', 'main')
        self._back_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self._back_button.clicked.connect(self.back_pressed.emit)
        self._property_frame.grid_layout.addWidget(self._back_button, 0, 0, Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)


        subframe = QGridWidget()
        subframe.grid_layout.setSpacing(8)
        subframe.grid_layout.setContentsMargins(0, 0, 0, 0)
        self._property_frame.grid_layout.addWidget(subframe, 1, 0)


        self._offset_hexspinbox = QNamedHexSpinBox(None, self._lang.get_data('PropertyWidget.QNamedHexSpinBox.offset'))
        self._offset_hexspinbox.set_range(0, 0xFFFFFFFF)
        self._offset_hexspinbox.set_value(self._data.offset)
        self._offset_hexspinbox.value_changed.connect(self._offset_changed)
        subframe.grid_layout.addWidget(self._offset_hexspinbox, 0, 0)

        self._valuefile_lineedit = QNamedLineEdit(None, '', self._lang.get_data('PropertyWidget.QNamedLineEdit.valuefile'))
        self._valuefile_lineedit.setText(self._data.valuefile)
        self._valuefile_lineedit.text_changed.connect(self._valuefile_changed)
        subframe.grid_layout.addWidget(self._valuefile_lineedit, 0, 1)

        self._comment_lineedit = QNamedTextEdit(None, '', self._lang.get_data('PropertyWidget.QNamedTextEdit.comment'))
        self._comment_lineedit.setText(self._data.comment)
        self._comment_lineedit.text_changed.connect(self._comment_changed)
        subframe.grid_layout.addWidget(self._comment_lineedit, 1, 0, 1, 2)

        subframe.grid_layout.setRowStretch(2, 1)

        self._property_frame.grid_layout.setRowStretch(2, 1)

        self._update_text()

        self._disable_send = False


    def _update_text(self) -> None:
        s = self._lang.get_data('QLabel.text').replace('%s', f'0x{self._data.offset:X}', 1).replace('%s', self._data.valuefile, 1)
        self._text_label.setText(s)


    def _offset_changed(self, value: int) -> None:
        self._data.offset = value
        self._send_data()

    def _valuefile_changed(self, text: str) -> None:
        if text == '': return
        if not text.startswith('/'): text = f'/{text}'

        self._data.valuefile = text
        self._valuefile_lineedit.setText(text)

        self._send_data()

    def _comment_changed(self, value: str) -> None:
        self._data.comment = value
        self._send_data()


    def _send_data(self, *args) -> None:
        if self._disable_send: return

        self._update_text()
        self.data_changed.emit()
#----------------------------------------------------------------------
