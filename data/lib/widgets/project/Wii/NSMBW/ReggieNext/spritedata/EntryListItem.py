#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QPushButton
from PySide6.QtCore import Qt, Signal
from data.lib.QtUtils import QBaseApplication, QSaveData, QNamedLineEdit, QDragListItem, QNamedSpinBox, QLangData
from ..sprites.Entry import Entry
#----------------------------------------------------------------------

    # Class
class EntryListItem(QDragListItem):
    data_changed = Signal()
    deleted = Signal(QDragListItem)

    _delete_icon = None
    _lang: QLangData = QLangData.NoTranslation()

    def init(app: QBaseApplication) -> None:
        EntryListItem._lang = app.get_lang_data('QMainWindow.QSlidingStackedWidget.mainMenu.projects.projectWidget.Wii.NSMBW.ReggieNextWidget.SpriteWidget.ListData.EntryListItem')
        EntryListItem._delete_icon = app.get_icon('pushbutton/deleteBig.png', True, QSaveData.IconMode.Local)

    def __init__(self, data: Entry) -> None:
        super().__init__()

        self._data = data

        self.setProperty('color', 'main')
        self.setProperty('side', 'all')
        self.setProperty('border-radius', 8)

        self.layout_.setContentsMargins(10, 10, 10, 10)
        self.layout_.setSpacing(8)


        self._value_spinbox = QNamedSpinBox(None, self._lang.get('QNamedSpinBox.value'))
        self._value_spinbox.setRange(0, 2147483647) # 16^16 - 1 but QSpinBox are s32 (2^31 - 1) -> Tbf nobody will have 16^16 entries lmao
        self._value_spinbox.setValue(self._data.value)
        self._value_spinbox.spin_box.valueChanged.connect(self._value_changed)
        self.layout_.addWidget(self._value_spinbox, 0, 0)

        self._item_lineedit = QNamedLineEdit(None, '', self._lang.get('QNamedLineEdit.item'))
        self._item_lineedit.setText(str(self._data.item))
        self._item_lineedit.line_edit.textChanged.connect(self._item_changed)
        self.layout_.addWidget(self._item_lineedit, 0, 1)

        self._delete_button = QPushButton()
        self._delete_button.setProperty('color', 'main')
        self._delete_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self._delete_button.setIcon(self._delete_icon)
        self._delete_button.clicked.connect(self._delete_clicked)
        self.layout_.addWidget(self._delete_button, 0, 2)


    @property
    def data(self) -> Entry:
        return self._data


    def _value_changed(self) -> None:
        self._data.value = self._value_spinbox.value()
        self.data_changed.emit()

    def _item_changed(self) -> None:
        self._data.item = self._item_lineedit.text()
        self.data_changed.emit()

    def _delete_clicked(self) -> None:
        self.deleted.emit(self)
#----------------------------------------------------------------------
