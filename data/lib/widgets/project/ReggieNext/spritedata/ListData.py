#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QLabel, QPushButton
from PySide6.QtCore import QSize, Qt
from data.lib.qtUtils import QGridWidget, QBaseApplication, QSaveData, QNamedLineEdit, QIconWidget, QDragList
from .BaseItemData import BaseItemData
from .EntryListItem import EntryListItem
from ..sprites.List import List, Entry
#----------------------------------------------------------------------

    # Class
class ListData(BaseItemData):
    type: str = 'List'
    child_cls = List

    _sublang = {}

    _list_icon = None
    _add_icon = None
    _icon_size = QSize(24, 24)

    def init(app: QBaseApplication) -> None:
        ListData._sublang = app.get_lang_data('QMainWindow.QSlidingStackedWidget.mainMenu.projects.ReggieNextWidget.SpriteWidget.ListData')
        ListData._list_icon = app.get_icon('baseitemdata/list.png', True, QSaveData.IconMode.Local)
        ListData._add_icon = app.get_icon('pushbutton/add.png', True, QSaveData.IconMode.Local)

        ListData.type = app.get_lang_data(f'QMainWindow.QSlidingStackedWidget.mainMenu.projects.ReggieNextWidget.type.{List.name}')

        EntryListItem.init(app)

    def __init__(self, data: List, path: str) -> None:
        super().__init__(data, path)

        self._title_label = QLabel(self._data.title)
        self._title_label.setProperty('brighttitle', True)
        self._content_frame.grid_layout.addWidget(self._title_label, 0, 0)

        iw = QIconWidget(None, self._list_icon, self._icon_size, False)
        self._content_frame.grid_layout.addWidget(iw, 0, 1)

        self._content_frame.grid_layout.setColumnStretch(2, 1)

        self._property_last_frame.title_lineedit = QNamedLineEdit(None, '', self._sublang.get_data('QNamedLineEdit.title'))
        self._property_last_frame.title_lineedit.setText(self._data.title)
        self._property_last_frame.title_lineedit.line_edit.textChanged.connect(self._title_changed)
        self._property_last_frame.grid_layout.addWidget(self._property_last_frame.title_lineedit, 0, 0)

        bottom_frame = QGridWidget()
        bottom_frame.grid_layout.setContentsMargins(0, 0, 0, 0)
        bottom_frame.grid_layout.setSpacing(8)
        self._property_last_frame.grid_layout.addWidget(bottom_frame, 1, 0)

        self._property_last_frame.items_draglist = QDragList(None, Qt.Orientation.Vertical)
        self._property_last_frame.items_draglist.moved.connect(self.move_item)
        bottom_frame.grid_layout.addWidget(self._property_last_frame.items_draglist, 0, 0)

        add_item_button = QPushButton(self._sublang.get_data('QPushButton.add'))
        add_item_button.setIcon(self._add_icon)
        add_item_button.setProperty('color', 'main')
        add_item_button.setCursor(Qt.CursorShape.PointingHandCursor)
        add_item_button.clicked.connect(self._add_item)
        bottom_frame.grid_layout.addWidget(add_item_button, 2, 0)

        for child in self._data.children:
            entry_list_item = EntryListItem(child)
            entry_list_item.data_changed.connect(self.data_changed.emit)
            entry_list_item.deleted.connect(self._remove_item)
            self._property_last_frame.items_draglist.add_item(entry_list_item)


    def _title_changed(self) -> None:
        self._data.title = self._property_last_frame.title_lineedit.text()
        self._title_label.setText(self._data.title)
        self.data_changed.emit()

    def _add_item(self, item: EntryListItem) -> None:
        entry = Entry.create()
        self._data.children.append(entry)
        entry_list_item = EntryListItem(entry)
        entry_list_item.data_changed.connect(self.data_changed.emit)
        entry_list_item.deleted.connect(self._remove_item)
        self._property_last_frame.items_draglist.add_item(entry_list_item)
        self.data_changed.emit()

    def _remove_item(self, item: EntryListItem) -> None:
        self._data.children.remove(item.data)
        item.deleteLater()
        self.data_changed.emit()

    def move_item(self, from_: int, to_: int) -> None:
        self._data.children.insert(to_, self._data.children.pop(from_))
        self.data_changed.emit()
#----------------------------------------------------------------------
