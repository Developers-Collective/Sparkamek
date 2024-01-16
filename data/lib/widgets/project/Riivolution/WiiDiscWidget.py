#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QLabel, QPushButton
from PySide6.QtCore import Signal, Qt
from data.lib.qtUtils import QBaseApplication, QGridWidget, QSaveData, QDragList, QNamedLineEdit, QNamedSpinBox
from data.lib.widgets.ProjectKeys import ProjectKeys
from .items import WiiDisc, Patch
from .IDWidget import IDWidget
from .OptionsWidget import OptionsWidget
from .itemdata.BaseItemData import BaseItemData
from .itemdata.PatchData import PatchData
from .ItemDataPropertyDockWidget import ItemDataPropertyDockWidget
#----------------------------------------------------------------------

    # Class
class WiiDiscWidget(QGridWidget):
    type: ProjectKeys = ProjectKeys.ReggieNext

    _app: QBaseApplication = None

    property_entry_selected = Signal(QGridWidget or None)

    _add_entry_icon = None
    _add_item_entry_icon = None

    _lang = {}

    def init(app: QBaseApplication) -> None:
        WiiDiscWidget._app = app

        WiiDiscWidget._lang = app.get_lang_data('QMainWindow.QSlidingStackedWidget.mainMenu.projects.RiivolutionWidget.WiiDiscWidget')
        WiiDiscWidget._add_entry_icon = app.get_icon('pushbutton/add.png', True, QSaveData.IconMode.Local)
        WiiDiscWidget._add_item_entry_icon = app.get_icon('popup/addItem.png', True, QSaveData.IconMode.Local)

        ItemDataPropertyDockWidget.init(app)

        BaseItemData.init(app)
        IDWidget.init(app)
        OptionsWidget.init(app)
        PatchData.init(app)

    def __init__(self, path: str) -> None:
        super().__init__()

        self._path = path

        self._disable_send = True

        self.grid_layout.setContentsMargins(0, 0, 0, 0)
        self.grid_layout.setSpacing(30)


        self._top_info_widget = QGridWidget()
        self._top_info_widget.grid_layout.setContentsMargins(0, 0, 0, 0)
        self._top_info_widget.grid_layout.setSpacing(8)
        self.grid_layout.addWidget(self._top_info_widget, 0, 0)

        label = QLabel(self._lang.get('QLabel.generalInfo'))
        label.setProperty('h', 2)
        label.setProperty('small', True)
        self._top_info_widget.grid_layout.addWidget(label, 0, 0, 1, 2)

        self._root_lineedit = QNamedLineEdit(None, '', self._lang.get('QNamedLineEdit.root'))
        self._root_lineedit.setToolTip(self._lang.get('QToolTip.root'))
        self._root_lineedit.line_edit.textChanged.connect(self._root_changed)
        self._top_info_widget.grid_layout.addWidget(self._root_lineedit, 1, 0)

        self._version_spinbox = QNamedSpinBox(None, self._lang.get('QNamedSpinBox.version'))
        self._version_spinbox.setToolTip(self._lang.get('QToolTip.version'))
        self._version_spinbox.spin_box.valueChanged.connect(self._version_changed)
        self._version_spinbox.setRange(1, 1)
        self._version_spinbox.setValue(1)
        self._version_spinbox.setProperty('wide', True)
        self._top_info_widget.grid_layout.addWidget(self._version_spinbox, 1, 1)

        self._id_widget = IDWidget(path)
        self._id_widget.data_changed.connect(self._send_data)
        self._id_widget.property_entry_selected.connect(self._id_property_entry_selected)
        self.grid_layout.addWidget(self._id_widget, 1, 0)


        self._options_widget = OptionsWidget(path)
        self._options_widget.data_changed.connect(self._send_data)
        self._options_widget.property_entry_selected.connect(self._options_property_entry_selected)
        self.grid_layout.addWidget(self._options_widget, 2, 0)


        frame = QGridWidget()
        frame.grid_layout.setContentsMargins(0, 0, 0, 0)
        frame.grid_layout.setSpacing(8)
        self.grid_layout.addWidget(frame, 3, 0)

        label = QLabel(self._lang.get('QLabel.patches'))
        label.setProperty('h', 2)
        label.setProperty('small', True)
        frame.grid_layout.addWidget(label, 0, 0)

        self._patch_draglist = QDragList(None, Qt.Orientation.Vertical)
        self._patch_draglist.moved.connect(self._patch_entry_moved)
        frame.grid_layout.addWidget(self._patch_draglist, 1, 0)

        self._add_patch_entry_button = QPushButton(self._lang.get('QPushButton.addEntry'))
        self._add_patch_entry_button.setIcon(self._add_entry_icon)
        self._add_patch_entry_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self._add_patch_entry_button.setProperty('color', 'main')
        self._add_patch_entry_button.clicked.connect(self._add_patch_entry)
        frame.grid_layout.addWidget(self._add_patch_entry_button, 2, 0)
        self._add_patch_entry_button.setEnabled(False)

        self._wiidisc: WiiDisc = None


    @property
    def wiidisc(self) -> WiiDisc:
        return self._wiidisc
    
    @wiidisc.setter
    def wiidisc(self, wiidisc: WiiDisc) -> None:
        self._wiidisc = wiidisc

        self._disable_send = True

        self._version_spinbox.setValue(self._wiidisc.version if self._wiidisc else 1)
        self._root_lineedit.setText(self._wiidisc.root if self._wiidisc else '')

        self._id_widget.id = self._wiidisc.id if self._wiidisc else None
        self._options_widget.options = self._wiidisc.options if self._wiidisc else None

        self._patch_draglist.clear()

        self._add_patch_entry_button.setEnabled(self._wiidisc is not None)

        if self._wiidisc.patch_children:
            for patch in self._wiidisc.patch_children:
                pd = PatchData(patch, self._path)
                pd.data_changed.connect(self._send_data)
                pd.selected.connect(self._patch_property_entry_selected)
                pd.deleted.connect(self._delete_patch_entry)
                self._patch_draglist.add_item(pd)

        self._disable_send = False


    def _version_changed(self, value: int) -> None:
        if self._disable_send: return
        self._wiidisc.version = value
        self._send_data()

    def _root_changed(self, text: str) -> None:
        if self._disable_send: return
        if text != '' and not text.startswith('/'): text = f'/{text}'
        self._wiidisc.root = text
        self._root_lineedit.setText(text)
        self._send_data()

    def _send_data(self, *args) -> None:
        pass

    def _id_property_entry_selected(self, widget: QGridWidget or None) -> None:
        self.property_entry_selected.emit(widget)

        self._options_widget.deselect_all()
        self._patch_deselect_all()

    def _options_property_entry_selected(self, widget: QGridWidget or None) -> None:
        self.property_entry_selected.emit(widget)

        self._id_widget.deselect_all()
        self._patch_deselect_all()

    def _patch_deselect_all(self) -> None:
        for item in self._patch_draglist.items:
            item.set_checked(False)

    def _patch_property_entry_selected(self, sender: PatchData, widget: QGridWidget or None) -> None:
        self.property_entry_selected.emit(widget)

        checked = sender.is_checked()

        self._id_widget.deselect_all()
        self._options_widget.deselect_all()
        self._patch_deselect_all()

        sender.set_checked(checked)


    def _patch_entry_moved(self, old_index: int, new_index: int) -> None:
        self._wiidisc.patch_children.insert(new_index, self._wiidisc.patch_children.pop(old_index))
        self._send_data()

    def _add_patch_entry(self) -> None:
        p = Patch.create()
        self._wiidisc.patch_children.append(p)

        pd = PatchData(p, self._path)
        pd.data_changed.connect(self._send_data)
        pd.deleted.connect(self._delete_patch_entry)
        pd.selected.connect(self._patch_property_entry_selected)
        self._patch_draglist.add_item(pd)

        self._send_data()

    def _delete_patch_entry(self, item: PatchData) -> None:
        if self._wiidisc is None: return

        self.property_entry_selected.emit(None)

        self._wiidisc.patch_children.remove(item.data)
        item.setParent(None)
        item.deleteLater()

        self._send_data()
#----------------------------------------------------------------------
