#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QLabel
from PySide6.QtCore import QSize
from data.lib.QtUtils import QBaseApplication, QSaveData, QNamedLineEdit, QIconWidget
from .BaseItemData import BaseItemData
from ..sprites.MultiDualBox import MultiDualBox
#----------------------------------------------------------------------

    # Class
class MultiDualBoxData(BaseItemData):
    type: str = 'Multi Dual Box'
    child_cls = MultiDualBox

    _sublang = {}

    _multidualbox_icon = None
    _multidualbox_selected_icon = None
    _icon_size = QSize(32, 16)

    def init(app: QBaseApplication) -> None:
        MultiDualBoxData._sublang = app.get_lang_data('QMainWindow.QSlidingStackedWidget.mainMenu.projects.projectWidget.Wii.NSMBW.ReggieNextWidget.SpriteWidget.MultiDualBoxData')
        MultiDualBoxData._multidualbox_icon = app.get_icon('baseitemdata/multidualbox.png', True, QSaveData.IconMode.Local)
        MultiDualBoxData._multidualbox_selected_icon = app.get_icon('baseitemdata/multidualboxSelected.png', True, QSaveData.IconMode.Local)

        MultiDualBoxData.type = app.get_lang_data(f'QMainWindow.QSlidingStackedWidget.mainMenu.projects.projectWidget.Wii.NSMBW.ReggieNextWidget.type.{MultiDualBox.name}')

    def __init__(self, data: MultiDualBox, path: str) -> None:
        super().__init__(data, path)

        self._title1_label = QLabel(self._data.title1)
        self._title1_label.setProperty('brighttitle', True)
        self._content_frame.grid_layout.addWidget(self._title1_label, 0, 0)

        iw = QIconWidget(None, self._multidualbox_selected_icon, self._icon_size, False)
        self._content_frame.grid_layout.addWidget(iw, 0, 1)

        label = QLabel('|')
        label.setProperty('brighttitle', True)
        self._content_frame.grid_layout.addWidget(label, 0, 2)

        iw = QIconWidget(None, self._multidualbox_icon, self._icon_size, False)
        self._content_frame.grid_layout.addWidget(iw, 0, 3)

        self._title2_label = QLabel(self._data.title2)
        self._title2_label.setProperty('brighttitle', True)
        self._content_frame.grid_layout.addWidget(self._title2_label, 0, 4)

        self._content_frame.grid_layout.setColumnStretch(4, 1)

        self._property_last_frame.title1_lineedit = QNamedLineEdit(None, '', self._sublang.get('QNamedLineEdit.title1'))
        self._property_last_frame.title1_lineedit.setText(self._data.title1)
        self._property_last_frame.title1_lineedit.line_edit.textChanged.connect(self._title1_changed)
        self._property_last_frame.grid_layout.addWidget(self._property_last_frame.title1_lineedit, 0, 0)

        self._property_last_frame.title2_lineedit = QNamedLineEdit(None, '', self._sublang.get('QNamedLineEdit.title2'))
        self._property_last_frame.title2_lineedit.setText(self._data.title2)
        self._property_last_frame.title2_lineedit.line_edit.textChanged.connect(self._title2_changed)
        self._property_last_frame.grid_layout.addWidget(self._property_last_frame.title2_lineedit, 0, 1)


    def _title1_changed(self) -> None:
        self._data.title1 = self._property_last_frame.title1_lineedit.text()
        self._title1_label.setText(self._data.title1)
        self.data_changed.emit()

    def _title2_changed(self) -> None:
        self._data.title2 = self._property_last_frame.title2_lineedit.text()
        self._title2_label.setText(self._data.title2)
        self.data_changed.emit()
#----------------------------------------------------------------------
