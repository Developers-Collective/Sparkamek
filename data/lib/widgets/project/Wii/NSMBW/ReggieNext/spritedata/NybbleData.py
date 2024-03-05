#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QLabel
from PySide6.QtCore import Signal
from data.lib.QtUtils import QGridWidget, QBaseApplication, QNamedComboBox, QLangData
from ..sprites.NybbleRange import NybbleRange
from ..sprites.Nybble import Nybble
#----------------------------------------------------------------------

    # Class
class NybbleData(QGridWidget):
    data_changed = Signal()

    _lang: QLangData = QLangData.NoTranslation()

    def init(app: QBaseApplication) -> None:
        NybbleData._lang = app.get_lang_data('QMainWindow.QSlidingStackedWidget.mainMenu.projects.projectWidget.Wii.NSMBW.ReggieNextWidget.SpriteWidget.NybbleData')

    def __init__(self, data: NybbleRange) -> None:
        super().__init__()

        self._data = data


        self.grid_layout.setContentsMargins(0, 0, 0, 0)
        self.grid_layout.setSpacing(8)
        self.grid_layout.setColumnStretch(6, 1)

        self._first_nybble_combobox = QNamedComboBox(None, self._lang.get('QNamedComboBox.firstNybble'))
        self._first_nybble_combobox.combo_box.addItems([str(i) for i in range(1, 17)])
        self._first_nybble_combobox.combo_box.setCurrentIndex(self._data.start.n - 1)
        self._first_nybble_combobox.combo_box.currentIndexChanged.connect(self._first_nybble_changed)
        self.grid_layout.addWidget(self._first_nybble_combobox, 0, 0)

        label = QLabel('.')
        label.setProperty('brighttitle', True)
        self.grid_layout.addWidget(label, 0, 1)

        self._first_nybblebit_combobox = QNamedComboBox(None, self._lang.get('QNamedComboBox.firstNybbleBit'))
        self._first_nybblebit_combobox.combo_box.addItems(['None'] + [str(i) for i in range(1, 5)])
        self._first_nybblebit_combobox.combo_box.setCurrentIndex((self._data.start.b + 1) if self._data.start.b is not None else 0)
        self._first_nybblebit_combobox.combo_box.currentIndexChanged.connect(self._first_nybblebit_changed)
        self.grid_layout.addWidget(self._first_nybblebit_combobox, 0, 2)

        label = QLabel('-')
        label.setProperty('brighttitle', True)
        self.grid_layout.addWidget(label, 0, 3)

        self._last_nybble_combobox = QNamedComboBox(None, self._lang.get('QNamedComboBox.lastNybble'))
        self._last_nybble_combobox.combo_box.addItems(['None'] + [str(i) for i in range(1, 17)])
        if self._data.end is not None: self._last_nybble_combobox.combo_box.setCurrentIndex(self._data.end.n if self._data.end.n is not None else 0)
        self._last_nybble_combobox.combo_box.currentIndexChanged.connect(self._last_nybble_changed)
        self.grid_layout.addWidget(self._last_nybble_combobox, 0, 4)

        label = QLabel('.')
        label.setProperty('brighttitle', True)
        self.grid_layout.addWidget(label, 0, 5)

        self._last_nybblebit_combobox = QNamedComboBox(None, self._lang.get('QNamedComboBox.lastNybbleBit'))
        self._last_nybblebit_combobox.combo_box.addItems(['None'] + [str(i) for i in range(1, 5)])
        if self._data.end is not None: self._last_nybblebit_combobox.combo_box.setCurrentIndex((self._data.end.b + 1) if self._data.end.b is not None else 0)
        self._last_nybblebit_combobox.combo_box.currentIndexChanged.connect(self._last_nybblebit_changed)
        self.grid_layout.addWidget(self._last_nybblebit_combobox, 0, 6)



    @property
    def data(self) -> NybbleRange:
        return self._data


    def _fix_nybbles(self) -> None:
        fn = self._first_nybble_combobox.combo_box.currentIndex()
        fnb = self._first_nybblebit_combobox.combo_box.currentIndex() - 1
        ln = self._last_nybble_combobox.combo_box.currentIndex() - 1
        lnb = self._last_nybblebit_combobox.combo_box.currentIndex() - 1

        if ln == -1: lnb = -1

        if ln >= 0:
            if fn > ln:
                fn, ln = ln, fn

            if (fn == ln) and (fnb > lnb):
                fnb, lnb = lnb, fnb

        self._first_nybble_combobox.combo_box.setCurrentIndex(fn)
        self._first_nybblebit_combobox.combo_box.setCurrentIndex(fnb + 1)
        self._last_nybble_combobox.combo_box.setCurrentIndex(ln + 1)
        self._last_nybblebit_combobox.combo_box.setCurrentIndex(lnb + 1)

        self._data.start.n = fn + 1
        self._data.start.b = fnb if fnb >= 0 else None

        if ln >= 0:
            s = f'{ln + 1}'
            if lnb >= 0: s += f'.{lnb + 1}'
            self._data.end = Nybble(s)

        else:
            self._data.end = None

        self.data_changed.emit()

    def _first_nybble_changed(self, index: int) -> None:
        self._fix_nybbles()

    def _first_nybblebit_changed(self, index: int) -> None:
        self._fix_nybbles()

    def _last_nybble_changed(self, index: int) -> None:
        self._fix_nybbles()

    def _last_nybblebit_changed(self, index: int) -> None:
        self._fix_nybbles()
#----------------------------------------------------------------------
