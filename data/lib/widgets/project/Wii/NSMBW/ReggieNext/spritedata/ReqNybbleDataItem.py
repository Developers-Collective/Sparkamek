#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QPushButton
from PySide6.QtCore import Qt, Signal
from data.lib.qtUtils import QDragListItem, QGridWidget, QBaseApplication, QSaveData, QNamedSpinBox, QLangData
from ..sprites.ReqNybble import ReqNybble
from .NybbleData import NybbleData
#----------------------------------------------------------------------

    # Class
class ReqNybbleDataItem(QDragListItem):
    deleted = Signal(QDragListItem)
    data_changed = Signal()

    _lang: QLangData = QLangData.NoTranslation()

    _delete_icon = None

    def init(app: QBaseApplication) -> None:
        ReqNybbleDataItem._lang = app.get_lang_data('QMainWindow.QSlidingStackedWidget.mainMenu.projects.projectWidget.Wii.NSMBW.ReggieNextWidget.SpriteWidget.ReqNybbleData.ReqNybbleDataItem')
        ReqNybbleDataItem._delete_icon = app.get_icon('pushbutton/deleteBig.png', True, QSaveData.IconMode.Local)

    def __init__(self, data: ReqNybble) -> None:
        super().__init__()

        self.setProperty('color', 'main')
        self.setProperty('side', 'all')
        self.setProperty('border-radius', 8)

        self._data = data

        self.grid_layout.setContentsMargins(10, 10, 10, 10)
        self.grid_layout.setSpacing(8)


        left_frame = QGridWidget()
        left_frame.grid_layout.setContentsMargins(0, 0, 0, 0)
        left_frame.grid_layout.setSpacing(8)
        self.grid_layout.addWidget(left_frame, 0, 0, Qt.AlignmentFlag.AlignLeft)

        self._nybble_data = NybbleData(data.nybbles)
        self._nybble_data.data_changed.connect(self.data_changed.emit)
        left_frame.grid_layout.addWidget(self._nybble_data, 0, 0)


        right_frame = QGridWidget()
        right_frame.grid_layout.setContentsMargins(0, 0, 0, 0)
        right_frame.grid_layout.setSpacing(8)
        self.grid_layout.addWidget(right_frame, 0, 1, Qt.AlignmentFlag.AlignRight)
        right_frame.grid_layout.setColumnStretch(2, 1)

        self._from_value_spinbox = QNamedSpinBox(None, self._lang.get('QNamedSpinBox.fromValue'))
        self._from_value_spinbox.setRange(0, 2147483647) # 2^32 - 1 but QSpinBox are s32 (2^31 - 1) -> Tbf nobody will require a value of 2^31 lmao
        self._from_value_spinbox.setValue(data.values.start)
        self._from_value_spinbox.spin_box.valueChanged.connect(self._from_value_changed)
        right_frame.grid_layout.addWidget(self._from_value_spinbox, 0, 1)

        self._to_value_spinbox = QNamedSpinBox(None, self._lang.get('QNamedSpinBox.toValue'))
        self._to_value_spinbox.setRange(0, 2147483647) # 2^32 - 1 but QSpinBox are s32 (2^31 - 1) -> Tbf nobody will require a value of 2^31 lmao
        self._to_value_spinbox.setValue(data.values.end)
        self._to_value_spinbox.spin_box.valueChanged.connect(self._to_value_changed)
        right_frame.grid_layout.addWidget(self._to_value_spinbox, 0, 2)


        delete_button = QPushButton()
        delete_button.setProperty('color', 'main')
        delete_button.setCursor(Qt.CursorShape.PointingHandCursor)
        delete_button.setIcon(self._delete_icon)
        delete_button.clicked.connect(self._delete)
        self.grid_layout.addWidget(delete_button, 0, 2, Qt.AlignmentFlag.AlignRight)


    @property
    def data(self) -> ReqNybble:
        return self._data


    def _delete(self) -> None:
        self.deleted.emit(self)


    def _fix_values(self) -> None:
        if self.data.values.start > self._data.values.end:
            self._data.values.start, self._data.values.end = self._data.values.end, self._data.values.start

        self._from_value_spinbox.setValue(self._data.values.start)
        self._to_value_spinbox.setValue(self._data.values.end)

        self.data_changed.emit()

    def _from_value_changed(self, value: int) -> None:
        self._data.values.start = value
        self._fix_values()

    def _to_value_changed(self, value: int) -> None:
        self._data.values.end = value
        self._fix_values()
#----------------------------------------------------------------------
