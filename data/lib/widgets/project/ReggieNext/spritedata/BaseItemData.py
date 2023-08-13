#----------------------------------------------------------------------

    # Libraries
from PySide6.QtGui import QMouseEvent
from PySide6.QtWidgets import QLabel, QPushButton
from PySide6.QtCore import Qt, Signal
from data.lib.qtUtils import QDragListItem, QGridWidget, QBaseApplication, QSaveData
from data.lib.storage.xml import XMLNode
from ..sprites.BaseItem import BaseItem
#----------------------------------------------------------------------

    # Class
class BaseItemData(QDragListItem):
    type: str = 'BaseItem'

    delete = Signal()
    selected = Signal(QGridWidget)

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

        self._data = data.copy()

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
        self._nybbles_label.setProperty('brighttitle', True)
        bottom_frame.grid_layout.addWidget(self._nybbles_label, 0, 0, Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignLeft)

        self._settings_label = QLabel()
        self._settings_label.setProperty('brighttitle', True)
        bottom_frame.grid_layout.addWidget(self._settings_label, 0, 1, Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignRight)

        self._update_nybbles_settings_text()

    def _update_title_text(self) -> None:
        self._type_label.setText(self.type)

    def _update_nybbles_settings_text(self) -> None:
        l = self._data.nybble.export().split('-')
        if len(l) == 1: l = l[0]
        else: l = self._lang.get_data('nybbleRange').replace('%s', l[0], 1).replace('%s', l[1], 1)

        self._nybbles_label.setText(self._lang.get_data('nybbles').replace('%s', l))
        self._settings_label.setText(self._lang.get_data('settings').replace('%s', self._data.nybble.convert2hex_formatted()))

    def _delete(self) -> None:
        self.delete.emit()
        self.deleteLater()

    def mousePressEvent(self, event: QMouseEvent) -> None:
        self.set_checked(True)
        self.selected.emit(QGridWidget())
        return super().mousePressEvent(event)

    def set_checked(self, checked: bool) -> None:
        self.setProperty('checked', checked)
        self.style().unpolish(self)
        self.style().polish(self)

    # def export(self) -> BaseItem:
    #     return BaseItem(XMLNode('template', {}, [], None))
#----------------------------------------------------------------------
