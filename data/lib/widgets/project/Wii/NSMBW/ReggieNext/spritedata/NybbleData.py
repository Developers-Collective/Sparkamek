#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QLabel
from PySide6.QtCore import Signal
from enum import Flag
from data.lib.QtUtils import QGridWidget, QBaseApplication, QNamedComboBox, QLangData, QNamedSpinBox
from ..sprites.NybbleRange import NybbleRange
from ..sprites.Nybble import Nybble
from ..sprites.BaseItem import BaseItem
from ..sprites.ReqNybble import ReqNybble
#----------------------------------------------------------------------

    # Class
class NybbleData(QGridWidget):
    class Type(Flag):
        None_ = 0

        Nybble = 1 << 0
        Bit = 1 << 1
        Block = 1 << 2

        All = Nybble | Bit | Block


    data_changed = Signal()

    _lang: QLangData = QLangData.NoTranslation()

    def init(app: QBaseApplication) -> None:
        NybbleData._lang = app.get_lang_data('QMainWindow.QSlidingStackedWidget.mainMenu.projects.projectWidget.Wii.NSMBW.ReggieNextWidget.SpriteWidget.NybbleData')

    def __init__(self, data: BaseItem | ReqNybble, type: Type = Type.All) -> None:
        super().__init__()

        self._data = data
        self._type = type

        self.grid_layout.setContentsMargins(0, 0, 0, 0)
        self.grid_layout.setSpacing(16)

        self._nybble_grid = QGridWidget()
        self._nybble_grid.grid_layout.setContentsMargins(0, 0, 0, 0)
        self._nybble_grid.grid_layout.setSpacing(8)
        self._nybble_grid.grid_layout.setColumnStretch(6, 1)
        self.grid_layout.addWidget(self._nybble_grid, 0, 0)

        self._first_nybble_combobox = QNamedComboBox(None, self._lang.get('QNamedComboBox.firstNybble'))
        self._nybble_grid.grid_layout.addWidget(self._first_nybble_combobox, 0, 0)

        label = QLabel('.')
        label.setProperty('brighttitle', True)
        self._nybble_grid.grid_layout.addWidget(label, 0, 1)

        self._first_nybblebit_combobox = QNamedComboBox(None, self._lang.get('QNamedComboBox.firstNybbleBit'))
        self._first_nybblebit_combobox.combo_box.addItems(['None'] + [str(i) for i in range(1, 5)])
        self._first_nybblebit_combobox.combo_box.currentIndexChanged.connect(self._first_nybblebit_changed)
        self._nybble_grid.grid_layout.addWidget(self._first_nybblebit_combobox, 0, 2)

        label = QLabel('-')
        label.setProperty('brighttitle', True)
        self._nybble_grid.grid_layout.addWidget(label, 0, 3)

        self._last_nybble_combobox = QNamedComboBox(None, self._lang.get('QNamedComboBox.lastNybble'))
        self._nybble_grid.grid_layout.addWidget(self._last_nybble_combobox, 0, 4)

        label = QLabel('.')
        label.setProperty('brighttitle', True)
        self._nybble_grid.grid_layout.addWidget(label, 0, 5)

        self._last_nybblebit_combobox = QNamedComboBox(None, self._lang.get('QNamedComboBox.lastNybbleBit'))
        self._last_nybblebit_combobox.combo_box.addItems(['None'] + [str(i) for i in range(1, 5)])
        self._last_nybblebit_combobox.combo_box.currentIndexChanged.connect(self._last_nybblebit_changed)
        self._nybble_grid.grid_layout.addWidget(self._last_nybblebit_combobox, 0, 6)


        self._block_spinbox = QNamedSpinBox(None, self._lang.get('QNamedSpinBox.block'))
        self._block_spinbox.spin_box.setMinimum(0)
        self._block_spinbox.spin_box.setMaximum(255)
        self._block_spinbox.spin_box.setValue(self._data.block if self._data.block else 0)
        self._block_spinbox.spin_box.valueChanged.connect(self._block_changed)
        self.grid_layout.addWidget(self._block_spinbox, 0, 1)
        self._block_spinbox.setVisible(False)

        self._rebuild_nybbles(self.extended)



    @property
    def data(self) -> NybbleRange:
        return self._data


    @property
    def extended(self) -> bool:
        return self._data.extended


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

        self._data.nybbles.start.n = fn + 1
        self._data.nybbles.start.b = fnb if fnb >= 0 else None

        if ln >= 0:
            s = f'{ln + 1}'
            if lnb >= 0: s += f'.{lnb + 1}'
            self._data.nybbles.end = Nybble(s)

        else:
            self._data.nybbles.end = None

        self.data_changed.emit()

    def _first_nybble_changed(self, index: int) -> None:
        self._fix_nybbles()

    def _first_nybblebit_changed(self, index: int) -> None:
        self._fix_nybbles()

    def _last_nybble_changed(self, index: int) -> None:
        self._fix_nybbles()

    def _last_nybblebit_changed(self, index: int) -> None:
        self._fix_nybbles()


    def _rebuild_nybbles(self, show_block: bool) -> None:
        self._first_nybblebit_combobox.combo_box.blockSignals(True)
        self._last_nybblebit_combobox.combo_box.blockSignals(True)

        self._first_nybble_combobox.deleteLater()

        self._first_nybble_combobox = QNamedComboBox(None, self._lang.get('QNamedComboBox.firstNybble'))
        self._first_nybble_combobox.combo_box.addItems([str(i) for i in range(1, (9 if self.extended and self._data.block > 0 else 17))])
        self._nybble_grid.grid_layout.addWidget(self._first_nybble_combobox, 0, 0)

        if not (self._type & NybbleData.Type.Nybble):
            self._first_nybble_combobox.setCurrentIndex(0)
            self._first_nybble_combobox.setDisabled(True)

        elif self._data.nybbles.start is not None:
            self._first_nybble_combobox.combo_box.setCurrentIndex(self._data.nybbles.start.n - 1)

        else:
            self._first_nybble_combobox.combo_box.setCurrentIndex(0)

        self._last_nybble_combobox.deleteLater()

        self._last_nybble_combobox = QNamedComboBox(None, self._lang.get('QNamedComboBox.lastNybble'))
        self._last_nybble_combobox.combo_box.addItems(['None'] + [str(i) for i in range(1, (9 if self.extended and self._data.block > 0 else 17))])
        self._nybble_grid.grid_layout.addWidget(self._last_nybble_combobox, 0, 4)

        if not (self._type & NybbleData.Type.Nybble):
            self._last_nybble_combobox.setCurrentIndex(self._last_nybble_combobox.combo_box.count() - 1)
            self._last_nybble_combobox.setDisabled(True)

        elif self._data.nybbles.end is not None:
            self._last_nybble_combobox.combo_box.setCurrentIndex(self._data.nybbles.end.n if self._data.nybbles.end.n is not None else 0)

        else:
            self._last_nybble_combobox.combo_box.setCurrentIndex(0)

        if not (self._type & NybbleData.Type.Bit) or not (self._type & NybbleData.Type.Nybble):
            print('Setting first nybble bit to 0')
            self._first_nybblebit_combobox.setCurrentIndex(0)
            self._first_nybblebit_combobox.setDisabled(True)

        elif self._data.nybbles.start is not None:
            print('Setting first nybble bit to', self._data.nybbles.start.b + 1 if self._data.nybbles.start.b is not None else 0)
            self._first_nybblebit_combobox.combo_box.setCurrentIndex(self._data.nybbles.start.b + 1 if self._data.nybbles.start.b is not None else 0)

        else:
            print('Setting first nybble bit to 0²')
            self._first_nybblebit_combobox.combo_box.setCurrentIndex(0)

        if not (self._type & NybbleData.Type.Bit) or not (self._type & NybbleData.Type.Nybble):
            print('Setting last nybble bit to 0')
            self._last_nybblebit_combobox.setCurrentIndex(0)
            self._last_nybblebit_combobox.setDisabled(True)

        elif self._data.nybbles.end is not None:
            print('Setting last nybble bit to', self._data.nybbles.end.b + 1 if self._data.nybbles.end.b is not None else 0)
            self._last_nybblebit_combobox.combo_box.setCurrentIndex(self._data.nybbles.end.b + 1 if self._data.nybbles.end.b is not None else 0)

        else:
            print('Setting last nybble bit to 0²')
            self._last_nybblebit_combobox.combo_box.setCurrentIndex(0)

        self._first_nybble_combobox.combo_box.currentIndexChanged.connect(self._first_nybble_changed)
        self._last_nybble_combobox.combo_box.currentIndexChanged.connect(self._last_nybble_changed)

        self._block_spinbox.setVisible(show_block)

        if not (self._type & NybbleData.Type.Block):
            self._block_spinbox.setValue(0)
            self._block_spinbox.setDisabled(True)

        else:
            self._block_spinbox.setValue(self._data.block if self._data.block else 0)

        self._first_nybblebit_combobox.combo_box.blockSignals(False)
        self._last_nybblebit_combobox.combo_box.blockSignals(False)


    def convert_to_extended(self, extended: bool) -> None:
        self._rebuild_nybbles(extended)


    def _block_changed(self, value: int) -> None:
        block_data = self._data.block
        self._data.block = value

        if (value == 0 and block_data > 0) or (value > 0 and block_data == 0):
            self._rebuild_nybbles(self.extended)

        self.data_changed.emit()
#----------------------------------------------------------------------
