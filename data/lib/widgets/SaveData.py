#----------------------------------------------------------------------

    # Libraries
from urllib.parse import urlparse
from PySide6.QtWidgets import QFrame, QLabel, QLineEdit, QPushButton
from PySide6.QtCore import Qt

from .PlatformType import PlatformType
from datetime import datetime
from contextlib import suppress
import os

from data.lib.qtUtils import QFiles, QSaveData, QGridFrame, QScrollableGridWidget, QSettingsDialog, QFileButton, QNamedComboBox, QNamedToggleButton, QUtilsColor, QBaseApplication
#----------------------------------------------------------------------

    # Class
class SaveData(QSaveData):
    dateformat = '%Y-%m-%dT%H:%M:%SZ'
    COLOR_LINK = QUtilsColor()

    def __init__(self, app: QBaseApplication, save_path: str = './data/save.dat', main_color_set: QSaveData.ColorSet = None, neutral_color_set: QSaveData.ColorSet = None) -> None:
        self.platform = PlatformType.from_qplatform(app.platform)
        self.check_for_updates = 4

        self.last_check_for_updates = datetime.now()

        self.start_at_launch = True # TODO: Implement this functionallity
        self.minimize_to_tray = True

        self.compact_paths = 0

        self.goes_to_tray_notif = True

        self.projects = []

        match self.platform:
            case PlatformType.Windows:
                self.devkitppc_path = 'C:/devkitPro/devkitPPC/bin/'

            case PlatformType.Linux:
                self.devkitppc_path = '/opt/devkitpro/devkitPPC/bin/'

            case PlatformType.MacOS:
                self.devkitppc_path = '/opt/devkitpro/devkitPPC/bin/'

        super().__init__(app, save_path, main_color_set = main_color_set, neutral_color_set = neutral_color_set)


    def _settings_menu_extra(self) -> tuple[dict, callable]:
        return {
            self.get_lang_data('QSettingsDialog.QSidePanel.updates.title'): (self.settings_menu_updates(), f'{self.get_icon_dir()}/sidepanel/updates.png'),
            self.get_lang_data('QSettingsDialog.QSidePanel.interface.title'): (self.settings_menu_interface(), f'{self.get_icon_dir()}/sidepanel/interface.png'),
            self.get_lang_data('QSettingsDialog.QSidePanel.notification.title'): (self.settings_menu_notification(), f'{self.get_icon_dir()}/sidepanel/notification.png'),
            self.get_lang_data('QSettingsDialog.QSidePanel.paths.title'): (self.settings_menu_paths(), f'{self.get_icon_dir()}/sidepanel/paths.png'),
        }, self.get_extra



    def settings_menu_updates(self) -> QScrollableGridWidget:
        lang = self.get_lang_data('QSettingsDialog.QSidePanel.updates')
        widget = QScrollableGridWidget()
        widget.scroll_layout.setSpacing(0)
        widget.scroll_layout.setContentsMargins(0, 0, 0, 0)


        root_frame = QGridFrame()
        root_frame.grid_layout.setSpacing(16)
        root_frame.grid_layout.setContentsMargins(0, 0, 16, 0)
        widget.scroll_layout.addWidget(root_frame, 0, 0)
        widget.scroll_layout.setAlignment(root_frame, Qt.AlignmentFlag.AlignTop)


        label = QSettingsDialog._text_group(lang.get_data('QLabel.checkForUpdates.title'), lang.get_data('QLabel.checkForUpdates.description'))
        root_frame.grid_layout.addWidget(label, root_frame.grid_layout.count(), 0)

        widget.check_for_updates_combobox = QNamedComboBox(None, lang.get_data('QNamedComboBox.checkForUpdates.title'))
        widget.check_for_updates_combobox.combo_box.addItems([
            lang.get_data('QNamedComboBox.checkForUpdates.values.never'),
            lang.get_data('QNamedComboBox.checkForUpdates.values.daily'),
            lang.get_data('QNamedComboBox.checkForUpdates.values.weekly'),
            lang.get_data('QNamedComboBox.checkForUpdates.values.monthly'),
            lang.get_data('QNamedComboBox.checkForUpdates.values.atLaunch')
        ])
        widget.check_for_updates_combobox.combo_box.setCurrentIndex(self.check_for_updates)
        root_frame.grid_layout.addWidget(widget.check_for_updates_combobox, root_frame.grid_layout.count(), 0)
        root_frame.grid_layout.setAlignment(widget.check_for_updates_combobox, Qt.AlignmentFlag.AlignLeft)


        return widget



    def settings_menu_interface(self) -> QScrollableGridWidget:
        lang = self.get_lang_data('QSettingsDialog.QSidePanel.interface')
        widget = QScrollableGridWidget()
        widget.scroll_layout.setSpacing(0)
        widget.scroll_layout.setContentsMargins(0, 0, 0, 0)

        root_frame = QGridFrame()
        root_frame.grid_layout.setSpacing(16)
        root_frame.grid_layout.setContentsMargins(0, 0, 16, 0)
        widget.scroll_layout.addWidget(root_frame, 0, 0)
        widget.scroll_layout.setAlignment(root_frame, Qt.AlignmentFlag.AlignTop)


        # label = QSettingsDialog.textGroup(lang.get_data('QLabel.startAtLaunch.title'), lang.get_data('QLabel.startAtLaunch.description'))
        # root_frame.grid_layout.addWidget(label, root_frame.grid_layout.count(), 0)

        widget.start_at_launch_checkbox = QNamedToggleButton()
        widget.start_at_launch_checkbox.setText(lang.get_data('QNamedToggleButton.startAtLaunch'))
        widget.start_at_launch_checkbox.setChecked(self.start_at_launch)
        # root_frame.grid_layout.addWidget(widget.start_at_launch_checkbox, root_frame.grid_layout.count(), 0)
        # root_frame.grid_layout.setAlignment(widget.start_at_launch_checkbox, Qt.AlignmentFlag.AlignLeft)


        # frame = QFrame()
        # frame.setProperty('border-top', True)
        # frame.setFixedHeight(1)
        # root_frame.grid_layout.addWidget(frame, root_frame.grid_layout.count(), 0)


        label = QSettingsDialog._text_group(lang.get_data('QLabel.minimizeToTray.title'), lang.get_data('QLabel.minimizeToTray.description'))
        root_frame.grid_layout.addWidget(label, root_frame.grid_layout.count(), 0)

        widget.minimize_to_tray_checkbox = QNamedToggleButton()
        widget.minimize_to_tray_checkbox.setText(lang.get_data('QNamedToggleButton.minimizeToTray'))
        widget.minimize_to_tray_checkbox.setChecked(self.minimize_to_tray)
        root_frame.grid_layout.addWidget(widget.minimize_to_tray_checkbox, root_frame.grid_layout.count(), 0)
        root_frame.grid_layout.setAlignment(widget.minimize_to_tray_checkbox, Qt.AlignmentFlag.AlignLeft)


        frame = QFrame()
        frame.setProperty('border-top', True)
        frame.setFixedHeight(1)
        root_frame.grid_layout.addWidget(frame, root_frame.grid_layout.count(), 0)


        label = QSettingsDialog._text_group(lang.get_data('QLabel.compactPaths.title'), lang.get_data('QLabel.compactPaths.description'))
        root_frame.grid_layout.addWidget(label, root_frame.grid_layout.count(), 0)

        widget.compact_paths_combobox = QNamedComboBox(None, lang.get_data('QNamedComboBox.compactPaths.title'))
        widget.compact_paths_combobox.combo_box.addItems([
            lang.get_data('QNamedComboBox.compactPaths.values.auto'),
            lang.get_data('QNamedComboBox.compactPaths.values.enabled'),
            lang.get_data('QNamedComboBox.compactPaths.values.disabled')
        ])
        widget.compact_paths_combobox.combo_box.setCurrentIndex(self.compact_paths)
        root_frame.grid_layout.addWidget(widget.compact_paths_combobox, root_frame.grid_layout.count(), 0)
        root_frame.grid_layout.setAlignment(widget.compact_paths_combobox, Qt.AlignmentFlag.AlignLeft)


        return widget



    def settings_menu_notification(self) -> QScrollableGridWidget:
        lang = self.get_lang_data('QSettingsDialog.QSidePanel.notification')
        widget = QScrollableGridWidget()
        widget.scroll_layout.setSpacing(0)
        widget.scroll_layout.setContentsMargins(0, 0, 0, 0)

        root_frame = QGridFrame()
        root_frame.grid_layout.setSpacing(16)
        root_frame.grid_layout.setContentsMargins(0, 0, 16, 0)
        widget.scroll_layout.addWidget(root_frame, 0, 0)
        widget.scroll_layout.setAlignment(root_frame, Qt.AlignmentFlag.AlignTop)


        all_checkboxes: list[QNamedToggleButton] = []

        def check_all(checked: bool) -> None:
            for checkbox in all_checkboxes:
                checkbox.setChecked(checked)

        def invert_all() -> None:
            for checkbox in all_checkboxes:
                checkbox.setChecked(not checkbox.isChecked())

        buttonframe = QGridFrame()
        buttonframe.grid_layout.setSpacing(16)
        buttonframe.grid_layout.setContentsMargins(0, 0, 0, 0)
        root_frame.grid_layout.addWidget(buttonframe, root_frame.grid_layout.count(), 0)
        root_frame.grid_layout.setAlignment(buttonframe, Qt.AlignmentFlag.AlignTop)

        button = QPushButton(lang.get_data('QPushButton.checkAll'))
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        button.setProperty('color', 'main')
        button.clicked.connect(lambda: check_all(True))
        buttonframe.grid_layout.addWidget(button, 0, buttonframe.grid_layout.count())

        button = QPushButton(lang.get_data('QPushButton.uncheckAll'))
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        button.setProperty('color', 'main')
        button.clicked.connect(lambda: check_all(False))
        buttonframe.grid_layout.addWidget(button, 0, buttonframe.grid_layout.count())

        button = QPushButton(lang.get_data('QPushButton.invertAll'))
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        button.setProperty('color', 'main')
        button.clicked.connect(lambda: invert_all())
        buttonframe.grid_layout.addWidget(button, 1, 0, 1, 2)


        subframe = QGridFrame()
        subframe.grid_layout.setSpacing(16)
        subframe.grid_layout.setContentsMargins(0, 0, 0, 0)
        root_frame.grid_layout.addWidget(subframe, root_frame.grid_layout.count(), 0)
        root_frame.grid_layout.setAlignment(subframe, Qt.AlignmentFlag.AlignTop)


        def generate_notif(key: str, checked: bool) -> QNamedToggleButton:
            frame = QFrame()
            frame.setProperty('border-top', True)
            frame.setFixedHeight(1)
            subframe.grid_layout.addWidget(frame, subframe.grid_layout.count(), 0)

            label = QSettingsDialog._text_group(lang.get_data(f'QLabel.{key}.title'), lang.get_data(f'QLabel.{key}.description'))
            subframe.grid_layout.addWidget(label, subframe.grid_layout.count(), 0)

            w = QNamedToggleButton()
            w.setText(lang.get_data(f'QNamedToggleButton.{key}'))
            w.setChecked(checked)
            subframe.grid_layout.addWidget(w, subframe.grid_layout.count(), 0)
            subframe.grid_layout.setAlignment(w, Qt.AlignmentFlag.AlignLeft)

            all_checkboxes.append(w)

            return w


        widget.goes_to_tray_notif_checkbox = generate_notif('goesToTray', self.goes_to_tray_notif)

        return widget



    def settings_menu_paths(self) -> QScrollableGridWidget:
        lang = self.get_lang_data('QSettingsDialog.QSidePanel.paths')
        widget = QScrollableGridWidget()
        widget.scroll_layout.setSpacing(0)
        widget.scroll_layout.setContentsMargins(0, 0, 0, 0)


        root_frame = QGridFrame()
        root_frame.grid_layout.setSpacing(16)
        root_frame.grid_layout.setContentsMargins(0, 0, 16, 0)
        widget.scroll_layout.addWidget(root_frame, 0, 0)
        widget.scroll_layout.setAlignment(root_frame, Qt.AlignmentFlag.AlignTop)


        label = QSettingsDialog._text_group(lang.get_data('QLabel.devkitPPCPath.title'), lang.get_data('QLabel.devkitPPCPath.description'))
        root_frame.grid_layout.addWidget(label, root_frame.grid_layout.count(), 0)

        widget.devkitppc_folder_button = QFileButton(
            None,
            lang.get_data('QFileButton.devkitPPCPath'),
            self.devkitppc_path,
            f'{self.get_icon_dir()}filebutton/folder.png',
            QFiles.Dialog.ExistingDirectory
        )
        widget.devkitppc_folder_button.setFixedWidth(350)
        root_frame.grid_layout.addWidget(widget.devkitppc_folder_button, root_frame.grid_layout.count(), 0)
        root_frame.grid_layout.setAlignment(widget.devkitppc_folder_button, Qt.AlignmentFlag.AlignLeft)


        return widget



    def get_extra(self, extra_tabs: dict = {}) -> None:
        self.check_for_updates = extra_tabs[self.get_lang_data('QSettingsDialog.QSidePanel.updates.title')].check_for_updates_combobox.combo_box.currentIndex()

        self.start_at_launch = extra_tabs[self.get_lang_data('QSettingsDialog.QSidePanel.interface.title')].start_at_launch_checkbox.isChecked()
        self.minimize_to_tray = extra_tabs[self.get_lang_data('QSettingsDialog.QSidePanel.interface.title')].minimize_to_tray_checkbox.isChecked()

        self.compact_paths = extra_tabs[self.get_lang_data('QSettingsDialog.QSidePanel.interface.title')].compact_paths_combobox.combo_box.currentIndex()

        self.goes_to_tray_notif = extra_tabs[self.get_lang_data('QSettingsDialog.QSidePanel.notification.title')].goes_to_tray_notif_checkbox.isChecked()

        self.devkitppc_path = extra_tabs[self.get_lang_data('QSettingsDialog.QSidePanel.paths.title')].devkitppc_folder_button.path()



    def valid_url(self, url: str) -> bool:
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except:
            return False


    def without_duplicates(self, l: list) -> list:
        return list(dict.fromkeys(l))


    def _save_extra_data(self) -> dict:
        return {
            'checkForUpdates': self.check_for_updates,
            'lastCheckForUpdates': self.last_check_for_updates.strftime(self.dateformat),

            'startAtLaunch': self.start_at_launch,
            'minimizeToTray': self.minimize_to_tray,

            'compactPaths': self.compact_paths,

            'goesToTrayNotif': self.goes_to_tray_notif,

            'projects': self.projects,

            'devkitPPCPath': self.devkitppc_path
        }

    def _load_extra_data(self, extra_data: dict = ..., reload: list = [], reload_all: bool = False) -> bool:
        exc = suppress(Exception)
        res = False

        with exc: self.check_for_updates = extra_data['checkForUpdates']

        with exc: self.last_check_for_updates = datetime.strptime(extra_data['lastCheckForUpdates'], self.dateformat)

        with exc: self.start_at_launch = extra_data['startAtLaunch']
        with exc: self.minimize_to_tray = extra_data['minimizeToTray']

        with exc: self.compact_paths = extra_data['compactPaths']

        with exc: self.goes_to_tray_notif = extra_data['goesToTrayNotif']

        with exc: self.projects = extra_data['projects']

        with exc: self.devkitppc_path = extra_data['devkitPPCPath']

        return res

    def _export_extra_data(self) -> dict:
        dct = self._save_extra_data()
        return dct
#----------------------------------------------------------------------
