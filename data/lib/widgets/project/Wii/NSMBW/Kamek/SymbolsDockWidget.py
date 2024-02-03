#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QFrame
from PySide6.QtCore import Qt
from data.lib.qtUtils import QScrollableGridWidget, QBaseApplication, QSavableDockWidget, QGridWidget, QIconLineEdit, QUtilsColor, QBetterListWidget, QSaveData, QNamedToggleButton, QNamedComboBox, QBetterSortFilterProxyModel, QLangData
from .compiler import FuncSymbol
#----------------------------------------------------------------------

    # Class
class SymbolsDockWidget(QSavableDockWidget):
    _search_icon = None

    _lang: QLangData = QLangData.NoTranslation()

    _neutral_color = QUtilsColor.from_hex('#aaaaaa')
    _bracket_color = QUtilsColor.from_hex('#dddddd')

    def init(app: QBaseApplication) -> None:
        SymbolsDockWidget._lang = app.get_lang_data('QMainWindow.QSlidingStackedWidget.mainMenu.projects.projectWidget.Wii.NSMBW.KamekWidget.SymbolsDockWidget')

        SymbolsDockWidget._search_icon = app.get_icon('lineedit/search', True, QSaveData.IconMode.Local)

    def __init__(self, app: QBaseApplication, name: str, icon: str, data: dict) -> None:
        super().__init__(self._lang.get('title').replace('%s', name))

        self._name = name
        self._icon = icon
        self._data = data

        self._root = QScrollableGridWidget()
        self._root.setProperty('wide', True)
        self._root.setMinimumWidth(200)
        self._root.setMinimumHeight(100)
        self._root.setFrameShape(QFrame.Shape.NoFrame)
        self._root.scroll_widget.setProperty('QDockWidget', True)
        self.setObjectName('symbols')
        self.setWidget(self._root)

        topframe = QGridWidget()
        topframe.grid_layout.setContentsMargins(0, 0, 0, 0)
        topframe.grid_layout.setSpacing(8)
        self._root.scroll_layout.addWidget(topframe, 0, 0, Qt.AlignmentFlag.AlignTop)

        topleftframe = QGridWidget()
        topleftframe.grid_layout.setContentsMargins(0, 0, 0, 0)
        topleftframe.grid_layout.setSpacing(8)
        topframe.grid_layout.addWidget(topleftframe, 0, 0, Qt.AlignmentFlag.AlignLeft)
        topleftframe.grid_layout.setColumnStretch(1, 0)

        self._search_combobox = QNamedComboBox(None, self._lang.get('QNamedComboBox.searchBy.title'))
        self._search_combobox.combo_box.addItems([
            self._lang.get('QNamedComboBox.searchBy.values.address'),
            self._lang.get('QNamedComboBox.searchBy.values.name'),
            self._lang.get('QNamedComboBox.searchBy.values.raw')
        ])
        self._search_combobox.combo_box.setCurrentIndex(1)
        self._search_combobox.combo_box.currentIndexChanged.connect(self._search_by_changed)
        topleftframe.grid_layout.addWidget(self._search_combobox, 0, 0, Qt.AlignmentFlag.AlignLeft)

        self._address_mode_combobox = QNamedComboBox(None, self._lang.get('QNamedComboBox.addressMode.title'))
        self._address_mode_combobox.combo_box.addItems([
            self._lang.get('QNamedComboBox.addressMode.values.contains'),
            self._lang.get('QNamedComboBox.addressMode.values.greaterOrEqual'),
            self._lang.get('QNamedComboBox.addressMode.values.lessOrEqual')
        ])
        self._address_mode_combobox.combo_box.setCurrentIndex(1)
        self._address_mode_combobox.combo_box.currentIndexChanged.connect(self._address_mode_changed)
        topleftframe.grid_layout.addWidget(self._address_mode_combobox, 0, 1, Qt.AlignmentFlag.AlignLeft)
        self._address_mode_combobox.setVisible(False)

        toprightframe = QGridWidget()
        toprightframe.grid_layout.setContentsMargins(0, 0, 0, 0)
        toprightframe.grid_layout.setSpacing(8)
        topframe.grid_layout.addWidget(toprightframe, 0, 1, Qt.AlignmentFlag.AlignRight)
        toprightframe.grid_layout.setColumnStretch(1, 0)

        case_sensitive_togge = QNamedToggleButton(None, self._lang.get('QNamedToggleButton.caseSensitive'), False)
        case_sensitive_togge.toggle_button.toggled.connect(self.case_sensitive_toggled)
        toprightframe.grid_layout.addWidget(case_sensitive_togge, 0, 0)

        self._searchbar = QIconLineEdit(None, self._search_icon, self._lang.get('QIconLineEdit.search'))
        self._searchbar.textChanged.connect(self.text_changed)
        toprightframe.grid_layout.addWidget(self._searchbar, 0, 1)

        self._list = QBetterListWidget(
            [
                self._lang.get('QBetterListWidget.address'),
                self._lang.get('QBetterListWidget.name'),
                self._lang.get('QBetterListWidget.raw')
            ],
            200,
            Qt.AlignmentFlag.AlignCenter
        )
        self._list.setSortingEnabled(True)
        self._list.sortByColumn(0, Qt.SortOrder.AscendingOrder)
        self._root.scroll_layout.addWidget(self._list, 1, 0)

        self._proxy_model = QBetterSortFilterProxyModel(
            self, filterKeyColumn = 1, recursiveFilteringEnabled = True
        )
        self._proxy_model.setSourceModel(self._list.model())
        self._proxy_model.setFilterCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self._list.setModel(self._proxy_model)

        self._task_is_running = False

    def text_changed(self, text: str) -> None:
        self._proxy_model.setFilterRegularExpression(text)

    def case_sensitive_toggled(self, state: bool) -> None:
        self._proxy_model.setFilterCaseSensitivity(Qt.CaseSensitivity.CaseSensitive if state else Qt.CaseSensitivity.CaseInsensitive)

    def _search_by_changed(self, index: int) -> None:
        self._address_mode_combobox.setVisible(index == 0)
        self._proxy_model.setFilterKeyColumn(index)

        if index == 0: self._address_mode_changed(self._address_mode_combobox.combo_box.currentIndex())
        else: self._address_mode_changed(0)

    def _address_mode_changed(self, index: int) -> None:
        self._proxy_model.filterAcceptsRow = lambda source_row, source_parent: self._filter_accepts_row(source_row, source_parent, index)
        self._proxy_model.invalidateFilter()

    def _filter_accepts_row(self, source_row: int, source_parent: int, index: int) -> bool:
        def try_parse_int(val: str) -> int:
            try: return int(val)
            except ValueError: pass

            try: return int(val, 16)
            except ValueError: pass

            try: return int(val, 2)
            except ValueError: pass

            try: return int(val, 8)
            except ValueError: pass

            return 0

        match index:
            case 0:
                pattern = self._searchbar.text()
                item = self._proxy_model.sourceModel().data(self._proxy_model.sourceModel().index(source_row, self._search_combobox.combo_box.currentIndex(), source_parent))

                if self._proxy_model.filterCaseSensitivity() == Qt.CaseSensitivity.CaseInsensitive:
                    pattern = pattern.lower()
                    item = item.lower()

                return pattern in item

            case 1:
                return try_parse_int(self._proxy_model.sourceModel().data(self._proxy_model.sourceModel().index(source_row, 0, source_parent))) >= try_parse_int(self._searchbar.text())

            case 2:
                return try_parse_int(self._proxy_model.sourceModel().data(self._proxy_model.sourceModel().index(source_row, 0, source_parent))) <= try_parse_int(self._searchbar.text())

        return False

    def set_symbols(self, symbols: list[FuncSymbol]) -> None:
        self._task_is_running = True

        self._list.clear()
        for symbol in symbols: self._list.add_item([f'0x{symbol.addr:08X}', symbol.name, symbol.raw], None, [Qt.AlignmentFlag.AlignCenter, Qt.AlignmentFlag.AlignLeft, Qt.AlignmentFlag.AlignLeft])

        self._task_is_running = False


    @property
    def task_is_running(self) -> bool:
        return self._task_is_running
#----------------------------------------------------------------------
