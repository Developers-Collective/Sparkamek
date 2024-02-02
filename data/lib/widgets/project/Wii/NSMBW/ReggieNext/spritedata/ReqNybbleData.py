#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QPushButton, QLabel
from PySide6.QtCore import Qt, Signal
from PySide6.QtCore import Signal
from data.lib.qtUtils import QGridWidget, QBaseApplication, QDragList, QSaveData, QLangData
from ..sprites.ReqNybble import ReqNybble
from ..sprites.NybbleRange import NybbleRange
from .ReqNybbleDataItem import ReqNybbleDataItem
#----------------------------------------------------------------------

    # Class
class ReqNybbleData(QGridWidget):
    data_changed = Signal()

    _add_icon = None

    _lang: QLangData = QLangData.NoTranslation()

    def init(app: QBaseApplication) -> None:
        ReqNybbleData._lang = app.get_lang_data('QMainWindow.QSlidingStackedWidget.mainMenu.projects.ReggieNextWidget.SpriteWidget.ReqNybbleData')
        ReqNybbleData._add_icon = app.get_icon('pushbutton/add.png', True, QSaveData.IconMode.Local)

        ReqNybbleDataItem.init(app)

    def __init__(self, data: list[ReqNybble]) -> None:
        super().__init__()

        self._data = data


        self.grid_layout.setContentsMargins(0, 0, 0, 0)
        self.grid_layout.setSpacing(8)


        label = QLabel(self._lang.get('QLabel.title'))
        label.setProperty('h', 2)
        label.setProperty('small', True)
        self.grid_layout.addWidget(label, 0, 0)


        self._list = QDragList()
        self.grid_layout.addWidget(self._list, 1, 0)

        for data in self._data:
            item = ReqNybbleDataItem(data)
            item.data_changed.connect(self.data_changed.emit)
            item.deleted.connect(self._remove)
            self._list.add_item(item)


        self._add_button = QPushButton()
        self._add_button.setProperty('color', 'main')
        self._add_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self._add_button.setIcon(ReqNybbleData._add_icon)
        self._add_button.clicked.connect(self._add)
        self.grid_layout.addWidget(self._add_button, 2, 0)



    @property
    def data(self) -> list[ReqNybble]:
        return self._data
    

    def _add(self) -> None:
        data = ReqNybble(NybbleRange('1'), [0])
        self._data.append(data)
        item = ReqNybbleDataItem(data)
        item.data_changed.connect(self.data_changed.emit)
        item.deleted.connect(self._remove)
        self._list.add_item(item)
        self.data_changed.emit()

    def _remove(self, item: ReqNybbleDataItem) -> None:
        self._data.remove(item.data)
        self._list.remove_item(item)
        item.deleteLater()
        self.data_changed.emit()

    def _moved(self, from_: int, to_: int) -> None:
        self._data.insert(to_, self._data.pop(from_))
        self.data_changed.emit()
#----------------------------------------------------------------------
