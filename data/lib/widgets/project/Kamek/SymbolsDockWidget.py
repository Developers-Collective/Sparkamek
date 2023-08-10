#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QFrame, QPushButton
from PySide6.QtCore import Qt, QSortFilterProxyModel
from data.lib.qtUtils import QScrollableGridWidget, QBaseApplication, QSavableDockWidget, QGridWidget, QIconLineEdit, QUtilsColor, QBetterListWidget, QSaveData, QNamedToggleButton, QNamedComboBox
from .compiler import FuncSymbol
#----------------------------------------------------------------------

    # Class
class SymbolsDockWidget(QSavableDockWidget):
    _search_icon = None

    _lang = {}

    _neutral_color = QUtilsColor.from_hex('#aaaaaa')
    _bracket_color = QUtilsColor.from_hex('#dddddd')

    def init(app: QBaseApplication) -> None:
        SymbolsDockWidget._lang = app.get_lang_data('QMainWindow.QSlidingStackedWidget.mainMenu.projects.KamekWidget.SymbolsDockWidget')

        SymbolsDockWidget._search_icon = app.get_icon('lineedit/search', True, QSaveData.IconMode.Local)

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
        self.setObjectName('symbols')
        self.setWidget(self._root)

        topframe = QGridWidget()
        topframe.grid_layout.setContentsMargins(0, 0, 0, 0)
        topframe.grid_layout.setSpacing(8)
        self._root.scroll_layout.addWidget(topframe, 0, 0, Qt.AlignmentFlag.AlignTop)

        search_combobox = QNamedComboBox(None, self._lang.get_data('QNamedComboBox.searchBy.title'))
        search_combobox.combo_box.addItems([
            self._lang.get_data('QNamedComboBox.searchBy.values.address'),
            self._lang.get_data('QNamedComboBox.searchBy.values.name'),
            self._lang.get_data('QNamedComboBox.searchBy.values.raw')
        ])
        search_combobox.combo_box.setCurrentIndex(1)
        search_combobox.combo_box.currentIndexChanged.connect(self._search_by_changed)
        topframe.grid_layout.addWidget(search_combobox, 0, 0, Qt.AlignmentFlag.AlignLeft)

        toprightframe = QGridWidget()
        toprightframe.grid_layout.setContentsMargins(0, 0, 0, 0)
        toprightframe.grid_layout.setSpacing(8)
        topframe.grid_layout.addWidget(toprightframe, 0, 1, Qt.AlignmentFlag.AlignRight)
        toprightframe.grid_layout.setColumnStretch(1, 0)

        case_sensitive_togge = QNamedToggleButton(None, self._lang.get_data('QNamedToggleButton.caseSensitive'), False)
        case_sensitive_togge.toggle_button.toggled.connect(self.case_sensitive_toggled)
        toprightframe.grid_layout.addWidget(case_sensitive_togge, 0, 0)

        self._searchbar = QIconLineEdit(None, self._search_icon, self._lang.get_data('QIconLineEdit.search'))
        self._searchbar.textChanged.connect(self.text_changed)
        toprightframe.grid_layout.addWidget(self._searchbar, 0, 1)

        self._list = QBetterListWidget(
            [
                self._lang.get_data('QBetterListWidget.address'),
                self._lang.get_data('QBetterListWidget.name'),
                self._lang.get_data('QBetterListWidget.raw')
            ],
            200,
            Qt.AlignmentFlag.AlignCenter
        )
        self._list.setSortingEnabled(True)
        self._list.sortByColumn(0, Qt.SortOrder.AscendingOrder)
        self._root.scroll_layout.addWidget(self._list, 1, 0)

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

    def set_symbols(self, symbols: list[FuncSymbol]) -> None:
        self._list.clear()

        for symbol in symbols: self._list.add_item([f'0x{symbol.addr:08X}', symbol.name, symbol.raw], None, Qt.AlignmentFlag.AlignLeft)
#----------------------------------------------------------------------
