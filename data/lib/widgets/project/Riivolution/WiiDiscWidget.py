#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QPushButton, QLabel, QMenu
from PySide6.QtCore import Qt, Signal, QPoint
from PySide6.QtGui import QAction
from data.lib.qtUtils import QBaseApplication, QGridWidget, QSaveData, QDragList, QNamedTextEdit, QNamedLineEdit, QNamedSpinBox, QNamedToggleButton
from data.lib.widgets.ProjectKeys import ProjectKeys
from .items import WiiDisc
#----------------------------------------------------------------------

    # Class
class WiiDiscWidget(QGridWidget):
    type: ProjectKeys = ProjectKeys.ReggieNext

    _app: QBaseApplication = None

    _add_entry_icon = None
    _add_item_entry_icon = None

    _lang = {}

    def init(app: QBaseApplication) -> None:
        WiiDiscWidget._app = app

        WiiDiscWidget._lang = app.get_lang_data('QMainWindow.QSlidingStackedWidget.mainMenu.projects.RiivolutionWidget.WiiDiscWidget')
        WiiDiscWidget._add_entry_icon = app.get_icon('pushbutton/add.png', True, QSaveData.IconMode.Local)
        WiiDiscWidget._add_item_entry_icon = app.get_icon('popup/addItem.png', True, QSaveData.IconMode.Local)

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
        self._root_lineedit.line_edit.textChanged.connect(self._send_data)
        self._top_info_widget.grid_layout.addWidget(self._root_lineedit, 1, 0)

        self._version_spinbox = QNamedSpinBox(None, self._lang.get_data('QNamedSpinBox.version'))
        self._version_spinbox.spin_box.valueChanged.connect(self._send_data)
        self._version_spinbox.setRange(1, 1)
        self._version_spinbox.setValue(1)
        self._version_spinbox.setProperty('wide', True)
        self._top_info_widget.grid_layout.addWidget(self._version_spinbox, 1, 1)

        self._wiidisc: WiiDisc = None


    @property
    def wiidisc(self) -> WiiDisc:
        return self._wiidisc
    
    @wiidisc.setter
    def wiidisc(self, wiidisc: WiiDisc) -> None:
        self._wiidisc = wiidisc

        self._disable_send = True

        self._version_spinbox.setValue(self._wiidisc.version)
        self._root_lineedit.setText(self._wiidisc.root)

        self._disable_send = False


    def _send_data(self, *args) -> None:
        pass
#----------------------------------------------------------------------
