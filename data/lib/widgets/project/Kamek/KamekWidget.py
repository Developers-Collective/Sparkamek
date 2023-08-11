#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QLabel, QPushButton, QDockWidget
from PySide6.QtCore import Qt, QSortFilterProxyModel
from data.lib.qtUtils import QBaseApplication, QBetterListWidget, QSaveData, QGridWidget, QIconLineEdit, QNamedComboBox, QNamedToggleButton
from ..SubProjectWidgetBase import SubProjectWidgetBase
from data.lib.widgets.ProjectKeys import ProjectKeys
from .CompilerDockWidget import CompilerDockWidget
from .SymbolsDockWidget import SymbolsDockWidget
from .SpritesAndActorsWorker import SpritesAndActorsWorker
import yaml, os
#----------------------------------------------------------------------

    # Class
class KamekWidget(SubProjectWidgetBase):
    type: ProjectKeys = ProjectKeys.Kamek

    _refresh_icon = None
    _search_icon = None

    _lang = {}

    def init(app: QBaseApplication) -> None:
        KamekWidget._lang = app.get_lang_data('QMainWindow.QSlidingStackedWidget.mainMenu.projects.KamekWidget')
        KamekWidget._refresh_icon = app.get_icon('pushbutton/refresh.png', True, QSaveData.IconMode.Local)
        KamekWidget._search_icon = app.get_icon('lineedit/search', True, QSaveData.IconMode.Local)

        CompilerDockWidget.init(app)
        SymbolsDockWidget.init(app)
        SpritesAndActorsWorker.init(app)

    def __init__(self, app: QBaseApplication, name: str, icon: str, data: dict) -> None:
        super().__init__(app, data)

        self.scroll_layout.setSpacing(20)

        dockwidgets = data.get('dockwidgets', {})

        self._compiler_dock_widget = CompilerDockWidget(app, name, icon, data)
        self._symbols_dock_widget = SymbolsDockWidget(app, name, icon, data)

        if 'compiler' in dockwidgets: self._compiler_dock_widget.load_dict(self, dockwidgets['compiler'])
        else: self.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, self._compiler_dock_widget)

        if 'symbols' in dockwidgets: self._symbols_dock_widget.load_dict(self, dockwidgets['symbols'])
        else: self.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, self._symbols_dock_widget)

        if 'compiler' not in dockwidgets and 'symbols' not in dockwidgets:
            self.tabifyDockWidget(self._compiler_dock_widget, self._symbols_dock_widget)
            self._compiler_dock_widget.raise_()

        self._compiler_dock_widget.new_symbols.connect(self._symbols_dock_widget.set_symbols)


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
        # self._refresh_sprites_and_actors()


    @property
    def task_is_running(self) -> bool:
        return self._compiler_dock_widget.task_is_running or self._symbols_dock_widget.task_is_running or self._sprites_and_actors_worker is not None


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

    def _save_dock_widgets(self) -> dict:
        if self._sprites_and_actors_worker is not None:
            self._sprites_and_actors_worker.terminate()

        self._compiler_dock_widget.terminate_task()

        dockwidgets = {}

        for dw in self.findChildren(QDockWidget):
            dockwidgets[dw.objectName()] = dw.to_dict()

        return dockwidgets

    def reset_dock_widgets(self) -> None:
        for dw in [self._compiler_dock_widget, self._symbols_dock_widget]:
            dw.setVisible(True)
            dw.setFloating(False)

        self.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, self._compiler_dock_widget)
        self.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, self._symbols_dock_widget)

        if self._compiler_dock_widget not in self.tabifiedDockWidgets(self._symbols_dock_widget): self.tabifyDockWidget(self._symbols_dock_widget, self._compiler_dock_widget)
#----------------------------------------------------------------------
