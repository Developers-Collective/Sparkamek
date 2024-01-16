#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QPushButton
from PySide6.QtCore import Qt, Signal
from data.lib.qtUtils import QDragListItem, QGridWidget, QBaseApplication, QSaveData, QNamedSpinBox, QLangData
from ..sprites.Required import Required
from ..sprites.Suggested import Suggested
#----------------------------------------------------------------------

    # Class
class DependencyDataItem(QDragListItem):
    deleted = Signal(QDragListItem)
    data_changed = Signal()

    _lang: QLangData = QLangData.NoTranslation()

    _delete_icon = None

    def init(app: QBaseApplication) -> None:
        DependencyDataItem._lang = app.get_lang_data('QMainWindow.QSlidingStackedWidget.mainMenu.projects.ReggieNextWidget.SpriteWidget.DependencyDataItem')
        DependencyDataItem._delete_icon = app.get_icon('pushbutton/deleteBig.png', True, QSaveData.IconMode.Local)

    def __init__(self, data: Required | Suggested) -> None:
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
        left_frame.grid_layout.setColumnStretch(2, 1)

        self._id_spinbox = QNamedSpinBox(None, self._lang.get('QNamedSpinBox.spriteID'))
        self._id_spinbox.spin_box.valueChanged.connect(self._id_changed)
        self._id_spinbox.setRange(0, 2147483647) # profileID is u32 (2^32 - 1) but QSpinBox are s32 (2^31 - 1) -> Tbf nobody will have 2^31 sprites lmao
        self._id_spinbox.spin_box.setValue(data.sprite)
        left_frame.grid_layout.addWidget(self._id_spinbox, 0, 0)


        delete_button = QPushButton()
        delete_button.setProperty('color', 'main')
        delete_button.setCursor(Qt.CursorShape.PointingHandCursor)
        delete_button.setIcon(self._delete_icon)
        delete_button.clicked.connect(self._delete)
        self.grid_layout.addWidget(delete_button, 0, 1, Qt.AlignmentFlag.AlignRight)


    @property
    def data(self) -> Required | Suggested:
        return self._data


    def _delete(self) -> None:
        self.deleted.emit(self)


    def _id_changed(self, value: int) -> None:
        self._data.sprite = value
        self.data_changed.emit()
#----------------------------------------------------------------------
