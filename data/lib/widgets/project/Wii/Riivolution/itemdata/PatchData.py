#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QLabel, QPushButton, QMenu
from PySide6.QtCore import Qt, QPoint
from PySide6.QtGui import QAction
from data.lib.qtUtils import QBaseApplication, QNamedLineEdit, QSlidingStackedWidget, QGridWidget, QSaveData, QDragList, QScrollableGridFrame, QLangData
from ..items.Patch import Patch
from .BaseItemData import BaseItemData
from .FileData import FileData
from .FolderData import FolderData
from .SaveGameData import SaveGameData
from .MemoryDataFactory import MemoryDataFactory
from .MemoryValueData import MemoryValueData, MemoryValue
from .MemoryValueFileData import MemoryValueFileData, MemoryValueFile
from .MemorySearchValueData import MemorySearchValueData, MemorySearchValue
from .MemorySearchValueFileData import MemorySearchValueFileData, MemorySearchValueFile
from .MemoryOcarinaData import MemoryOcarinaData, MemoryOcarina
#----------------------------------------------------------------------

    # Class
class PatchData(BaseItemData):
    type: str = 'Patch'
    child_cls: Patch = Patch

    _add_entry_icon = None
    _add_memory_entry_icon = None

    _lang: QLangData = QLangData.NoTranslation()

    def init(app: QBaseApplication) -> None:
        PatchData._lang = app.get_lang_data('QMainWindow.QSlidingStackedWidget.mainMenu.projects.projectWidget.Wii.RiivolutionWidget.WiiDiscWidget.PatchData')

        PatchData._add_entry_icon = app.get_icon('pushbutton/add.png', True, QSaveData.IconMode.Local)
        PatchData._add_memory_entry_icon = app.get_icon('popup/addMemory.png', True, QSaveData.IconMode.Local)

        FileData.init(app)
        FolderData.init(app)
        SaveGameData.init(app)
        MemoryDataFactory.init(app)

    def __init__(self, data: Patch, path: str) -> None:
        super().__init__(data, path)

        self._disable_send = False
        self._current_widget = None

        self._patchid_label = QLabel()
        self._patchid_label.setProperty('brighttitle', True)
        self._content_frame.grid_layout.addWidget(self._patchid_label, 0, 0)

        self._child_pages = QSlidingStackedWidget()
        self._child_pages.set_orientation(Qt.Orientation.Horizontal)
        self._property_frame.grid_layout.addWidget(self._child_pages, 0, 0)


        frame = QScrollableGridFrame()
        frame.set_all_property('transparent', True)
        frame.scroll_layout.setSpacing(30)
        frame.scroll_layout.setContentsMargins(0, 0, 10, 0)

        self._child_pages.addWidget(frame)


        subframe = QGridWidget()
        subframe.grid_layout.setSpacing(8)
        subframe.grid_layout.setContentsMargins(0, 0, 0, 0)
        frame.scroll_layout.addWidget(subframe, 0, 0, 1, 2)

        label = QLabel(self._lang.get('QLabel.generalInfo'))
        label.setProperty('h', 2)
        label.setProperty('small', True)
        subframe.grid_layout.addWidget(label, 0, 0)

        self._id_lineedit = QNamedLineEdit(None, '', self._lang.get('PropertyWidget.QNamedLineEdit.id'))
        self._id_lineedit.setToolTip(self._lang.get('PropertyWidget.QToolTip.id'))
        self._id_lineedit.line_edit.setText(self._data.id)
        self._id_lineedit.line_edit.textChanged.connect(self._id_changed)
        subframe.grid_layout.addWidget(self._id_lineedit, 1, 0)

        self._root_lineedit = QNamedLineEdit(None, '', self._lang.get('PropertyWidget.QNamedLineEdit.root'))
        self._root_lineedit.setToolTip(self._lang.get('PropertyWidget.QToolTip.root'))
        self._root_lineedit.line_edit.setText(self._data.root)
        self._root_lineedit.line_edit.textChanged.connect(self._root_changed)
        subframe.grid_layout.addWidget(self._root_lineedit, 2, 0)

        subframe.grid_layout.setRowStretch(3, 1)


        leftframe = QGridWidget()
        leftframe.grid_layout.setSpacing(30)
        leftframe.grid_layout.setContentsMargins(0, 0, 0, 0)
        frame.scroll_layout.addWidget(leftframe, 1, 0)

        rightframe = QGridWidget()
        rightframe.grid_layout.setSpacing(30)
        rightframe.grid_layout.setContentsMargins(0, 0, 0, 0)
        frame.scroll_layout.addWidget(rightframe, 1, 1)


        subframe = QGridWidget()
        subframe.grid_layout.setSpacing(8)
        subframe.grid_layout.setContentsMargins(0, 0, 0, 0)
        leftframe.grid_layout.addWidget(subframe, 0, 0)

        label = QLabel(self._lang.get('QLabel.files'))
        label.setProperty('h', 2)
        label.setProperty('small', True)
        subframe.grid_layout.addWidget(label, 0, 0)

        self._file_draglist = QDragList()
        self._file_draglist.moved.connect(self._file_entry_moved)
        subframe.grid_layout.addWidget(self._file_draglist, 1, 0)

        self._add_file_entry_button = QPushButton(self._lang.get('QPushButton.addFile'))
        self._add_file_entry_button.setIcon(self._add_entry_icon)
        self._add_file_entry_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self._add_file_entry_button.setProperty('color', 'main')
        self._add_file_entry_button.clicked.connect(self._add_file_entry)
        subframe.grid_layout.addWidget(self._add_file_entry_button, 2, 0)
        self._add_file_entry_button.setEnabled(False)

        subframe.grid_layout.setRowStretch(3, 1)


        subframe = QGridWidget()
        subframe.grid_layout.setSpacing(8)
        subframe.grid_layout.setContentsMargins(0, 0, 0, 0)
        rightframe.grid_layout.addWidget(subframe, 0, 0)

        label = QLabel(self._lang.get('QLabel.folders'))
        label.setProperty('h', 2)
        label.setProperty('small', True)
        subframe.grid_layout.addWidget(label, 0, 0)

        self._folder_draglist = QDragList()
        self._folder_draglist.moved.connect(self._folder_entry_moved)
        subframe.grid_layout.addWidget(self._folder_draglist, 1, 0)

        self._add_folder_entry_button = QPushButton(self._lang.get('QPushButton.addFolder'))
        self._add_folder_entry_button.setIcon(self._add_entry_icon)
        self._add_folder_entry_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self._add_folder_entry_button.setProperty('color', 'main')
        self._add_folder_entry_button.clicked.connect(self._add_folder_entry)
        subframe.grid_layout.addWidget(self._add_folder_entry_button, 2, 0)
        self._add_folder_entry_button.setEnabled(False)

        subframe.grid_layout.setRowStretch(3, 1)


        subframe = QGridWidget()
        subframe.grid_layout.setSpacing(8)
        subframe.grid_layout.setContentsMargins(0, 0, 0, 0)
        leftframe.grid_layout.addWidget(subframe, 1, 0)

        label = QLabel(self._lang.get('QLabel.savegames'))
        label.setProperty('h', 2)
        label.setProperty('small', True)
        subframe.grid_layout.addWidget(label, 0, 0)

        self._savegame_draglist = QDragList()
        self._savegame_draglist.moved.connect(self._savegame_entry_moved)
        subframe.grid_layout.addWidget(self._savegame_draglist, 1, 0)

        self._add_savegame_entry_button = QPushButton(self._lang.get('QPushButton.addSavegame'))
        self._add_savegame_entry_button.setIcon(self._add_entry_icon)
        self._add_savegame_entry_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self._add_savegame_entry_button.setProperty('color', 'main')
        self._add_savegame_entry_button.clicked.connect(self._add_savegame_entry)
        subframe.grid_layout.addWidget(self._add_savegame_entry_button, 2, 0)
        self._add_savegame_entry_button.setEnabled(False)


        subframe = QGridWidget()
        subframe.grid_layout.setSpacing(8)
        subframe.grid_layout.setContentsMargins(0, 0, 0, 0)
        leftframe.grid_layout.addWidget(subframe, 2, 0)

        label = QLabel(self._lang.get('QLabel.memories'))
        label.setProperty('h', 2)
        label.setProperty('small', True)
        subframe.grid_layout.addWidget(label, 0, 0)

        self._memory_draglist = QDragList()
        self._memory_draglist.moved.connect(self._memory_entry_moved)
        subframe.grid_layout.addWidget(self._memory_draglist, 1, 0)

        self._add_memory_entry_button = QPushButton(self._lang.get('QPushButton.addMemory'))
        self._add_memory_entry_button.setIcon(self._add_entry_icon)
        self._add_memory_entry_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self._add_memory_entry_button.setProperty('color', 'main')
        self._add_memory_entry_button.clicked.connect(self._add_memory_entry)
        subframe.grid_layout.addWidget(self._add_memory_entry_button, 2, 0)
        self._add_memory_entry_button.setEnabled(False)


        subframe.grid_layout.setRowStretch(3, 1)

        leftframe.grid_layout.setRowStretch(2, 1)
        frame.scroll_layout.setRowStretch(2, 1)


        self._data_frame = QGridWidget()
        self._data_frame.grid_layout.setSpacing(8)
        self._data_frame.grid_layout.setContentsMargins(0, 0, 0, 0)

        self._child_pages.addWidget(self._data_frame)

        self._update_text()

        self._load_data()


    def _load_data(self) -> None:
        self._disable_send = True

        self._file_draglist.clear()
        self._add_file_entry_button.setEnabled(self._data is not None)
        if self._data:
            for file in self._data.file_children:
                fd = FileData(file, self._path)
                fd.data_changed.connect(self._send_data)
                fd.edited.connect(self._entry_selected)
                fd.deleted.connect(self._delete_file_entry)
                self._file_draglist.add_item(fd)

        self._folder_draglist.clear()
        self._add_folder_entry_button.setEnabled(self._data is not None)
        if self._data:
            for folder in self._data.folder_children:
                fd = FolderData(folder, self._path)
                fd.data_changed.connect(self._send_data)
                fd.edited.connect(self._entry_selected)
                fd.deleted.connect(self._delete_folder_entry)
                self._folder_draglist.add_item(fd)

        self._savegame_draglist.clear()
        self._add_savegame_entry_button.setEnabled(self._data is not None)
        if self._data:
            for savegame in self._data.savegame_children:
                sgd = SaveGameData(savegame, self._path)
                sgd.data_changed.connect(self._send_data)
                sgd.edited.connect(self._entry_selected)
                sgd.deleted.connect(self._delete_savegame_entry)
                self._savegame_draglist.add_item(sgd)

        self._memory_draglist.clear()
        self._add_memory_entry_button.setEnabled(self._data is not None)
        if self._data:
            for memory in self._data.memory_children:
                type_ = type(memory)
                if (type_ is MemoryValue): md = MemoryValueData(memory, self._path)
                elif (type_ is MemoryValueFile): md = MemoryValueFileData(memory, self._path)
                elif (type_ is MemorySearchValue): md = MemorySearchValueData(memory, self._path)
                elif (type_ is MemorySearchValueFile): md = MemorySearchValueFileData(memory, self._path)
                elif (type_ is MemoryOcarina): md = MemoryOcarinaData(memory, self._path)

                else: continue

                md.data_changed.connect(self._send_data)
                md.edited.connect(self._entry_selected)
                md.deleted.connect(self._delete_memory_entry)
                self._memory_draglist.add_item(md)

        self._disable_send = False


    def _update_text(self) -> None:
        s = self._lang.get('QLabel.text').replace(
            '%s', self._data.id, 1
        ).replace(
            '%s', str(
                len(self._data.file_children) + len(self._data.folder_children) + len(self._data.savegame_children) + len(self._data.memory_children)
            ), 1
        )
        self._patchid_label.setText(s)


    def _id_changed(self, text: str) -> None:
        if not text: return

        self._data.id = text
        self._update_text()
        self.data_changed.emit()

    def _root_changed(self, text: str) -> None:
        if not text: return

        self._data.root = text
        self.data_changed.emit()


    def _file_entry_moved(self, old_index: int, new_index: int) -> None:
        self._data.file_children.insert(new_index, self._data.file_children.pop(old_index))
        self._send_data()

    def _add_file_entry(self) -> None:
        f = FileData.child_cls.create()
        self._data.file_children.append(f)

        fd = FileData(f, self._path)
        fd.data_changed.connect(self._send_data)
        fd.deleted.connect(self._delete_file_entry)
        fd.edited.connect(self._entry_selected)
        self._file_draglist.add_item(fd)

        self._send_data()

    def _delete_file_entry(self, item: FileData) -> None:
        if self._data is None: return

        self._data.file_children.remove(item.data)
        item.setParent(None)
        item.deleteLater()

        self._child_pages.slide_in_index(0)

        self._send_data()


    def _folder_entry_moved(self, old_index: int, new_index: int) -> None:
        self._data.folder_children.insert(new_index, self._data.folder_children.pop(old_index))
        self._send_data()

    def _add_folder_entry(self) -> None:
        f = FolderData.child_cls.create()
        self._data.folder_children.append(f)

        fd = FolderData(f, self._path)
        fd.data_changed.connect(self._send_data)
        fd.deleted.connect(self._delete_folder_entry)
        fd.edited.connect(self._entry_selected)
        self._folder_draglist.add_item(fd)

        self._send_data()

    def _delete_folder_entry(self, item: FolderData) -> None:
        if self._data is None: return

        self._data.folder_children.remove(item.data)
        item.setParent(None)
        item.deleteLater()

        self._child_pages.slide_in_index(0)

        self._send_data()


    def _savegame_entry_moved(self, old_index: int, new_index: int) -> None:
        self._data.savegame_children.insert(new_index, self._data.savegame_children.pop(old_index))
        self._send_data()

    def _add_savegame_entry(self) -> None:
        sg = SaveGameData.child_cls.create()
        self._data.savegame_children.append(sg)

        sgd = SaveGameData(sg, self._path)
        sgd.data_changed.connect(self._send_data)
        sgd.deleted.connect(self._delete_savegame_entry)
        sgd.edited.connect(self._entry_selected)
        self._savegame_draglist.add_item(sgd)

        self._send_data()

    def _delete_savegame_entry(self, item: SaveGameData) -> None:
        if self._data is None: return

        self._data.savegame_children.remove(item.data)
        item.setParent(None)
        item.deleteLater()

        self._child_pages.slide_in_index(0)

        self._send_data()


    def _memory_entry_moved(self, old_index: int, new_index: int) -> None:
        self._data.memory_children.insert(new_index, self._data.memory_children.pop(old_index))
        self._send_data()

    def _add_memory_entry(self) -> None:
        lang = self._lang.get('QMenu.addEntry')
        send_param = lambda k: lambda: self._add_memory_entry_clicked(k)

        menu = QMenu(self)
        menu.setCursor(Qt.CursorShape.PointingHandCursor)

        actions_add_entry = []

        for memory_item_t in MemoryDataFactory.get_all():
            action_add_entry = QAction(lang.get(f'QAction.add{memory_item_t.child_cls.key.title()}'))
            action_add_entry.setIcon(self._add_memory_entry_icon)
            action_add_entry.triggered.connect(send_param(memory_item_t.child_cls.key))
            actions_add_entry.append(action_add_entry)

        for a in actions_add_entry: menu.addAction(a) # Doesn't work if I do it in the loop above for some reason

        menu.exec(self._add_memory_entry_button.mapToGlobal(QPoint(0, 0)))

        self._send_data()

    def _add_memory_entry_clicked(self, key: str) -> None:
        cls_ = MemoryDataFactory.get(key)
        if cls_ is None: return

        m = cls_.child_cls.create()
        self._data.memory_children.append(m)

        md = cls_(m, self._path)
        md.data_changed.connect(self._send_data)
        md.deleted.connect(self._delete_memory_entry)
        md.edited.connect(self._entry_selected)
        self._memory_draglist.add_item(md)

        self._send_data()

    def _delete_memory_entry(self, item: MemoryValueData) -> None:
        if self._data is None: return

        self._data.memory_children.remove(item.data)
        item.setParent(None)
        item.deleteLater()

        self._child_pages.slide_in_index(0)

        self._send_data()


    def _entry_selected(self, sender: FileData | FolderData | SaveGameData, widget: QGridWidget | None) -> None:
        self._set_widget(widget)
        try: sender.back_pressed.disconnect()
        except: pass
        sender.back_pressed.connect(lambda: self._child_pages.slide_in_index(0))
        self._child_pages.slide_in_index(1)


    def _set_widget(self, widget: QGridWidget | None) -> None:
        if self._current_widget: self._current_widget.setParent(None)
        if widget: self._data_frame.grid_layout.addWidget(widget, 0, 0)
        self._current_widget = widget


    def _send_data(self, *args) -> None:
        self._update_text()
        self.data_changed.emit()
#----------------------------------------------------------------------
