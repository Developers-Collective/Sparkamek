#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QPushButton, QLabel, QMenu
from PySide6.QtCore import Qt, Signal, QPoint
from PySide6.QtGui import QAction
from data.lib.qtUtils import QBaseApplication, QGridWidget, QSaveData, QDragList, QNamedTextEdit, QNamedLineEdit, QNamedSpinBox, QNamedToggleButton
from data.lib.widgets.ProjectKeys import ProjectKeys
from .items import ID, Region
from .itemdata import RegionData
#----------------------------------------------------------------------

    # Class
class IDWidget(QGridWidget):
    type: ProjectKeys = ProjectKeys.ReggieNext

    data_changed = Signal()
    property_entry_selected = Signal(QGridWidget or None)

    _app: QBaseApplication = None

    _add_entry_icon = None

    _lang = {}

    def init(app: QBaseApplication) -> None:
        IDWidget._app = app

        IDWidget._lang = app.get_lang_data('QMainWindow.QSlidingStackedWidget.mainMenu.projects.RiivolutionWidget.WiiDiscWidget.IDWidget')
        IDWidget._add_entry_icon = app.get_icon('pushbutton/add.png', True, QSaveData.IconMode.Local)

        RegionData.init(app)

    def __init__(self, path: str) -> None:
        super().__init__()

        self._path = path

        self._disable_send = True

        self.grid_layout.setContentsMargins(0, 0, 0, 0)
        self.grid_layout.setSpacing(8)

        label = QLabel(self._lang.get_data('QLabel.ID'))
        label.setProperty('h', 2)
        label.setProperty('small', True)
        self.grid_layout.addWidget(label, 0, 0)

        self._region_draglist = QDragList(None, Qt.Orientation.Vertical)
        self._region_draglist.moved.connect(self._region_entry_moved)
        self.grid_layout.addWidget(self._region_draglist, 1, 0)

        self._add_region_entry_button = QPushButton(self._lang.get_data('QPushButton.addEntry'))
        self._add_region_entry_button.setIcon(self._add_entry_icon)
        self._add_region_entry_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self._add_region_entry_button.setProperty('color', 'main')
        self._add_region_entry_button.clicked.connect(self._add_region_entry)
        self.grid_layout.addWidget(self._add_region_entry_button, 2, 0)
        self._add_region_entry_button.setEnabled(False)

        self._id: ID = None


    @property
    def id(self) -> ID:
        return self._id
    
    @id.setter
    def id(self, id: ID) -> None:
        self._id = id

        self._disable_send = True

        self._region_draglist.clear()

        self._add_region_entry_button.setEnabled(self._id is not None)

        if self._id:
            for region in self._id.region_children:
                rd = RegionData(region, self._path)
                rd.data_changed.connect(self._send_data)
                rd.selected.connect(self._entry_selected)
                rd.deleted.connect(self._delete_region_entry)
                self._region_draglist.add_item(rd)

        self._disable_send = False


    def _region_entry_moved(self, old_index: int, new_index: int) -> None:
        self._id.region_children.insert(new_index, self._id.region_children.pop(old_index))
        self._send_data()

    def _add_region_entry(self) -> None:
        r = Region.create()
        self._id.region_children.append(r)

        rd = RegionData(r, self._path)
        rd.data_changed.connect(self._send_data)
        rd.deleted.connect(self._delete_region_entry)
        rd.selected.connect(self._entry_selected)
        self._region_draglist.add_item(rd)

        self._send_data()

    def _delete_region_entry(self, item: RegionData) -> None:
        if self._id is None: return

        self._id.region_children.remove(item.data)
        item.deleteLater()
        self._send_data()

    def _entry_selected(self, sender: RegionData, widget: QGridWidget | None) -> None:
        checked = sender.is_checked()

        for item in self._region_draglist.items:
            item.set_checked(False)

        sender.set_checked(checked)
        self.property_entry_selected.emit(widget)


    def _send_data(self, *args) -> None:
        self.data_changed.emit()
#----------------------------------------------------------------------
