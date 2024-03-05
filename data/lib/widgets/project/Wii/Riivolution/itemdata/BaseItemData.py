#----------------------------------------------------------------------

    # Libraries
from PySide6.QtGui import QMouseEvent
from PySide6.QtWidgets import QLabel, QPushButton
from PySide6.QtCore import Qt, Signal
from data.lib.QtUtils import QDragListItem, QGridWidget, QBaseApplication, QSaveData, QNamedTextEdit, QNamedToggleButton, QssSelector
from ..items.IBaseItem import IBaseItem
#----------------------------------------------------------------------

    # Class
class BaseItemData(QDragListItem):
    type: str = 'IBaseItem'
    child_cls: IBaseItem = IBaseItem

    _normal_color = '#FFFFFF'
    _checked_color = '#FFFFFF'

    deleted = Signal(QDragListItem)
    selected = Signal(QDragListItem, QGridWidget or None)
    data_changed = Signal()

    _delete_icon = None

    def init(app: QBaseApplication) -> None:
        BaseItemData._delete_icon = app.get_icon('pushbutton/deleteBig.png', True, QSaveData.IconMode.Local)

        BaseItemData._normal_color = app.qss.search(
            QssSelector(widget = 'QWidget', attributes = {'BaseItemData': True}),
            QssSelector(widget = 'QLabel')
        )
        BaseItemData._checked_color = app.qss.search(
            QssSelector(widget = 'QWidget', attributes = {'color': app.window.property('color')}),
            QssSelector(widget = 'QWidget', attributes = {'BaseItemData': True, 'color': 'main'}),
            QssSelector(widget = 'QLabel', attributes = {'checked': True})
        )['color']

    def __init__(self, data: IBaseItem, path: str) -> None:
        super().__init__()

        self.setProperty('color', 'main')
        self.setProperty('side', 'all')
        self.setProperty('checkable', True)
        self.setProperty('checked', False)
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

        delete_button = QPushButton()
        delete_button.clicked.connect(self._delete)
        delete_button.setIcon(self._delete_icon)
        delete_button.setProperty('color', 'main')
        delete_button.setCursor(Qt.CursorShape.PointingHandCursor)
        topright_frame.grid_layout.addWidget(delete_button, 0, 0, Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignRight)


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

    def mousePressEvent(self, event: QMouseEvent) -> None:
        self.set_checked(not self.property('checked'))
        self.selected.emit(self, self._property_frame if self.property('checked') else None)
        return super().mousePressEvent(event)

    def is_checked(self) -> bool:
        return self.property('checked')

    def set_checked(self, checked: bool) -> None:
        self.setProperty('checked', checked)
        self._type_label.setStyleSheet(f'color: {self._checked_color if checked else self._normal_color}')
        self.style().unpolish(self)
        self.style().polish(self)
#----------------------------------------------------------------------
