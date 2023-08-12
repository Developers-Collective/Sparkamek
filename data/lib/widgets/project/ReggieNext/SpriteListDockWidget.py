#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QFrame, QPushButton
from PySide6.QtCore import Qt, QSortFilterProxyModel
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
        self._root.scroll_layout.addWidget(self._list, 2, 0)

        self._proxy_model = QSortFilterProxyModel(
            self, filterKeyColumn = 1, recursiveFilteringEnabled = True
        )
        self._proxy_model.setSourceModel(self._list.model())
        self._proxy_model.setFilterCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self._list.setModel(self._proxy_model)

    def text_changed(self, text: str) -> None:
        self._proxy_model.setFilterRegularExpression(text)

    def case_sensitive_toggled(self, state: bool) -> None:
        self._proxy_model.setFilterCaseSensitivity(Qt.CaseSensitivity.CaseSensitive if state else Qt.CaseSensitivity.CaseInsensitive)

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
        try: self._sprites.add(item)
        except: pass
        self._list.add_item([str(item.id), item.name], None, [Qt.AlignmentFlag.AlignCenter, Qt.AlignmentFlag.AlignLeft])

    def _load_done(self) -> None:
        if self._sprite_list_loader_worker.isRunning():
            self._sprite_list_loader_worker.terminate()

        self._sprite_list_loader_worker = None

        self._update_buttons()

    def _load_error(self, error: str) -> None:
        self._load_done()


    def _save(self) -> None:
        pass
#----------------------------------------------------------------------
