#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QPushButton
from PySide6.QtCore import Qt, Signal
from data.lib.qtUtils import QBaseApplication, QGridWidget, QSaveData, QDragList, QNamedComboBox, QNamedLineEdit, QNamedSpinBox, QNamedToggleButton
from data.lib.widgets.ProjectKeys import ProjectKeys
from .sprites.Sprite import Sprite
#----------------------------------------------------------------------

    # Class
class SpriteWidget(QGridWidget):
    type: ProjectKeys = ProjectKeys.ReggieNext

    _add_entry_icon = None

    _lang = {}

    sprite_edited = Signal()

    def init(app: QBaseApplication) -> None:
        SpriteWidget._lang = app.get_lang_data('QMainWindow.QSlidingStackedWidget.mainMenu.projects.ReggieNextWidget.SpriteWidget')
        SpriteWidget._add_entry_icon = app.get_icon('pushbutton/add.png', True, QSaveData.IconMode.Local)

    def __init__(self) -> None:
        super().__init__()

        self._disable_send = True

        self._top_info_widget = QGridWidget()
        self._top_info_widget.grid_layout.setContentsMargins(0, 0, 0, 0)
        self._top_info_widget.grid_layout.setSpacing(8)
        self.grid_layout.addWidget(self._top_info_widget, 0, 0)

        self._id_spinbox = QNamedSpinBox(None, self._lang.get_data('QNamedSpinBox.spriteID'))
        self._id_spinbox.spin_box.valueChanged.connect(self._send_data)
        self._id_spinbox.setRange(0, 2147483647) # profileID is u32 (2^32 - 1) but QSpinBox are s32 (2^31 - 1) -> Tbf nobody will have 2^31 sprites lmao
        self._id_spinbox.setValue(0)
        self._id_spinbox.setProperty('wide', True)
        self._top_info_widget.grid_layout.addWidget(self._id_spinbox, 0, 0)

        self._name_lineedit = QNamedLineEdit(None, '', self._lang.get_data('QNamedLineEdit.name'))
        self._name_lineedit.line_edit.textChanged.connect(self._send_data)
        self._top_info_widget.grid_layout.addWidget(self._name_lineedit, 0, 1)


        self._settings_widget = QGridWidget()
        self._settings_widget.grid_layout.setContentsMargins(0, 0, 0, 0)
        self._settings_widget.grid_layout.setSpacing(8)
        self.grid_layout.addWidget(self._settings_widget, 1, 0)

        self._drag_list = QDragList(None, Qt.Orientation.Vertical)
        self._settings_widget.grid_layout.addWidget(self._drag_list, 0, 0)

        self._add_entry_button = QPushButton(self._lang.get_data('QPushButton.addEntry'))
        self._add_entry_button.setIcon(self._add_entry_icon)
        self._add_entry_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self._add_entry_button.setProperty('color', 'main')
        self._add_entry_button.clicked.connect(self._add_entry)
        self._settings_widget.grid_layout.addWidget(self._add_entry_button, 1, 0, Qt.AlignmentFlag.AlignBottom)

        self.sprite = None


    @property
    def sprite(self) -> Sprite or None:
        self._sprite.name = self._name_lineedit.text()
        self._sprite.id = self._id_spinbox.value()

        return self._sprite

    @sprite.setter
    def sprite(self, sprite: Sprite or None) -> None:
        self._sprite = sprite

        self._disable_send = True

        self._drag_list.clear()
        self.setEnabled(sprite is not None)

        if sprite is None:
            self._name_lineedit.setText('')
            self._id_spinbox.setValue(0)

        else:
            self._name_lineedit.setText(sprite.name)
            self._id_spinbox.setValue(sprite.id)
            # todo: add entries to drag list

        self._disable_send = False


    def _send_data(self, *args) -> None:
        if self._disable_send: return
        self.sprite_edited.emit()


    def _add_entry(self) -> None:
        self._send_data()
        # todo: add entry to drag list
#----------------------------------------------------------------------
