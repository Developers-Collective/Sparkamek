#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QLabel, QPushButton
from PySide6.QtCore import Qt
from data.lib.qtUtils import QBaseApplication, QNamedLineEdit, QSlidingStackedWidget, QGridWidget, QSaveData, QDragList
from ..items.Patch import Patch
from ..items.File import File
from ..items.Folder import Folder
from ..items.MemoryValue import MemoryValue
from ..items.MemorySearchValueFile import MemorySearchValueFile
from ..items.MemorySearchValue import MemorySearchValue
from ..items.MemorySearchValueFile import MemorySearchValueFile
from ..items.MemoryOcarina import MemoryOcarina
from .BaseItemData import BaseItemData
# from .PatchChildData import PatchChildData
#----------------------------------------------------------------------

    # Class
class PatchData(BaseItemData):
    type: str = 'Patch'
    child_cls: Patch = Patch

    _add_entry_icon = None

    _lang = {}

    def init(app: QBaseApplication) -> None:
        PatchData._lang = app.get_lang_data('QMainWindow.QSlidingStackedWidget.mainMenu.projects.RiivolutionWidget.WiiDiscWidget.PatchData')

        PatchData._add_entry_icon = app.get_icon('pushbutton/add.png', True, QSaveData.IconMode.Local)

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


        frame = QGridWidget()
        frame.grid_layout.setSpacing(30)
        frame.grid_layout.setContentsMargins(0, 0, 0, 0)

        self._child_pages.addWidget(frame)


        subframe = QGridWidget()
        subframe.grid_layout.setSpacing(8)
        subframe.grid_layout.setContentsMargins(0, 0, 0, 0)
        frame.grid_layout.addWidget(subframe, 0, 0)

        label = QLabel(self._lang.get_data('QLabel.generalInfo'))
        label.setProperty('h', 2)
        label.setProperty('small', True)
        subframe.grid_layout.addWidget(label, 0, 0)

        self._id_lineedit = QNamedLineEdit(None, '', self._lang.get_data('PropertyWidget.QNamedLineEdit.id'))
        self._id_lineedit.line_edit.setText(self._data.id)
        self._id_lineedit.line_edit.textChanged.connect(self._id_changed)
        subframe.grid_layout.addWidget(self._id_lineedit, 1, 0)

        subframe.grid_layout.setRowStretch(2, 1)


        subframe = QGridWidget()
        subframe.grid_layout.setSpacing(8)
        subframe.grid_layout.setContentsMargins(0, 0, 0, 0)
        frame.grid_layout.addWidget(subframe, 1, 0)

        label = QLabel(self._lang.get_data('QLabel.files'))
        label.setProperty('h', 2)
        label.setProperty('small', True)
        subframe.grid_layout.addWidget(label, 0, 0)

        self._file_draglist = QDragList()
        self._file_draglist.moved.connect(self._file_entry_moved)
        subframe.grid_layout.addWidget(self._file_draglist, 1, 0)

        self._add_file_entry_button = QPushButton(self._lang.get_data('QPushButton.addFile'))
        self._add_file_entry_button.setIcon(self._add_entry_icon)
        self._add_file_entry_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self._add_file_entry_button.setProperty('color', 'main')
        self._add_file_entry_button.clicked.connect(self._add_file_entry)
        subframe.grid_layout.addWidget(self._add_file_entry_button, 2, 0)
        self._add_file_entry_button.setEnabled(False)

        subframe.grid_layout.setRowStretch(3, 1)

        frame.grid_layout.setRowStretch(2, 1)


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
                # fd = FileData(file, self._path)
                # fd.data_changed.connect(self._send_data)
                # fd.edited.connect(self._entry_selected)
                # fd.deleted.connect(self._delete_file_entry)
                # self._file_draglist.add_item(fd)
                pass

        self._disable_send = False


    def _update_text(self) -> None:
        s = self._lang.get_data('QLabel.text').replace(
            '%s', self._data.id, 1
        ).replace(
            '%s', str(
                len(self._data.file_children) + len(self._data.folder_children) + len(self._data.savegame_children) + len(self._data.memory_children)
            ), 1
        )
        self._patchid_label.setText(s)
        self._id_lineedit.line_edit.setText(self._data.id)


    def _id_changed(self, text: str) -> None:
        if not text: return

        self._data.id = text
        self._update_text()
        self.data_changed.emit()

    def _file_entry_moved(self, old_index: int, new_index: int) -> None:
        self._data.file_children.insert(new_index, self._data.file_children.pop(old_index))
        self._send_data()

    def _add_file_entry(self) -> None:
        f = File.create()
        self._data.file_children.append(f)

        # fd = FileData(f, self._path)
        # fd.data_changed.connect(self._send_data)
        # fd.deleted.connect(self._delete_file_entry)
        # fd.edited.connect(self._entry_selected)
        # self._file_draglist.add_item(fd)

        self._send_data()

    # def _delete_file_entry(self, item: FileData) -> None:
    #     if self._data is None: return

    #     self._data.file_children.remove(item.data)
    #     item.setParent(None)
    #     item.deleteLater()

    #     self._child_pages.slide_in_index(0)

    #     self._send_data()

    # def _entry_selected(self, sender: PatchChildData, widget: QGridWidget | None) -> None:
    #     self._set_widget(widget)
    #     try: sender.back_pressed.disconnect()
    #     except: pass
    #     sender.back_pressed.connect(lambda: self._child_pages.slide_in_index(0))
    #     self._child_pages.slide_in_index(1)


    def _set_widget(self, widget: QGridWidget | None) -> None:
        if self._current_widget: self._current_widget.setParent(None)
        if widget: self._data_frame.grid_layout.addWidget(widget, 0, 0)
        self._current_widget = widget


    def _send_data(self, *args) -> None:
        self._update_text()
        self.data_changed.emit()
#----------------------------------------------------------------------
