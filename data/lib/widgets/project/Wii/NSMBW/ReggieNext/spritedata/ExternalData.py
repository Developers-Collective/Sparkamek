#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QLabel
from PySide6.QtCore import QSize
from data.lib.QtUtils import QNamedComboBox, QBaseApplication, QSaveData, QNamedLineEdit, QIconWidget
from .BaseItemData import BaseItemData
from ..sprites.External import External
import os
#----------------------------------------------------------------------

    # Class
class ExternalData(BaseItemData):
    type: str = 'External'
    child_cls = External

    _sublang = {}

    _external_icon = None
    _icon_size = QSize(24, 24)

    def init(app: QBaseApplication) -> None:
        ExternalData._sublang = app.get_lang_data('QMainWindow.QSlidingStackedWidget.mainMenu.projects.projectWidget.Wii.NSMBW.ReggieNextWidget.SpriteWidget.ExternalData')
        ExternalData._external_icon = app.get_icon('baseitemdata/external.png', True, QSaveData.IconMode.Local)

        ExternalData.type = app.get_lang_data(f'QMainWindow.QSlidingStackedWidget.mainMenu.projects.projectWidget.Wii.NSMBW.ReggieNextWidget.type.{External.name}')

    def __init__(self, data: External, path: str) -> None:
        super().__init__(data, path)

        self._title_label = QLabel(self._data.title)
        self._title_label.setProperty('brighttitle', True)
        self._content_frame.layout_.addWidget(self._title_label, 0, 0)

        iw = QIconWidget(None, self._external_icon, self._icon_size, False)
        self._content_frame.layout_.addWidget(iw, 0, 1)

        self._external_type_label = QLabel(self._data.type)
        self._external_type_label.setProperty('brighttitle', True)
        self._content_frame.layout_.addWidget(self._external_type_label, 0, 2)

        self._content_frame.layout_.setColumnStretch(3, 1)

        self._property_last_frame.title_lineedit = QNamedLineEdit(None, '', self._sublang.get('QNamedLineEdit.title'))
        self._property_last_frame.title_lineedit.setText(self._data.title)
        self._property_last_frame.title_lineedit.line_edit.textChanged.connect(self._title_changed)
        self._property_last_frame.layout_.addWidget(self._property_last_frame.title_lineedit, 0, 0)

        self._files = []
        if os.path.isdir(f'{path}/external'):
            for file in os.listdir(f'{path}/external'):
                if file.endswith('.xml'):
                    try: self._files.append(os.path.splitext(os.path.basename(file))[0])
                    except: pass

        self._property_last_frame.type_combobox = QNamedComboBox(None, self._sublang.get('QNamedComboBox.type'))
        self._property_last_frame.type_combobox.combo_box.addItems(self._files)
        if self._data.type in self._files: self._property_last_frame.type_combobox.combo_box.setCurrentIndex(self._files.index(self._data.type))
        self._property_last_frame.type_combobox.combo_box.currentIndexChanged.connect(self._type_changed)
        self._property_last_frame.layout_.addWidget(self._property_last_frame.type_combobox, 0, 1)


    def _title_changed(self) -> None:
        self._data.title = self._property_last_frame.title_lineedit.text()
        self._title_label.setText(self._data.title)
        self.data_changed.emit()

    def _type_changed(self, index: int) -> None:
        self._data.type = self._files[index]
        self._external_type_label.setText(self._data.type)
        self.data_changed.emit()
#----------------------------------------------------------------------
