#----------------------------------------------------------------------

    # Libraries
from PySide6.QtGui import QMouseEvent
from PySide6.QtWidgets import QLabel, QPushButton
from PySide6.QtCore import Qt, Signal
from data.lib.qtUtils import QDragListItem, QGridWidget, QBaseApplication, QSaveData, QNamedTextEdit, QNamedToggleButton, QNamedComboBox
from ..sprites.BaseItem import BaseItem
from ..sprites.Nybble import Nybble
#----------------------------------------------------------------------

    # Class
class BaseItemData(QDragListItem):
    type: str = 'BaseItem'

    deleted = Signal(QDragListItem)
    selected = Signal(QDragListItem, QGridWidget or None)
    data_changed = Signal()

    _lang = {}

    _delete_icon = None

    def init(app: QBaseApplication) -> None:
        BaseItemData._lang = app.get_lang_data('QMainWindow.QSlidingStackedWidget.mainMenu.projects.ReggieNextWidget.SpriteWidget.BaseItemData')
        BaseItemData._delete_icon = app.get_icon('pushbutton/deleteBig.png', True, QSaveData.IconMode.Local)

    def __init__(self, data: BaseItem) -> None:
        super().__init__()

        self.setProperty('color', 'main')
        self.setProperty('side', 'all')
        self.setProperty('checkable', True)
        self.setProperty('checked', False)
        self.setProperty('bottom-border-only', True)
        self.setProperty('border-radius', 8)

        self._data = data

        self.grid_layout.setContentsMargins(10, 10, 10, 10)
        self.grid_layout.setSpacing(8)


        top_frame = QGridWidget()
        top_frame.grid_layout.setContentsMargins(0, 0, 0, 0)
        top_frame.grid_layout.setSpacing(8)
        self.grid_layout.addWidget(top_frame, 0, 0)

        topleft_frame = QGridWidget()
        topleft_frame.grid_layout.setContentsMargins(0, 0, 0, 0)
        topleft_frame.grid_layout.setSpacing(8)
        top_frame.grid_layout.addWidget(topleft_frame, 0, 0)

        self._type_label = QLabel()
        # self._type_label.setProperty('bigbrighttitle', True)
        self._type_label.setProperty('brightsubtitle', True)
        topleft_frame.grid_layout.addWidget(self._type_label, 0, 0, Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self._update_title_text()

        self._content_frame = QGridWidget()
        self._content_frame.grid_layout.setContentsMargins(0, 0, 0, 0)
        self._content_frame.grid_layout.setSpacing(8)
        topleft_frame.grid_layout.addWidget(self._content_frame, 1, 0)


        topright_frame = QGridWidget()
        topright_frame.grid_layout.setContentsMargins(0, 0, 0, 0)
        topright_frame.grid_layout.setSpacing(8)
        top_frame.grid_layout.addWidget(topright_frame, 0, 1, Qt.AlignmentFlag.AlignRight)
        topright_frame.grid_layout.setColumnStretch(2, 1)

        delete_button = QPushButton()
        delete_button.clicked.connect(self._delete)
        delete_button.setIcon(self._delete_icon)
        delete_button.setProperty('color', 'main')
        delete_button.setCursor(Qt.CursorShape.PointingHandCursor)
        topright_frame.grid_layout.addWidget(delete_button, 0, 0, Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignRight)


        bottom_frame = QGridWidget()
        bottom_frame.grid_layout.setContentsMargins(0, 0, 0, 0)
        bottom_frame.grid_layout.setSpacing(8)
        self.grid_layout.addWidget(bottom_frame, 1, 0)

        self._nybbles_label = QLabel()
        self._nybbles_label.setProperty('title', True)
        bottom_frame.grid_layout.addWidget(self._nybbles_label, 0, 0, Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignLeft)

        self._settings_label = QLabel()
        self._settings_label.setProperty('title', True)
        bottom_frame.grid_layout.addWidget(self._settings_label, 0, 1, Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignRight)

        self._update_nybbles_settings_text()


        self._property_frame = QGridWidget()
        self._property_frame.grid_layout.setContentsMargins(0, 0, 0, 0)
        self._property_frame.grid_layout.setSpacing(20)


        nybble_frame = QGridWidget()
        nybble_frame.grid_layout.setContentsMargins(0, 0, 0, 0)
        nybble_frame.grid_layout.setSpacing(8)
        self._property_frame.grid_layout.addWidget(nybble_frame, self._property_frame.grid_layout.rowCount(), 0)
        nybble_frame.grid_layout.setColumnStretch(6, 1)

        self._property_frame._first_nybble_combobox = QNamedComboBox(None, self._lang.get_data('QNamedComboBox.firstNybble'))
        self._property_frame._first_nybble_combobox.combo_box.addItems([str(i) for i in range(1, 17)])
        self._property_frame._first_nybble_combobox.combo_box.setCurrentIndex(self._data.nybble.start.n - 1)
        self._property_frame._first_nybble_combobox.combo_box.currentIndexChanged.connect(self._first_nybble_changed)
        nybble_frame.grid_layout.addWidget(self._property_frame._first_nybble_combobox, 0, 0)

        label = QLabel('.')
        label.setProperty('brighttitle', True)
        nybble_frame.grid_layout.addWidget(label, 0, 1)

        self._property_frame._first_nybblebit_combobox = QNamedComboBox(None, self._lang.get_data('QNamedComboBox.firstNybbleBit'))
        self._property_frame._first_nybblebit_combobox.combo_box.addItems(['None'] + [str(i) for i in range(1, 5)])
        self._property_frame._first_nybblebit_combobox.combo_box.setCurrentIndex((self._data.nybble.start.b + 1) if self._data.nybble.start.b is not None else 0)
        self._property_frame._first_nybblebit_combobox.combo_box.currentIndexChanged.connect(self._first_nybblebit_changed)
        nybble_frame.grid_layout.addWidget(self._property_frame._first_nybblebit_combobox, 0, 2)

        label = QLabel('-')
        label.setProperty('brighttitle', True)
        nybble_frame.grid_layout.addWidget(label, 0, 3)

        self._property_frame._last_nybble_combobox = QNamedComboBox(None, self._lang.get_data('QNamedComboBox.lastNybble'))
        self._property_frame._last_nybble_combobox.combo_box.addItems(['None'] + [str(i) for i in range(1, 17)])
        if self._data.nybble.end is not None: self._property_frame._last_nybble_combobox.combo_box.setCurrentIndex(self._data.nybble.end.n if self._data.nybble.end.n is not None else 0)
        self._property_frame._last_nybble_combobox.combo_box.currentIndexChanged.connect(self._last_nybble_changed)
        nybble_frame.grid_layout.addWidget(self._property_frame._last_nybble_combobox, 0, 4)

        label = QLabel('.')
        label.setProperty('brighttitle', True)
        nybble_frame.grid_layout.addWidget(label, 0, 5)

        self._property_frame._last_nybblebit_combobox = QNamedComboBox(None, self._lang.get_data('QNamedComboBox.lastNybbleBit'))
        self._property_frame._last_nybblebit_combobox.combo_box.addItems(['None'] + [str(i) for i in range(1, 5)])
        if self._data.nybble.end is not None: self._property_frame._last_nybblebit_combobox.combo_box.setCurrentIndex((self._data.nybble.end.b + 1) if self._data.nybble.end.b is not None else 0)
        self._property_frame._last_nybblebit_combobox.combo_box.currentIndexChanged.connect(self._last_nybblebit_changed)
        nybble_frame.grid_layout.addWidget(self._property_frame._last_nybblebit_combobox, 0, 6)


        required_nybbleval_frame = QGridWidget()
        required_nybbleval_frame.grid_layout.setContentsMargins(0, 0, 0, 0)
        required_nybbleval_frame.grid_layout.setSpacing(8)
        self._property_frame.grid_layout.addWidget(required_nybbleval_frame, self._property_frame.grid_layout.rowCount(), 0)

        # todo: add required nybbleval frame content


        self._property_last_frame = QGridWidget()
        self._property_last_frame.grid_layout.setContentsMargins(0, 0, 0, 0)
        self._property_last_frame.grid_layout.setSpacing(8)
        self._property_frame.grid_layout.addWidget(self._property_last_frame, self._property_frame.grid_layout.rowCount(), 0)


        comment_frame = QGridWidget()
        comment_frame.grid_layout.setContentsMargins(0, 0, 0, 0)
        comment_frame.grid_layout.setSpacing(8)
        self._property_frame.grid_layout.addWidget(comment_frame, self._property_frame.grid_layout.rowCount(), 0)

        self._property_frame._comment_textedit = QNamedTextEdit(None, '', self._lang.get_data('QNamedTextEdit.comment'))
        self._property_frame._comment_textedit.setText(self._data.comment)
        self._property_frame._comment_textedit.text_edit.textChanged.connect(self._comment_changed)
        comment_frame.grid_layout.addWidget(self._property_frame._comment_textedit, 0, 0)

        self._property_frame._comment2_textedit = QNamedTextEdit(None, '', self._lang.get_data('QNamedTextEdit.comment2'))
        self._property_frame._comment2_textedit.setText(self._data.comment2)
        self._property_frame._comment2_textedit.text_edit.textChanged.connect(self._comment2_changed)
        comment_frame.grid_layout.addWidget(self._property_frame._comment2_textedit, 0, 1)


        advanced_frame = QGridWidget()
        advanced_frame.grid_layout.setContentsMargins(0, 0, 0, 0)
        advanced_frame.grid_layout.setSpacing(8)
        self._property_frame.grid_layout.addWidget(advanced_frame, self._property_frame.grid_layout.rowCount(), 0)


        self._property_frame.advanced_togglebutton = QNamedToggleButton(None, self._lang.get_data('QNamedToggleButton.advanced'))
        self._property_frame.advanced_togglebutton.setChecked(self._data.advanced)
        self._property_frame.advanced_togglebutton.toggle_button.stateChanged.connect(self._advanced_changed)
        advanced_frame.grid_layout.addWidget(self._property_frame.advanced_togglebutton, 0, 0, Qt.AlignmentFlag.AlignLeft)

        self._property_frame.advancedcomment_textedit = QNamedTextEdit(None, '', self._lang.get_data('QNamedTextEdit.advancedcomment'))
        if not data.advanced: self._property_frame.advancedcomment_textedit.hide()
        self._property_frame.advancedcomment_textedit.setText(self._data.advancedcomment)
        self._property_frame.advancedcomment_textedit.text_edit.textChanged.connect(self._advancedcomment_changed)
        advanced_frame.grid_layout.addWidget(self._property_frame.advancedcomment_textedit, 0, 1)


    @property
    def data(self) -> BaseItem:
        return self._data


    def _update_title_text(self) -> None:
        self._type_label.setText(self.type)

    def _update_nybbles_settings_text(self) -> None:
        l = self._data.nybble.export().split('-')
        if len(l) == 1: l = l[0]
        else: l = self._lang.get_data('QLabel.nybbleRange').replace('%s', l[0], 1).replace('%s', l[1], 1)

        self._nybbles_label.setText(self._lang.get_data('QLabel.nybbles').replace('%s', l))
        self._settings_label.setText(self._lang.get_data('QLabel.settings').replace('%s', self._data.nybble.convert2hex_formatted()))

    def _delete(self) -> None:
        self.deleted.emit(self)
        # self.deleteLater()

    def mousePressEvent(self, event: QMouseEvent) -> None:
        self.set_checked(not self.property('checked'))
        self.selected.emit(self, self._property_frame if self.property('checked') else None)
        return super().mousePressEvent(event)

    def is_checked(self) -> bool:
        return self.property('checked')

    def set_checked(self, checked: bool) -> None:
        self.setProperty('checked', checked)
        self.style().unpolish(self)
        self.style().polish(self)


    def _comment_changed(self) -> None:
        self._data.comment = self._property_frame._comment_textedit.text()
        self.data_changed.emit()

    def _comment2_changed(self) -> None:
        self._data.comment2 = self._property_frame._comment2_textedit.text()
        self.data_changed.emit()

    def _advanced_changed(self, advanced: bool) -> None:
        self._data.advanced = advanced
        self._property_frame.advancedcomment_textedit.setVisible(advanced)
        self.data_changed.emit()

    def _advancedcomment_changed(self) -> None:
        self._data.advancedcomment = self._property_frame.advancedcomment_textedit.text()
        self.data_changed.emit()

    def _fix_nybbles(self) -> None:
        fn = self._property_frame._first_nybble_combobox.combo_box.currentIndex()
        fnb = self._property_frame._first_nybblebit_combobox.combo_box.currentIndex() - 1
        ln = self._property_frame._last_nybble_combobox.combo_box.currentIndex() - 1
        lnb = self._property_frame._last_nybblebit_combobox.combo_box.currentIndex() - 1

        if ln == -1: lnb = -1

        if ln >= 0:
            if fn > ln:
                fn, ln = ln, fn

            if (fn == ln) and (fnb > lnb):
                fnb, lnb = lnb, fnb

        self._property_frame._first_nybble_combobox.combo_box.setCurrentIndex(fn)
        self._property_frame._first_nybblebit_combobox.combo_box.setCurrentIndex(fnb + 1)
        self._property_frame._last_nybble_combobox.combo_box.setCurrentIndex(ln + 1)
        self._property_frame._last_nybblebit_combobox.combo_box.setCurrentIndex(lnb + 1)

        self._data.nybble.start.n = fn + 1
        self._data.nybble.start.b = fnb if fnb >= 0 else None

        if ln >= 0:
            s = f'{ln + 1}'
            if lnb >= 0: s += f'.{lnb + 1}'
            self._data.nybble.end = Nybble(s)

        else:
            self._data.nybble.end = None

        self._update_nybbles_settings_text()
        self.data_changed.emit()

    def _first_nybble_changed(self, index: int) -> None:
        self._fix_nybbles()

    def _first_nybblebit_changed(self, index: int) -> None:
        self._fix_nybbles()

    def _last_nybble_changed(self, index: int) -> None:
        self._fix_nybbles()

    def _last_nybblebit_changed(self, index: int) -> None:
        self._fix_nybbles()



    def export(self) -> BaseItem:
        return self._data
#----------------------------------------------------------------------
