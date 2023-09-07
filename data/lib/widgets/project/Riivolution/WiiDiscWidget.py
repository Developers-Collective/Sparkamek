#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QLabel
from PySide6.QtCore import Signal
from data.lib.qtUtils import QBaseApplication, QGridWidget, QSaveData, QDragListItem, QNamedLineEdit, QNamedSpinBox
from data.lib.widgets.ProjectKeys import ProjectKeys
from .items import WiiDisc
from .IDWidget import IDWidget
from .OptionsWidget import OptionsWidget
# from .PatchWidget import PatchWidget
from .itemdata.BaseItemData import BaseItemData
from .itemdata.BaseSubItemData import BaseSubItemData
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
        BaseSubItemData.init(app)
        IDWidget.init(app)
        OptionsWidget.init(app)
        # PatchWidget.init(app)

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

        label = QLabel(self._lang.get_data('QLabel.generalInfo'))
        label.setProperty('h', 2)
        label.setProperty('small', True)
        self._top_info_widget.grid_layout.addWidget(label, 0, 0, 1, 2)

        self._root_lineedit = QNamedLineEdit(None, '', self._lang.get_data('QNamedLineEdit.root'))
        self._root_lineedit.line_edit.textChanged.connect(self._root_changed)
        self._top_info_widget.grid_layout.addWidget(self._root_lineedit, 1, 0)

        self._version_spinbox = QNamedSpinBox(None, self._lang.get_data('QNamedSpinBox.version'))
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

        # self._patch_widget = PatchWidget(path)
        # self._patch_widget.data_changed.connect(self._send_data)
        # self._patch_widget.property_entry_selected.connect(self._patch_property_entry_selected)
        # self.grid_layout.addWidget(self._patch_widget, 3, 0)

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
        # self._patch_widget.patch = self._wiidisc.patch if self._wiidisc else None

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
        # self._patch_widget.deselect_all()

    def _options_property_entry_selected(self, widget: QGridWidget or None) -> None:
        self.property_entry_selected.emit(widget)

        self._id_widget.deselect_all()
        # self._patch_widget.deselect_all()

    # def _patch_property_entry_selected(self, widget: QGridWidget or None) -> None:
    #     self.property_entry_selected.emit(widget)

    #     self._id_widget.deselect_all()
    #     self._options_widget.deselect_all()

    #     # todo: unselect all other widgets
#----------------------------------------------------------------------
