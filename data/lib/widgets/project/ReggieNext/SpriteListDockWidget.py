#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QFrame, QPushButton
from PySide6.QtCore import Qt, QSortFilterProxyModel, Signal
from data.lib.qtUtils import QScrollableGridWidget, QBaseApplication, QSavableDockWidget, QGridWidget, QIconLineEdit, QUtilsColor, QBetterListWidget, QSaveData
from .SpriteListLoaderWorker import SpriteListLoaderWorker
from .sprites import *
#----------------------------------------------------------------------

    # Class
class SpriteListDockWidget(QSavableDockWidget):
    _search_icon = None
    _load_icon = None
    _save_icon = None

    _lang = {}

    _neutral_color = QUtilsColor.from_hex('#aaaaaa')
    _bracket_color = QUtilsColor.from_hex('#dddddd')

    _list_alignment = [Qt.AlignmentFlag.AlignCenter, Qt.AlignmentFlag.AlignLeft]

    selected_sprite_changed = Signal(Sprite or None, Sprite or None)

    def init(app: QBaseApplication) -> None:
        SpriteListDockWidget._lang = app.get_lang_data('QMainWindow.QSlidingStackedWidget.mainMenu.projects.ReggieNextWidget.SpriteListDockWidget')

        SpriteListDockWidget._search_icon = app.get_icon('lineedit/search.png', True, QSaveData.IconMode.Local)
        SpriteListDockWidget._load_icon = app.get_icon('pushbutton/load.png', True, QSaveData.IconMode.Local)
        SpriteListDockWidget._save_icon = app.get_icon('pushbutton/save.png', True, QSaveData.IconMode.Local)

        SpriteListLoaderWorker.init(app)

    def __init__(self, app: QBaseApplication, name: str, icon: str, data: dict) -> None:
        super().__init__(self._lang.get_data('title').replace('%s', name))

        self._name = name
        self._icon = icon
        self._data = data

        self._root = QScrollableGridWidget()
        self._root.setProperty('wide', True)
        self._root.setMinimumWidth(200)
        self._root.setMinimumHeight(100)
        self._root.setFrameShape(QFrame.Shape.NoFrame)
        self._root.scroll_widget.setProperty('QDockWidget', True)
        self.setObjectName('spriteList')
        self.setWidget(self._root)

        self._sprite_list_loader_worker = None

        self._sprites = Sprites()


        topframe = QGridWidget()
        topframe.grid_layout.setContentsMargins(0, 0, 0, 0)
        topframe.grid_layout.setSpacing(8)
        self._root.scroll_layout.addWidget(topframe, 0, 0, Qt.AlignmentFlag.AlignTop)

        self._load_button = QPushButton(self._lang.get_data('QPushButton.load'))
        self._load_button.setIcon(self._load_icon)
        self._load_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self._load_button.setProperty('icon-padding', True)
        self._load_button.setProperty('color', 'main')
        self._load_button.clicked.connect(self._load)
        topframe.grid_layout.addWidget(self._load_button, 0, 0, Qt.AlignmentFlag.AlignLeft)

        self._save_button = QPushButton(self._lang.get_data('QPushButton.save'))
        self._save_button.setIcon(self._save_icon)
        self._save_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self._save_button.setProperty('icon-padding', True)
        self._save_button.setProperty('color', 'main')
        self._save_button.clicked.connect(self._save)
        topframe.grid_layout.addWidget(self._save_button, 0, 1, Qt.AlignmentFlag.AlignRight)


        self._searchbar = QIconLineEdit(None, self._search_icon, self._lang.get_data('QIconLineEdit.search'))
        self._searchbar.textChanged.connect(self.text_changed)
        self._root.scroll_layout.addWidget(self._searchbar, 1, 0, Qt.AlignmentFlag.AlignTop)


        self._list = QBetterListWidget(
            [
                self._lang.get_data('QBetterListWidget.spriteID'),
                self._lang.get_data('QBetterListWidget.name')
            ],
            100,
            Qt.AlignmentFlag.AlignCenter
        )
        self._list.setSortingEnabled(True)
        self._list.sortByColumn(0, Qt.SortOrder.AscendingOrder)
        self._list.item_selection_changed.connect(self._sprite_selection_changed)
        self._root.scroll_layout.addWidget(self._list, 2, 0)

        self._proxy_model = QSortFilterProxyModel(
            self, filterKeyColumn = 1, recursiveFilteringEnabled = True
        )
        self._proxy_model.setSourceModel(self._list.model())
        self._proxy_model.setFilterCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self._list.setModel(self._proxy_model)

    def text_changed(self, text: str) -> None:
        self._proxy_model.setFilterRegularExpression(text)

    def _search_by_changed(self, index: int) -> None:
        self._proxy_model.setFilterKeyColumn(index)


    @property
    def task_is_running(self) -> bool:
        return self._sprite_list_loader_worker is not None

    def terminate_task(self) -> None:
        if self._sprite_list_loader_worker is not None:
            self._sprite_list_loader_worker.terminate()
            self._sprite_list_loader_worker = None

    
    def _update_buttons(self) -> None:
        self._load_button.setEnabled(not self.task_is_running)
        self._save_button.setEnabled(not self.task_is_running)


    def _load(self) -> None:
        self._list.clear()

        if self._sprite_list_loader_worker:
            if self._sprite_list_loader_worker.isRunning():
                self._sprite_list_loader_worker.terminate()

        self._sprite_list_loader_worker = SpriteListLoaderWorker(self._data['path'] + '/spritedata.xml')
        self._sprite_list_loader_worker.done.connect(self._load_done)
        self._sprite_list_loader_worker.error.connect(self._load_error)
        self._sprite_list_loader_worker.found_item.connect(self._load_item)
        self._update_buttons()

        self._sprite_list_loader_worker.start()

    def _load_item(self, item: Sprite) -> None:
        try:
            self._sprites.add(item)
            self._list.add_item([str(item.id), item.name], None, self._list_alignment)
        except: pass

    def _load_done(self) -> None:
        if self._sprite_list_loader_worker.isRunning():
            self._sprite_list_loader_worker.terminate()

        self._sprite_list_loader_worker = None

        self._update_buttons()

    def _load_error(self, error: str) -> None:
        self._load_done()


    def update_sprite(self, prev_info: tuple[int, str], sprite: Sprite) -> None:
        if prev_info[0] == sprite.id:
            if self._sprites.get_by_id(prev_info[0]):
                self._sprites.replace_by_id(prev_info[0], sprite)

                index = self._list.index((str(prev_info[0]), prev_info[1]))
                self._list.replace_item(index, [str(sprite.id), sprite.name], None, self._list_alignment)

            else:
                self._sprites.add(sprite)
                self._list.add_item([str(sprite.id), sprite.name], None, self._list_alignment)

        else:
            if prev_sprite := self._sprites.get_by_id(prev_info[0]):
                self._sprites.remove_by_id(prev_sprite.id)

                index = self._list.index((str(prev_sprite.id), prev_sprite.name))
                self._list.remove_item(index)

            if existing_sprite := self._sprites.get_by_id(sprite.id):
                self._sprites.replace_by_id(existing_sprite.id, sprite)

                index = self._list.index((str(existing_sprite.id), existing_sprite.name))
                # load_next_sprite = False
                # if self._list.get_selected_row() == index and index != -1: load_next_sprite = True
                self._list.replace_item(index, [str(sprite.id), sprite.name], None, self._list_alignment)
                # if load_next_sprite:
                #     self._list.select(index)
                #     print('should be:', self._list.get_item(index))

            else:
                self._sprites.add(sprite)
                self._list.add_item([str(sprite.id), sprite.name], None, self._list_alignment)


    def delete_sprite(self, data: tuple[int, str]) -> None:
        if self._sprites.get_by_id(data[0]):
            self._sprites.remove_by_id(data[0])

            index = self._list.index((str(data[0]), data[1]))
            self._list.remove_item(index)


    def deselect_sprite(self) -> None:
        self._list.clearSelection()


    def _save(self) -> None:
        pass


    def _sprite_selection_changed(self, selected: tuple[str, str], deselected: tuple[str, str]) -> None:
        if deselected:
            deselected_sprite = self._sprites.get_by_id(int(deselected[0]))

        if selected:
            selected_sprite = self._sprites.get_by_id(int(selected[0])).copy()

        self.selected_sprite_changed.emit(selected_sprite if selected else None, deselected_sprite if deselected else None)
#----------------------------------------------------------------------
