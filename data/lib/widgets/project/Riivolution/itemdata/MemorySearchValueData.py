#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QLabel, QPushButton
from PySide6.QtCore import Qt
from data.lib.qtUtils import QBaseApplication, QNamedTextEdit, QGridWidget, QSaveData, QNamedHexSpinBox, QNamedSpinBox
from ..items.MemorySearchValue import MemorySearchValue
from .BaseSubItemData import BaseSubItemData
#----------------------------------------------------------------------

    # Class
class MemorySearchValueData(BaseSubItemData):
    type: str = 'Memory Search Value'
    child_cls: MemorySearchValue = MemorySearchValue

    _back_icon = None

    _lang = {}

    def init(app: QBaseApplication) -> None:
        MemorySearchValueData._lang = app.get_lang_data('QMainWindow.QSlidingStackedWidget.mainMenu.projects.RiivolutionWidget.WiiDiscWidget.PatchData.PropertyWidget.MemoryData.MemorySearchValueData')

        MemorySearchValueData._back_icon = app.get_icon('pushbutton/back.png', True, QSaveData.IconMode.Local)

    def __init__(self, data: MemorySearchValue, path: str) -> None:
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


        self._original_hexspinbox = QNamedHexSpinBox(None, self._lang.get_data('PropertyWidget.QNamedHexSpinBox.original'))
        self._original_hexspinbox.setToolTip(self._lang.get_data('PropertyWidget.QToolTip.original'))
        self._original_hexspinbox.set_range(0, 0xFFFFFFFFFFFFFFFF)
        self._original_hexspinbox.set_value(self._data.original)
        self._original_hexspinbox.value_changed.connect(self._original_changed)
        subframe.grid_layout.addWidget(self._original_hexspinbox, 0, 0)

        self._value_hexspinbox = QNamedHexSpinBox(None, self._lang.get_data('PropertyWidget.QNamedHexSpinBox.value'))
        self._value_hexspinbox.setToolTip(self._lang.get_data('PropertyWidget.QToolTip.value'))
        self._value_hexspinbox.set_range(0, 0xFFFFFFFFFFFFFFFF)
        self._value_hexspinbox.set_value(self._data.value)
        self._value_hexspinbox.value_changed.connect(self._value_changed)
        subframe.grid_layout.addWidget(self._value_hexspinbox, 1, 0)

        self._align_spinbox = QNamedSpinBox(None, self._lang.get_data('PropertyWidget.QNamedSpinBox.align'))
        self._align_spinbox.setToolTip(self._lang.get_data('PropertyWidget.QToolTip.align'))
        self._align_spinbox.set_range(1, 65535)
        self._align_spinbox.set_value(self._data.align)
        self._align_spinbox.value_changed.connect(self._align_changed)
        subframe.grid_layout.addWidget(self._align_spinbox, 2, 0)

        self._comment_lineedit = QNamedTextEdit(None, '', self._lang.get_data('PropertyWidget.QNamedTextEdit.comment'))
        self._comment_lineedit.setToolTip(self._lang.get_data('PropertyWidget.QToolTip.comment'))
        self._comment_lineedit.setText(self._data.comment)
        self._comment_lineedit.text_changed.connect(self._comment_changed)
        subframe.grid_layout.addWidget(self._comment_lineedit, 3, 0)

        subframe.grid_layout.setRowStretch(4, 1)

        self._property_frame.grid_layout.setRowStretch(2, 1)

        self._update_text()

        self._disable_send = False


    def _update_text(self) -> None:
        s = self._lang.get_data('QLabel.text').replace('%s', f'0x{self._data.original:X}', 1).replace('%s', f'0x{self._data.value:X}', 1).replace('%s', f'{self._data.align:X}', 1)
        self._text_label.setText(s)


    def _original_changed(self, value: int) -> None:
        self._data.original = value
        self._send_data()

    def _value_changed(self, value: int) -> None:
        self._data.value = value
        self._send_data()

    def _align_changed(self, value: int) -> None:
        self._data.align = value
        self._send_data()

    def _comment_changed(self, text: str) -> None:
        self._data.comment = text
        self._send_data()


    def _send_data(self, *args) -> None:
        if self._disable_send: return

        self._update_text()
        self.data_changed.emit()
#----------------------------------------------------------------------
