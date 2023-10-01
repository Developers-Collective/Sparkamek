#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QFrame, QPushButton, QLabel
from PySide6.QtCore import Qt, QSortFilterProxyModel
from data.lib.qtUtils import QScrollableGridWidget, QBaseApplication, QSavableDockWidget, QSaveData, QGridWidget, QNamedToggleButton, QUtilsColor, QIconLineEdit, QNamedComboBox, QBetterListWidget
from .SpritesAndActorsWorker import SpritesAndActorsWorker
#----------------------------------------------------------------------

    # Class
class SpritesAndActorsDockWidget(QSavableDockWidget):
    _refresh_icon = None
    _search_icon = None

    _lang = {}

    def init(app: QBaseApplication) -> None:
        SpritesAndActorsDockWidget._lang = app.get_lang_data('QMainWindow.QSlidingStackedWidget.mainMenu.projects.KamekWidget.SpritesAndActorsDockWidget')
        SpritesAndActorsDockWidget._refresh_icon = app.get_icon('pushbutton/refresh.png', True, QSaveData.IconMode.Local)
        SpritesAndActorsDockWidget._search_icon = app.get_icon('lineedit/search', True, QSaveData.IconMode.Local)

        SpritesAndActorsWorker.init(app)

    def __init__(self, app: QBaseApplication, name: str, icon: str, data: dict) -> None:
        super().__init__(self._lang.get_data('title').replace('%s', name))

        self._name = name
        self._icon = icon
        self._data = data
        self._path = data['path']

        self._root = QScrollableGridWidget()
        self._root.setProperty('wide', True)
        self._root.setMinimumWidth(200)
        self._root.setMinimumHeight(100)
        self._root.setFrameShape(QFrame.Shape.NoFrame)
        self._root.scroll_widget.setProperty('QDockWidget', True)
        self.setObjectName('spritesAndActors')
        self.setWidget(self._root)

        topframe = QGridWidget()
        topframe.grid_layout.setContentsMargins(0, 0, 0, 0)
        topframe.grid_layout.setSpacing(8)
        self._root.scroll_layout.addWidget(topframe, 0, 0, Qt.AlignmentFlag.AlignTop)

        label = QLabel(self._lang.get_data('QLabel.spritesAndActors'))
        label.setProperty('h', 2)
        label.setProperty('small', True)
        topframe.grid_layout.addWidget(label, 0, 0, Qt.AlignmentFlag.AlignLeft)

        self._refresh_sprites_and_actors_button = QPushButton()
        self._refresh_sprites_and_actors_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self._refresh_sprites_and_actors_button.setProperty('color', 'main')
        self._refresh_sprites_and_actors_button.setIcon(self._refresh_icon)
        self._refresh_sprites_and_actors_button.clicked.connect(self._refresh_sprites_and_actors)
        topframe.grid_layout.addWidget(self._refresh_sprites_and_actors_button, 0, 1, Qt.AlignmentFlag.AlignRight)


        subtopframe = QGridWidget()
        subtopframe.grid_layout.setContentsMargins(0, 0, 0, 0)
        subtopframe.grid_layout.setSpacing(8)
        self._root.scroll_layout.addWidget(subtopframe, 1, 0, Qt.AlignmentFlag.AlignTop)

        search_combobox = QNamedComboBox(None, self._lang.get_data('QNamedComboBox.searchBy.title'))
        search_combobox.combo_box.addItems([
            self._lang.get_data('QNamedComboBox.searchBy.values.actorName'),
            self._lang.get_data('QNamedComboBox.searchBy.values.actorID'),
            self._lang.get_data('QNamedComboBox.searchBy.values.spriteID'),
            self._lang.get_data('QNamedComboBox.searchBy.values.replaceOrNew')
        ])
        search_combobox.combo_box.setCurrentIndex(0)
        search_combobox.combo_box.currentIndexChanged.connect(self._search_by_changed)
        subtopframe.grid_layout.addWidget(search_combobox, 0, 0, Qt.AlignmentFlag.AlignLeft)

        subtoprightframe = QGridWidget()
        subtoprightframe.grid_layout.setContentsMargins(0, 0, 0, 0)
        subtoprightframe.grid_layout.setSpacing(8)
        subtopframe.grid_layout.addWidget(subtoprightframe, 0, 1, Qt.AlignmentFlag.AlignRight)
        subtoprightframe.grid_layout.setColumnStretch(1, 0)

        case_sensitive_togge = QNamedToggleButton(None, self._lang.get_data('QNamedToggleButton.caseSensitive'), False)
        case_sensitive_togge.toggle_button.toggled.connect(self.case_sensitive_toggled)
        subtoprightframe.grid_layout.addWidget(case_sensitive_togge, 0, 0)

        self._searchbar = QIconLineEdit(None, self._search_icon, self._lang.get_data('QIconLineEdit.search'))
        self._searchbar.textChanged.connect(self.text_changed)
        subtoprightframe.grid_layout.addWidget(self._searchbar, 0, 1)


        self._sprite_list = QBetterListWidget(
            [
                self._lang.get_data('QBetterListWidget.actorName'),
                self._lang.get_data('QBetterListWidget.actorID'),
                self._lang.get_data('QBetterListWidget.spriteID'),
                self._lang.get_data('QBetterListWidget.replaceOrNew')
            ],
            170,
            Qt.AlignmentFlag.AlignCenter
        )
        self._sprite_list.setSortingEnabled(True)
        self._sprite_list.sortByColumn(1, Qt.SortOrder.AscendingOrder)
        self._root.scroll_layout.addWidget(self._sprite_list, 2, 0)

        self._proxy_model = QSortFilterProxyModel(
            self, filterKeyColumn = 0, recursiveFilteringEnabled = True
        )
        self._proxy_model.setSourceModel(self._sprite_list.model())
        self._proxy_model.setFilterCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self._sprite_list.setModel(self._proxy_model)

        self._sprites_and_actors_worker: SpritesAndActorsWorker = None


    @property
    def task_is_running(self) -> bool:
        return self._sprites_and_actors_worker is not None


    def text_changed(self, text: str) -> None:
        self._proxy_model.setFilterRegularExpression(text)

    def case_sensitive_toggled(self, state: bool) -> None:
        self._proxy_model.setFilterCaseSensitivity(Qt.CaseSensitivity.CaseSensitive if state else Qt.CaseSensitivity.CaseInsensitive)

    def _search_by_changed(self, index: int) -> None:
        self._proxy_model.setFilterKeyColumn(index)


    def _refresh_sprites_and_actors(self) -> None:
        self._sprite_list.clear()

        if self._sprites_and_actors_worker is not None:
            self._sprites_and_actors_worker.terminate()

        self._sprites_and_actors_worker = SpritesAndActorsWorker(self._path)
        self._sprites_and_actors_worker.done.connect(self._refresh_sprites_and_actors_done)
        self._sprites_and_actors_worker.error.connect(self._refresh_sprites_and_actors_error)
        self._sprites_and_actors_worker.found_item.connect(self._refresh_sprites_and_actors_found_item)
        self._sprites_and_actors_worker.start()

    def _refresh_sprites_and_actors_done(self) -> None:
        if self._sprites_and_actors_worker.isRunning():
            self._sprites_and_actors_worker.terminate()

        self._sprites_and_actors_worker = None

    def _refresh_sprites_and_actors_error(self, error: str) -> None:
        self._refresh_sprites_and_actors_done()
        print(error)

    def _refresh_sprites_and_actors_found_item(self, actor_name: str, actor_id: int, sprite_id: int, replace: bool) -> None:
        self._sprite_list.add_item([actor_name, str(actor_id), str(sprite_id) if sprite_id > -1 else '-', self._lang.get_data('QBetterListWidget.replace') if replace else self._lang.get_data('QBetterListWidget.new')], None, [Qt.AlignmentFlag.AlignLeft, Qt.AlignmentFlag.AlignCenter, Qt.AlignmentFlag.AlignCenter, Qt.AlignmentFlag.AlignCenter])

    def terminate_task(self) -> None:
        if self._sprites_and_actors_worker is not None:
            self._sprites_and_actors_worker.terminate()
            self._sprites_and_actors_worker = None
#----------------------------------------------------------------------
