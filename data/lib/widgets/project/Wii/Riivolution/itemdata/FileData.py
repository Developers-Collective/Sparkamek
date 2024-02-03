#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QLabel, QPushButton
from PySide6.QtCore import Qt
from data.lib.qtUtils import QBaseApplication, QNamedLineEdit, QNamedToggleButton, QGridWidget, QSaveData, QNamedHexSpinBox, QScrollableGridFrame, QLangData
from ..items.File import File
from .BaseSubItemData import BaseSubItemData
#----------------------------------------------------------------------

    # Class
class FileData(BaseSubItemData):
    type: str = 'File'
    child_cls: File = File

    _back_icon = None

    _lang: QLangData = QLangData.NoTranslation()

    def init(app: QBaseApplication) -> None:
        FileData._lang = app.get_lang_data('QMainWindow.QSlidingStackedWidget.mainMenu.projects.projectWidget.Wii.RiivolutionWidget.WiiDiscWidget.PatchData.PropertyWidget.FileData')

        FileData._back_icon = app.get_icon('pushbutton/back.png', True, QSaveData.IconMode.Local)

    def __init__(self, data: File, path: str) -> None:
        super().__init__(data, path)

        self._disable_send = False
        self._current_widget = None

        self._text_label = QLabel()
        self._text_label.setProperty('brighttitle', True)
        self._content_frame.grid_layout.addWidget(self._text_label, 0, 0)


        frame = QScrollableGridFrame()
        frame.set_all_property('transparent', True)
        frame.scroll_layout.setSpacing(30)
        frame.scroll_layout.setContentsMargins(0, 0, 10, 0)
        self._property_frame.grid_layout.addWidget(frame, 0, 0)

        self._back_button = QPushButton()
        self._back_button.setIcon(self._back_icon)
        self._back_button.setText(self._lang.get('QPushButton.back'))
        self._back_button.setProperty('color', 'main')
        self._back_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self._back_button.clicked.connect(self.back_pressed.emit)
        frame.scroll_layout.addWidget(self._back_button, 0, 0, Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)


        subframe = QGridWidget()
        subframe.grid_layout.setSpacing(8)
        subframe.grid_layout.setContentsMargins(0, 0, 0, 0)
        frame.scroll_layout.addWidget(subframe, 1, 0)


        self._disc_lineedit = QNamedLineEdit(None, '', self._lang.get('PropertyWidget.QNamedLineEdit.disc'))
        self._disc_lineedit.setToolTip(self._lang.get('PropertyWidget.QToolTip.disc'))
        self._disc_lineedit.line_edit.setText(self._data.disc)
        self._disc_lineedit.line_edit.textChanged.connect(self._disc_changed)
        subframe.grid_layout.addWidget(self._disc_lineedit, 0, 0)

        self._external_lineedit = QNamedLineEdit(None, '', self._lang.get('PropertyWidget.QNamedLineEdit.external'))
        self._external_lineedit.setToolTip(self._lang.get('PropertyWidget.QToolTip.external'))
        self._external_lineedit.line_edit.setText(self._data.external)
        self._external_lineedit.line_edit.textChanged.connect(self._external_changed)
        subframe.grid_layout.addWidget(self._external_lineedit, 0, 1)

        self._resize_togglebutton = QNamedToggleButton(None, self._lang.get('PropertyWidget.QNamedToggleButton.resize'), self._data.resize, True)
        self._resize_togglebutton.setToolTip(self._lang.get('PropertyWidget.QToolTip.resize'))
        self._resize_togglebutton.toggled.connect(self._resize_toggled)
        subframe.grid_layout.addWidget(self._resize_togglebutton, 1, 0)

        self._create_togglebutton = QNamedToggleButton(None, self._lang.get('PropertyWidget.QNamedToggleButton.create'), self._data.create_, True)
        self._create_togglebutton.setToolTip(self._lang.get('PropertyWidget.QToolTip.create'))
        self._create_togglebutton.toggled.connect(self._create_toggled)
        subframe.grid_layout.addWidget(self._create_togglebutton, 1, 1)

        self._offset_hexspinbox = QNamedHexSpinBox(None, self._lang.get('PropertyWidget.QNamedHexSpinBox.offset'))
        self._offset_hexspinbox.setToolTip(self._lang.get('PropertyWidget.QToolTip.offset'))
        self._offset_hexspinbox.set_value(self._data.offset)
        self._offset_hexspinbox.value_changed.connect(self._offset_changed)
        subframe.grid_layout.addWidget(self._offset_hexspinbox, 2, 0)

        self._length_hexspinbox = QNamedHexSpinBox(None, self._lang.get('PropertyWidget.QNamedHexSpinBox.length'))
        self._length_hexspinbox.setToolTip(self._lang.get('PropertyWidget.QToolTip.length'))
        self._length_hexspinbox.set_range(0, 0xFFFFFFFF)
        self._length_hexspinbox.set_value(self._data.length)
        self._length_hexspinbox.value_changed.connect(self._length_changed)
        subframe.grid_layout.addWidget(self._length_hexspinbox, 2, 1)

        subframe.grid_layout.setRowStretch(3, 1)

        frame.scroll_layout.setRowStretch(2, 1)

        self._update_text()

        self._disable_send = False


    def _update_text(self) -> None:
        s = self._lang.get('QLabel.text').replace('%s', self._data.external, 1).replace('%s', self._data.disc, 1)
        self._text_label.setText(s)


    def _disc_changed(self, text: str) -> None:
        if not text: return

        if not text.startswith('/'): text = f'/{text}'
        self._disc_lineedit.setText(text)

        self._data.disc = text
        self._send_data()

    def _external_changed(self, text: str) -> None:
        if not text: return

        self._data.external = text
        self._send_data()

    def _resize_toggled(self, checked: bool) -> None:
        self._data.resize = checked
        self._send_data()

    def _create_toggled(self, checked: bool) -> None:
        self._data.create_ = checked
        self._send_data()

    def _offset_changed(self, text: str) -> None:
        if not text: return

        text = text.replace('0x', '')
        new_text = ''
        for c in text.upper():
            if c in '0123456789ABCDEF': new_text += c

        try: value = int(text, 16)
        except ValueError:
            self._offset_hexspinbox.setText(f'0x{hex(self._data.offset)[2:].upper()}')
            return

        self._data.offset = value
        self._send_data()

    def _length_changed(self, value: int) -> None:
        self._data.length = value
        self._send_data()


    def _send_data(self, *args) -> None:
        if self._disable_send: return

        self._update_text()
        self.data_changed.emit()
#----------------------------------------------------------------------
