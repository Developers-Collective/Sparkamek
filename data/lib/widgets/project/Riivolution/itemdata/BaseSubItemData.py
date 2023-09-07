#----------------------------------------------------------------------

    # Libraries
from PySide6.QtGui import QMouseEvent
from PySide6.QtWidgets import QLabel, QPushButton
from PySide6.QtCore import Qt, Signal
from data.lib.qtUtils import QDragListItem, QGridWidget, QBaseApplication, QSaveData, QNamedTextEdit, QNamedToggleButton, QssSelector
from ..items.IBaseItem import IBaseItem
#----------------------------------------------------------------------

    # Class
class BaseSubItemData(QDragListItem):
    type: str = 'IBaseItem'
    child_cls: IBaseItem = IBaseItem

    _normal_color = '#FFFFFF'
    _checked_color = '#FFFFFF'

    edited = Signal(QDragListItem, QGridWidget or None)
    deleted = Signal(QDragListItem)
    data_changed = Signal()

    _edit_icon = None
    _delete_icon = None

    def init(app: QBaseApplication) -> None:
        BaseSubItemData._edit_icon = app.get_icon('pushbutton/editBig.png', True, QSaveData.IconMode.Local)
        BaseSubItemData._delete_icon = app.get_icon('pushbutton/deleteBig.png', True, QSaveData.IconMode.Local)

        BaseSubItemData._normal_color = app.qss.search(
            QssSelector(widget = 'QWidget', attributes = {'BaseItemData': True}),
            QssSelector(widget = 'QLabel')
        )

    def __init__(self, data: IBaseItem, path: str) -> None:
        super().__init__()

        self.setProperty('color', 'main')
        self.setProperty('side', 'all')
        self.setProperty('bottom-border-only', True)
        self.setProperty('border-radius', 8)

        self._data = data
        self._path = path

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

        self._edit_button = QPushButton()
        self._edit_button.clicked.connect(self._edit)
        self._edit_button.setIcon(self._edit_icon)
        self._edit_button.setProperty('color', 'main')
        self._edit_button.setCursor(Qt.CursorShape.PointingHandCursor)
        topright_frame.grid_layout.addWidget(self._edit_button, 0, 0)

        self._delete_button = QPushButton()
        self._delete_button.clicked.connect(self._delete)
        self._delete_button.setIcon(self._delete_icon)
        self._delete_button.setProperty('color', 'main')
        self._delete_button.setCursor(Qt.CursorShape.PointingHandCursor)
        topright_frame.grid_layout.addWidget(self._delete_button, 0, 1)

        topright_frame.grid_layout.setColumnStretch(2, 1)


        self._property_frame = QGridWidget()
        self._property_frame.type = self.type
        self._property_frame.grid_layout.setContentsMargins(0, 0, 0, 0)
        self._property_frame.grid_layout.setSpacing(20)


    @property
    def data(self) -> IBaseItem:
        return self._data


    def _update_title_text(self) -> None:
        self._type_label.setText(self.type)


    def _delete(self) -> None:
        self.deleted.emit(self)

    def _edit(self) -> None:
        self.edited.emit(self, self._property_frame)
#----------------------------------------------------------------------
