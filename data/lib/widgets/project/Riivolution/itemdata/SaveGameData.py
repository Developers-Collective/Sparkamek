#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QLabel, QPushButton
from PySide6.QtCore import Qt
from data.lib.qtUtils import QBaseApplication, QNamedLineEdit, QNamedToggleButton, QGridWidget, QSaveData
from ..items.SaveGame import SaveGame
from .BaseSubItemData import BaseSubItemData
#----------------------------------------------------------------------

    # Class
class SaveGameData(BaseSubItemData):
    type: str = 'SaveGame'
    child_cls: SaveGame = SaveGame

    _back_icon = None

    _lang = {}

    def init(app: QBaseApplication) -> None:
        SaveGameData._lang = app.get_lang_data('QMainWindow.QSlidingStackedWidget.mainMenu.projects.RiivolutionWidget.WiiDiscWidget.PatchData.PropertyWidget.SaveGameData')

        SaveGameData._back_icon = app.get_icon('pushbutton/back.png', True, QSaveData.IconMode.Local)

    def __init__(self, data: SaveGame, path: str) -> None:
        super().__init__(data, path)

        self._disable_send = False
        self._current_widget = None

        self._text_label = QLabel()
        self._text_label.setProperty('brighttitle', True)
        self._content_frame.grid_layout.addWidget(self._text_label, 0, 0)


        self._back_button = QPushButton()
        self._back_button.setIcon(self._back_icon)
        self._back_button.setText(self._lang.get_data('QPushButton.back'))
        self._back_button.setProperty('color', 'main')
        self._back_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self._back_button.clicked.connect(self.back_pressed.emit)
        self._property_frame.grid_layout.addWidget(self._back_button, 0, 0, Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)


        subframe = QGridWidget()
        subframe.grid_layout.setSpacing(8)
        subframe.grid_layout.setContentsMargins(0, 0, 0, 0)
        self._property_frame.grid_layout.addWidget(subframe, 1, 0)


        self._external_lineedit = QNamedLineEdit(None, '', self._lang.get_data('PropertyWidget.QNamedLineEdit.external'))
        self._external_lineedit.line_edit.setText(self._data.external)
        self._external_lineedit.line_edit.textChanged.connect(self._external_changed)
        subframe.grid_layout.addWidget(self._external_lineedit, 0, 0)

        self._clone_togglebutton = QNamedToggleButton(None, self._lang.get_data('PropertyWidget.QNamedToggleButton.clone'), self._data.clone, True)
        self._clone_togglebutton.toggled.connect(self._clone_toggled)
        subframe.grid_layout.addWidget(self._clone_togglebutton, 0, 1)

        self._property_frame.grid_layout.setRowStretch(2, 1)

        self._update_text()

        self._disable_send = False


    def _update_text(self) -> None:
        self._text_label.setText(self._data.external)

    def _external_changed(self, text: str) -> None:
        if not text: return

        if not text.startswith('/'): text = f'/{text}'
        self._external_lineedit.setText(text)

        self._data.external = text
        self._send_data()

    def _clone_toggled(self, checked: bool) -> None:
        self._data.clone = checked
        self._send_data()


    def _send_data(self, *args) -> None:
        if self._disable_send: return

        self._update_text()
        self.data_changed.emit()
#----------------------------------------------------------------------
