#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QPushButton, QLabel
from PySide6.QtCore import Qt, Signal
from data.lib.qtUtils import QBaseApplication, QGridWidget, QSaveData, QDragList, QNamedLineEdit, QNamedSpinBox
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
        self.grid_layout.setSpacing(16)


        frame = QGridWidget()
        frame.grid_layout.setContentsMargins(0, 0, 0, 0)
        frame.grid_layout.setSpacing(8)
        self.grid_layout.addWidget(frame, 0, 0)

        label = QLabel(self._lang.get_data('QLabel.gameProperties'))
        label.setProperty('h', 2)
        label.setProperty('small', True)
        frame.grid_layout.addWidget(label, 0, 0, 1, 2)

        self._game_lineedit = QNamedLineEdit(None, '', self._lang.get_data('QNamedLineEdit.game'))
        self._game_lineedit.line_edit.setMaxLength(3)
        self._game_lineedit.setToolTip(self._lang.get_data('QToolTip.game'))
        self._game_lineedit.line_edit.textChanged.connect(self._game_changed)
        frame.grid_layout.addWidget(self._game_lineedit, 1, 0)

        self._developer_lineedit = QNamedLineEdit(None, '', self._lang.get_data('QNamedLineEdit.developer'))
        self._developer_lineedit.line_edit.setMaxLength(2)
        self._developer_lineedit.setToolTip(self._lang.get_data('QToolTip.developer'))
        self._developer_lineedit.line_edit.textChanged.connect(self._developer_changed)
        frame.grid_layout.addWidget(self._developer_lineedit, 1, 1)

        self._disc_spinbox = QNamedSpinBox(None, self._lang.get_data('QNamedSpinBox.disc'))
        self._disc_spinbox.set_range(-1, 99)
        self._disc_spinbox.setToolTip(self._lang.get_data('QToolTip.disc'))
        self._disc_spinbox.value_changed.connect(self._disc_changed)
        frame.grid_layout.addWidget(self._disc_spinbox, 2, 0)

        self._version_spinbox = QNamedSpinBox(None, self._lang.get_data('QNamedSpinBox.version'))
        self._version_spinbox.set_range(-1, 99)
        self._version_spinbox.setToolTip(self._lang.get_data('QToolTip.version'))
        self._version_spinbox.value_changed.connect(self._version_changed)
        frame.grid_layout.addWidget(self._version_spinbox, 2, 1)


        frame = QGridWidget()
        frame.grid_layout.setContentsMargins(0, 0, 0, 0)
        frame.grid_layout.setSpacing(8)
        self.grid_layout.addWidget(frame, 1, 0)

        label = QLabel(self._lang.get_data('QLabel.regions'))
        label.setProperty('h', 2)
        label.setProperty('small', True)
        frame.grid_layout.addWidget(label, 2, 0)

        self._region_draglist = QDragList(None, Qt.Orientation.Vertical)
        self._region_draglist.moved.connect(self._region_entry_moved)
        frame.grid_layout.addWidget(self._region_draglist, 3, 0)

        self._add_region_entry_button = QPushButton(self._lang.get_data('QPushButton.addEntry'))
        self._add_region_entry_button.setIcon(self._add_entry_icon)
        self._add_region_entry_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self._add_region_entry_button.setProperty('color', 'main')
        self._add_region_entry_button.clicked.connect(self._add_region_entry)
        frame.grid_layout.addWidget(self._add_region_entry_button, 4, 0)
        self._add_region_entry_button.setEnabled(False)


        self._id: ID = None


    @property
    def id(self) -> ID:
        return self._id

    @id.setter
    def id(self, id: ID) -> None:
        self._id = id

        self._disable_send = True

        self._game_lineedit.line_edit.setText('')
        self._developer_lineedit.line_edit.setText('')
        self._disc_spinbox.set_value(-1)
        self._version_spinbox.set_value(-1)

        self._region_draglist.clear()

        self._add_region_entry_button.setEnabled(self._id is not None)

        if self._id:
            self._game_lineedit.line_edit.setText(self._id.game)
            self._developer_lineedit.line_edit.setText(self._id.developer)
            self._disc_spinbox.set_value(self._id.disc)
            self._version_spinbox.set_value(self._id.version)

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

        self.property_entry_selected.emit(None)

        for item in self._region_draglist.items:
            item.set_checked(False)

        self._send_data()

    def _entry_selected(self, sender: RegionData, widget: QGridWidget | None) -> None:
        checked = sender.is_checked()

        self.deselect_all()

        sender.set_checked(checked)
        self.property_entry_selected.emit(widget)

    def deselect_all(self) -> None:
        self._disable_send = True

        for item in self._region_draglist.items:
            item.set_checked(False)

        self._disable_send = False


    def _send_data(self, *args) -> None:
        self.data_changed.emit()


    def _game_changed(self, text: str) -> None:
        if self._disable_send: return

        self._id.game = text
        self._send_data()

    def _developer_changed(self, text: str) -> None:
        if self._disable_send: return

        self._id.developer = text
        self._send_data()

    def _disc_changed(self, value: int) -> None:
        if self._disable_send: return

        self._id.disc = value
        self._send_data()

    def _version_changed(self, value: int) -> None:
        if self._disable_send: return

        self._id.version = value
        self._send_data()
#----------------------------------------------------------------------
