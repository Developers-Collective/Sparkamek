#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QLabel, QPushButton
from PySide6.QtCore import Qt
from data.lib.QtUtils import QBaseApplication, QNamedLineEdit, QGridWidget, QSaveData, QNamedHexSpinBox, QNamedTextEdit, QNamedSpinBox, QScrollableGridFrame, QLangData
from ..items.MemorySearchValueFile import MemorySearchValueFile
from .BaseSubItemData import BaseSubItemData
#----------------------------------------------------------------------

    # Class
class MemorySearchValueFileData(BaseSubItemData):
    type: str = 'Memory Search Value File'
    child_cls: MemorySearchValueFile = MemorySearchValueFile

    _back_icon = None

    _lang: QLangData = QLangData.NoTranslation()

    def init(app: QBaseApplication) -> None:
        MemorySearchValueFileData._lang = app.get_lang_data('QMainWindow.QSlidingStackedWidget.mainMenu.projects.projectWidget.Wii.RiivolutionWidget.WiiDiscWidget.PatchData.PropertyWidget.MemoryData.MemorySearchValueFileData')

        MemorySearchValueFileData._back_icon = app.get_icon('pushbutton/back.png', True, QSaveData.IconMode.Local)

    def __init__(self, data: MemorySearchValueFile, path: str) -> None:
        super().__init__(data, path)

        self._disable_send = False
        self._current_widget = None

        self._text_label = QLabel()
        self._text_label.setProperty('brighttitle', True)
        self._content_frame.layout_.addWidget(self._text_label, 0, 0)


        frame = QScrollableGridFrame()
        frame.set_all_property('transparent', True)
        frame.layout_.setSpacing(30)
        frame.layout_.setContentsMargins(0, 0, 10, 0)
        self._property_frame.layout_.addWidget(frame, 0, 0)

        self._back_button = QPushButton()
        self._back_button.setIcon(self._back_icon)
        self._back_button.setText(self._lang.get('QPushButton.back'))
        self._back_button.setProperty('color', 'main')
        self._back_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self._back_button.clicked.connect(self.back_pressed.emit)
        frame.layout_.addWidget(self._back_button, 0, 0, Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)


        subframe = QGridWidget()
        subframe.layout_.setSpacing(8)
        subframe.layout_.setContentsMargins(0, 0, 0, 0)
        frame.layout_.addWidget(subframe, 1, 0)


        self._original_hexspinbox = QNamedHexSpinBox(None, self._lang.get('PropertyWidget.QNamedHexSpinBox.original'))
        self._original_hexspinbox.setToolTip(self._lang.get('PropertyWidget.QToolTip.original'))
        self._original_hexspinbox.set_range(0, 0xFFFFFFFFFFFFFFFF)
        self._original_hexspinbox.set_value(self._data.original)
        self._original_hexspinbox.value_changed.connect(self._original_changed)
        subframe.layout_.addWidget(self._original_hexspinbox, 0, 0)

        self._valuefile_lineedit = QNamedLineEdit(None, '', self._lang.get('PropertyWidget.QNamedLineEdit.valuefile'))
        self._valuefile_lineedit.setToolTip(self._lang.get('PropertyWidget.QToolTip.valuefile'))
        self._valuefile_lineedit.setText(self._data.valuefile)
        self._valuefile_lineedit.text_changed.connect(self._valuefile_changed)
        subframe.layout_.addWidget(self._valuefile_lineedit, 1, 0)

        self._align_spinbox = QNamedSpinBox(None, self._lang.get('PropertyWidget.QNamedSpinBox.align'))
        self._align_spinbox.setToolTip(self._lang.get('PropertyWidget.QToolTip.align'))
        self._align_spinbox.set_range(1, 65535)
        self._align_spinbox.set_value(self._data.align)
        self._align_spinbox.value_changed.connect(self._align_changed)
        subframe.layout_.addWidget(self._align_spinbox, 2, 0)

        self._comment_lineedit = QNamedTextEdit(None, '', self._lang.get('PropertyWidget.QNamedTextEdit.comment'))
        self._comment_lineedit.setToolTip(self._lang.get('PropertyWidget.QToolTip.comment'))
        self._comment_lineedit.setText(self._data.comment)
        self._comment_lineedit.text_changed.connect(self._comment_changed)
        subframe.layout_.addWidget(self._comment_lineedit, 3, 0)

        subframe.layout_.setRowStretch(4, 1)

        frame.layout_.setRowStretch(2, 1)

        self._update_text()

        self._disable_send = False


    def update_title_text(self) -> None:
        comment = self._data.comment.replace('\n', '')
        if len(comment) > 32: comment = f'{comment[:32]}...'
        self._type_label.setText(f'{self.type}' + (f' • {comment}' if comment else ''))

    def _update_text(self) -> None:
        s = self._lang.get('QLabel.text').replace('%s', f'0x{self._data.original:X}', 1).replace('%s', self._data.valuefile, 1).replace('%s', f'{self._data.align}', 1)
        self._text_label.setText(s)


    def _original_changed(self, value: int) -> None:
        self._data.original = value
        self._send_data()

    def _valuefile_changed(self, text: str) -> None:
        if text == '': return
        if not text.startswith('/'): text = f'/{text}'

        self._data.valuefile = text
        self._valuefile_lineedit.setText(text)

        self._send_data()

    def _align_changed(self, value: int) -> None:
        self._data.align = value
        self._send_data()

    def _comment_changed(self, value: str) -> None:
        self._data.comment = value
        self._send_data()


    def _send_data(self, *args) -> None:
        if self._disable_send: return

        self.update_title_text()
        self._update_text()
        self.data_changed.emit()
#----------------------------------------------------------------------
