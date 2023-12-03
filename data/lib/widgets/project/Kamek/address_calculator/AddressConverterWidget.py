#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QPushButton, QLabel
from PySide6.QtCore import Qt, QSize
from data.lib.qtUtils import QBaseApplication, QGridWidget, QGridGroupBox, QNamedComboBox, QNamedHexSpinBox, QIconWidget, QSaveData
from ..compiler import KamekConstants, AddressMapperController, AddressMapper, AddressMapperMistake
import os
#----------------------------------------------------------------------

    # Class
class AddressConverterWidget(QGridWidget):
    _error_icon = None
    _warning_icon = None
    _success_icon = None
    _right_arrow_icon = None

    _lang = {}

    def init(app: QBaseApplication) -> None:
        AddressConverterWidget._lang = app.get_lang_data('QMainWindow.QSlidingStackedWidget.mainMenu.projects.KamekWidget.AddressCalculatorDockWidget.AddressConverterWidget')
        AddressConverterWidget._error_icon = app.get_icon('raw/error.png', True, QSaveData.IconMode.Local)
        AddressConverterWidget._warning_icon = app.get_icon('raw/warning.png', True, QSaveData.IconMode.Local)
        AddressConverterWidget._success_icon = app.get_icon('raw/success.png', True, QSaveData.IconMode.Local)
        AddressConverterWidget._right_arrow_icon = app.get_icon('raw/arrowRight.png', True, QSaveData.IconMode.Local)


    def __init__(self, app: QBaseApplication, data: dict) -> None:
        super().__init__()
        self._app = app
        self._data = data
        self._path = data.get('path')

        self._address_mapper_path = KamekConstants.get_versions_nsmbw(os.path.dirname(self._path))
        self._base_address_mapper: dict[str, AddressMapper] = None
        self._other_address_mapper: dict[str, AddressMapper] = None
        self._base_errors: dict[str, AddressMapperMistake] = None
        self._other_errors: dict[str, AddressMapperMistake] = None

        self._regions: list[str] = (
            ['default'] +
            (['P1'] if (data.get('generatePALv1', None) or data.get('generatePAL', None)) else []) +
            (['P2'] if (data.get('generatePALv2', None) or data.get('generatePAL', None)) else []) +
            (['E1'] if (data.get('generateNTSCv1', None) or data.get('generateNTSC', None)) else []) +
            (['E2'] if (data.get('generateNTSCv2', None) or data.get('generateNTSC', None)) else []) +
            (['J1'] if (data.get('generateJPv1', None) or data.get('generateJP', None)) else []) +
            (['J2'] if (data.get('generateJPv2', None) or data.get('generateJP', None)) else []) +
            (['K' ]if data.get('generateKR', None) else []) +
            (['W' ]if data.get('generateTW', None) else []) +
            (['C'] if data.get('generateCN', None) else [])
        )

        translated_regions = [self._lang.get_data('QNamedComboBox.region.values').get(region, region).replace('%s', region) for region in self._regions]

        label = QLabel(self._lang.get_data('title'))
        label.setProperty('h', 2)
        label.setProperty('small', True)
        self.grid_layout.addWidget(label, 0, 0, Qt.AlignmentFlag.AlignLeft)

        frame = QGridWidget()
        frame.grid_layout.setContentsMargins(0, 0, 0, 0)
        frame.grid_layout.setSpacing(32)
        self.grid_layout.addWidget(frame, 1, 0, Qt.AlignmentFlag.AlignTop)
        frame.grid_layout.setColumnStretch(5, 1)


        left_groupbox = QGridGroupBox(self._lang.get_data('QGridGroupBox.input.title'))
        left_groupbox.setProperty('QDockWidget', True)
        left_groupbox.grid_layout.setContentsMargins(64, 16, 64, 16)
        left_groupbox.grid_layout.setSpacing(8)
        frame.grid_layout.addWidget(left_groupbox, 0, 0)
        left_groupbox.grid_layout.setRowStretch(2, 1)

        self._input_combobox = QNamedComboBox(None, self._lang.get_data('QGridGroupBox.input.QNamedComboBox.region.title'))
        self._input_combobox.setCursor(Qt.CursorShape.PointingHandCursor)
        self._input_combobox.addItems(translated_regions)
        self._input_combobox.setCurrentIndex(0)
        left_groupbox.grid_layout.addWidget(self._input_combobox, 0, 0)
        self._input_combobox.combo_box.currentIndexChanged.connect(self._convert)

        self._input_hexspinbox = QNamedHexSpinBox(None, self._lang.get_data('QGridGroupBox.input.QNamedHexSpinBox.address'))
        self._input_hexspinbox.set_range(0, 0x80999999)
        self._input_hexspinbox.set_value(0x80000000)
        left_groupbox.grid_layout.addWidget(self._input_hexspinbox, 1, 0)
        self._input_hexspinbox.hex_spinbox.value_changed.connect(self._convert)


        convert_direction_button_left = QIconWidget(None, AddressConverterWidget._right_arrow_icon, QSize(32, 32), False)
        frame.grid_layout.addWidget(convert_direction_button_left, 0, 1)


        middle_groupbox = QGridGroupBox(self._lang.get_data('QGridGroupBox.default.title'))
        middle_groupbox.setProperty('QDockWidget', True)
        middle_groupbox.grid_layout.setContentsMargins(64, 16, 64, 16)
        middle_groupbox.grid_layout.setSpacing(8)
        frame.grid_layout.addWidget(middle_groupbox, 0, 2)
        middle_groupbox.grid_layout.setRowStretch(2, 1)

        self._middle_combobox = QNamedComboBox(None, self._lang.get_data('QGridGroupBox.default.QNamedComboBox.region.title'))
        self._middle_combobox.setCursor(Qt.CursorShape.ForbiddenCursor)
        self._middle_combobox.addItems([translated_regions[0]])
        self._middle_combobox.setCurrentIndex(0)
        middle_groupbox.grid_layout.addWidget(self._middle_combobox, 0, 0)
        self._middle_combobox.combo_box.setDisabled(True)

        row_frame = QGridWidget()
        row_frame.grid_layout.setContentsMargins(0, 0, 0, 0)
        row_frame.grid_layout.setSpacing(8)
        middle_groupbox.grid_layout.addWidget(row_frame, 1, 0)

        self._middle_hexspinbox = QNamedHexSpinBox(None, self._lang.get_data('QGridGroupBox.default.QNamedHexSpinBox.address'))
        self._middle_hexspinbox.set_range(0, 0x80999999)
        self._middle_hexspinbox.set_value(0x80000000)
        row_frame.grid_layout.addWidget(self._middle_hexspinbox, 0, 0)
        self._middle_hexspinbox.hex_spinbox.setReadOnly(True)

        self._middle_icon_widget = QIconWidget(None, AddressConverterWidget._success_icon, QSize(32, 32), False)
        row_frame.grid_layout.addWidget(self._middle_icon_widget, 0, 1)


        convert_direction_button_right = QIconWidget(None, AddressConverterWidget._right_arrow_icon, QSize(32, 32), False)
        frame.grid_layout.addWidget(convert_direction_button_right, 0, 3)


        right_groupbox = QGridGroupBox(self._lang.get_data('QGridGroupBox.output.title'))
        right_groupbox.setProperty('QDockWidget', True)
        right_groupbox.grid_layout.setContentsMargins(64, 16, 64, 16)
        right_groupbox.grid_layout.setSpacing(8)
        frame.grid_layout.addWidget(right_groupbox, 0, 4)
        right_groupbox.grid_layout.setRowStretch(2, 1)

        self._output_combobox = QNamedComboBox(None, self._lang.get_data('QGridGroupBox.output.QNamedComboBox.region.title'))
        self._output_combobox.setCursor(Qt.CursorShape.PointingHandCursor)
        self._output_combobox.addItems(translated_regions)
        self._output_combobox.setCurrentIndex(0)
        right_groupbox.grid_layout.addWidget(self._output_combobox, 0, 0)
        self._output_combobox.combo_box.currentIndexChanged.connect(self._convert)

        row_frame = QGridWidget()
        row_frame.grid_layout.setContentsMargins(0, 0, 0, 0)
        row_frame.grid_layout.setSpacing(8)
        right_groupbox.grid_layout.addWidget(row_frame, 1, 0)

        self._output_hexspinbox = QNamedHexSpinBox(None, self._lang.get_data('QGridGroupBox.output.QNamedHexSpinBox.address'))
        self._output_hexspinbox.set_range(0, 0x80999999)
        self._output_hexspinbox.set_value(0x80000000)
        self._output_hexspinbox.hex_spinbox.setReadOnly(True)
        row_frame.grid_layout.addWidget(self._output_hexspinbox, 0, 0)

        self._output_icon_widget = QIconWidget(None, AddressConverterWidget._success_icon, QSize(32, 32), False)
        row_frame.grid_layout.addWidget(self._output_icon_widget, 0, 1)


    def _convert(self, *args, **kwargs) -> None:
        input_region = self._regions[self._input_combobox.currentIndex()]
        output_region = self._regions[self._output_combobox.currentIndex()]
        input_address = self._input_hexspinbox.value()
        error: bool = False

        if not self._base_address_mapper:
            with open(self._address_mapper_path, 'r', encoding='utf-8') as infile:
                self._base_address_mapper = AddressMapperController.read_version_info(infile)

        if not self._other_address_mapper:
            self._other_address_mapper = AddressMapperController.revert_mappers(self._base_address_mapper)

        if not self._base_errors or not self._other_errors:
            path = KamekConstants.get_errors_nsmbw(os.path.dirname(self._path))
            self._base_errors, self._other_errors = AddressMapperController.read_version_errors(path)

        if self._other_errors[input_region].overlaps(input_address):
            error = True

            self._middle_icon_widget.icon = AddressConverterWidget._warning_icon

            self._app.show_alert(
                self._lang.get_data('QSystemTrayIcon.showMessage.inputOverlap').replace('%s', f'{input_address:X}', 1),
                raise_duration = self._app.ALERT_RAISE_DURATION,
                pause_duration = self._app.ALERT_PAUSE_DURATION,
                fade_duration = self._app.ALERT_FADE_DURATION,
                color = 'main'
            )

        else:
            self._middle_icon_widget.icon = AddressConverterWidget._success_icon

        output_address: int = self._other_address_mapper[input_region].demap_reverse(input_address)
        self._middle_hexspinbox.set_value(output_address)

        if self._base_errors[output_region].overlaps(output_address):
            error = True

            self._app.show_alert(
                self._lang.get_data('QSystemTrayIcon.showMessage.outputOverlap').replace('%s', f'{output_address:X}', 1).replace('%s', output_region, 1),
                raise_duration = self._app.ALERT_RAISE_DURATION,
                pause_duration = self._app.ALERT_PAUSE_DURATION,
                fade_duration = self._app.ALERT_FADE_DURATION,
                color = 'main'
            )

        output_address = self._base_address_mapper[output_region].remap(output_address)

        if not error: self._output_icon_widget.icon = AddressConverterWidget._success_icon
        elif input_address == output_address:
            self._output_icon_widget.icon = AddressConverterWidget._warning_icon

            self._app.show_alert(
                self._lang.get_data('QSystemTrayIcon.showMessage.noChange').replace('%s', f'{input_address:X}', 1).replace('%s', output_region, 1),
                raise_duration = self._app.ALERT_RAISE_DURATION,
                pause_duration = self._app.ALERT_PAUSE_DURATION,
                fade_duration = self._app.ALERT_FADE_DURATION,
                color = 'main'
            )
        else: self._output_icon_widget.icon = AddressConverterWidget._error_icon

        self._output_hexspinbox.set_value(output_address)
#----------------------------------------------------------------------
