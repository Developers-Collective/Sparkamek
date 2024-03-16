#----------------------------------------------------------------------

    # Libraries
from urllib.parse import urlparse
from PySide6.QtWidgets import QFrame, QPushButton
from PySide6.QtCore import Qt

from .PlatformType import PlatformType
from datetime import datetime
from contextlib import suppress

from data.lib.QtUtils import QFiles, QSaveData, QGridFrame, QScrollableGridWidget, QSettingsDialog, QFileButton, QNamedComboBox, QNamedToggleButton, QUtilsColor, QBaseApplication, QColorSet
from .NotificationManager import NotificationManager
#----------------------------------------------------------------------

    # Class
class SaveData(QSaveData):
    dateformat = '%Y-%m-%dT%H:%M:%SZ'
    COLOR_LINK = QUtilsColor()
    downloads_folder = './Sparkamek/'

    def __init__(self, app: QBaseApplication, save_path: str = './data/save.dat', main_color_set: QColorSet = None, neutral_color_set: QColorSet = None) -> None:
        self.platform = PlatformType.from_qplatform(app.platform)
        self.check_for_updates = 4

        self.last_check_for_updates = datetime.now()

        self.start_at_launch = True # TODO: Implement this functionallity
        self.minimize_to_tray = True

        self.compact_paths = 0

        self.goes_to_tray_notif = True

        self.version = '0' * 8

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


        label = QSettingsDialog._text_group(lang.get('QLabel.checkForUpdates.title'), lang.get('QLabel.checkForUpdates.description'))
        root_frame.grid_layout.addWidget(label, root_frame.grid_layout.count(), 0)

        widget.check_for_updates_combobox = QNamedComboBox(None, lang.get('QNamedComboBox.checkForUpdates.title'))
        widget.check_for_updates_combobox.combo_box.addItems([
            lang.get('QNamedComboBox.checkForUpdates.values.never'),
            lang.get('QNamedComboBox.checkForUpdates.values.daily'),
            lang.get('QNamedComboBox.checkForUpdates.values.weekly'),
            lang.get('QNamedComboBox.checkForUpdates.values.monthly'),
            lang.get('QNamedComboBox.checkForUpdates.values.atLaunch')
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


        # label = QSettingsDialog._text_group(lang.get('QLabel.startAtLaunch.title'), lang.get('QLabel.startAtLaunch.description'))
        # root_frame.grid_layout.addWidget(label, root_frame.grid_layout.count(), 0)

        widget.start_at_launch_checkbox = QNamedToggleButton()
        widget.start_at_launch_checkbox.setText(lang.get('QNamedToggleButton.startAtLaunch'))
        widget.start_at_launch_checkbox.setChecked(self.start_at_launch)
        # root_frame.grid_layout.addWidget(widget.start_at_launch_checkbox, root_frame.grid_layout.count(), 0)
        # root_frame.grid_layout.setAlignment(widget.start_at_launch_checkbox, Qt.AlignmentFlag.AlignLeft)


        # frame = QFrame()
        # frame.setProperty('border-top', True)
        # frame.setFixedHeight(1)
        # root_frame.grid_layout.addWidget(frame, root_frame.grid_layout.count(), 0)


        label = QSettingsDialog._text_group(lang.get('QLabel.minimizeToTray.title'), lang.get('QLabel.minimizeToTray.description'))
        root_frame.grid_layout.addWidget(label, root_frame.grid_layout.count(), 0)

        widget.minimize_to_tray_checkbox = QNamedToggleButton()
        widget.minimize_to_tray_checkbox.setText(lang.get('QNamedToggleButton.minimizeToTray'))
        widget.minimize_to_tray_checkbox.setChecked(self.minimize_to_tray)
        root_frame.grid_layout.addWidget(widget.minimize_to_tray_checkbox, root_frame.grid_layout.count(), 0)
        root_frame.grid_layout.setAlignment(widget.minimize_to_tray_checkbox, Qt.AlignmentFlag.AlignLeft)


        frame = QFrame()
        frame.setProperty('border-top', True)
        frame.setFixedHeight(1)
        root_frame.grid_layout.addWidget(frame, root_frame.grid_layout.count(), 0)


        label = QSettingsDialog._text_group(lang.get('QLabel.compactPaths.title'), lang.get('QLabel.compactPaths.description'))
        root_frame.grid_layout.addWidget(label, root_frame.grid_layout.count(), 0)

        widget.compact_paths_combobox = QNamedComboBox(None, lang.get('QNamedComboBox.compactPaths.title'))
        widget.compact_paths_combobox.combo_box.addItems([
            lang.get('QNamedComboBox.compactPaths.values.auto'),
            lang.get('QNamedComboBox.compactPaths.values.enabled'),
            lang.get('QNamedComboBox.compactPaths.values.disabled')
        ])
        widget.compact_paths_combobox.combo_box.setCurrentIndex(self.compact_paths)
        root_frame.grid_layout.addWidget(widget.compact_paths_combobox, root_frame.grid_layout.count(), 0)
        root_frame.grid_layout.setAlignment(widget.compact_paths_combobox, Qt.AlignmentFlag.AlignLeft)


        frame = QFrame()
        frame.setProperty('border-top', True)
        frame.setFixedHeight(1)
        root_frame.grid_layout.addWidget(frame, root_frame.grid_layout.count(), 0)


        label = QSettingsDialog._text_group(lang.get('QLabel.developerMode.title'), lang.get('QLabel.developerMode.description'))
        root_frame.grid_layout.addWidget(label, root_frame.grid_layout.count(), 0)

        widget.developer_mode_checkbox = QNamedToggleButton()
        widget.developer_mode_checkbox.setText(lang.get('QNamedToggleButton.developerMode'))
        widget.developer_mode_checkbox.setChecked(self._developer_mode)
        root_frame.grid_layout.addWidget(widget.developer_mode_checkbox, root_frame.grid_layout.count(), 0)
        root_frame.grid_layout.setAlignment(widget.developer_mode_checkbox, Qt.AlignmentFlag.AlignLeft)


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

        button = QPushButton(lang.get('QPushButton.checkAll'))
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        button.setProperty('color', 'main')
        button.clicked.connect(lambda: check_all(True))
        buttonframe.grid_layout.addWidget(button, 0, buttonframe.grid_layout.count())

        button = QPushButton(lang.get('QPushButton.uncheckAll'))
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        button.setProperty('color', 'main')
        button.clicked.connect(lambda: check_all(False))
        buttonframe.grid_layout.addWidget(button, 0, buttonframe.grid_layout.count())

        button = QPushButton(lang.get('QPushButton.invertAll'))
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

            label = QSettingsDialog._text_group(lang.get(f'{key}.QLabel.title'), lang.get(f'{key}.QLabel.description'))
            subframe.grid_layout.addWidget(label, subframe.grid_layout.count(), 0)

            w = QNamedToggleButton()
            w.setText(lang.get(f'{key}.QNamedToggleButton'))
            w.setChecked(checked)
            subframe.grid_layout.addWidget(w, subframe.grid_layout.count(), 0)
            subframe.grid_layout.setAlignment(w, Qt.AlignmentFlag.AlignLeft)

            all_checkboxes.append(w)

            return w


        widget.goes_to_tray_notif_checkbox = generate_notif('goesToTray', self.goes_to_tray_notif)
        widget.notif_states = {}

        for key in NotificationManager.get_all():
            widget.notif_states[key] = {}

            for notif in NotificationManager.get(key).keys():
                widget.notif_states[key][notif] = generate_notif(f'game.{key}.{notif}', NotificationManager.get(key)[notif])

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


        label = QSettingsDialog._text_group(lang.get('QLabel.devkitPPCPath.title'), lang.get('QLabel.devkitPPCPath.description'))
        root_frame.grid_layout.addWidget(label, root_frame.grid_layout.count(), 0)

        widget.devkitppc_folder_button = QFileButton(
            None,
            lang.get('QFileButton.devkitPPCPath'),
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
        self._developer_mode = extra_tabs[self.get_lang_data('QSettingsDialog.QSidePanel.interface.title')].developer_mode_checkbox.isChecked()

        self.goes_to_tray_notif = extra_tabs[self.get_lang_data('QSettingsDialog.QSidePanel.notification.title')].goes_to_tray_notif_checkbox.isChecked()

        for key in NotificationManager.get_all():
            for notif in NotificationManager.get(key).keys():
                NotificationManager.get(key)[notif] = extra_tabs[self.get_lang_data('QSettingsDialog.QSidePanel.notification.title')].notif_states[key][notif].isChecked()

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
        notifs = {}

        for key in NotificationManager.get_all():
            notifs[key] = {notif: NotificationManager.get(key)[notif] for notif in NotificationManager.get(key).keys()}

        return {
            'version': self.version,

            'checkForUpdates': self.check_for_updates,
            'lastCheckForUpdates': self.last_check_for_updates.strftime(self.dateformat),

            'startAtLaunch': self.start_at_launch,
            'minimizeToTray': self.minimize_to_tray,

            'compactPaths': self.compact_paths,

            'goesToTrayNotif': self.goes_to_tray_notif,

            'projects': self.projects,

            'devkitPPCPath': self.devkitppc_path,

            'notifications': notifs,
        }


    def _load_extra_data(self, extra_data: dict = ..., reload: list = [], reload_all: bool = False) -> bool:
        exc = suppress(Exception)
        res = False

        with exc: self.version = extra_data['version']

        with exc: self.check_for_updates = extra_data['checkForUpdates']

        with exc: self.last_check_for_updates = datetime.strptime(extra_data['lastCheckForUpdates'], self.dateformat)

        with exc: self.start_at_launch = extra_data['startAtLaunch']
        with exc: self.minimize_to_tray = extra_data['minimizeToTray']

        with exc: self.compact_paths = extra_data['compactPaths']

        with exc: self.goes_to_tray_notif = extra_data['goesToTrayNotif']

        with exc:
            notifs = extra_data['notifications']

            for key in notifs:
                for notif in notifs[key]:
                    NotificationManager.get(key)[notif] = notifs[key][notif]

        with exc: self.projects = extra_data['projects']

        with exc: self.devkitppc_path = extra_data['devkitPPCPath']

        return res


    def _export_extra_data(self) -> dict:
        dct = self._save_extra_data()
        return dct


    def _fix_07e8158b(self) -> None:
        for project in self.projects:
            if not (data := project.get('data')): continue

            if 'kamek' in data: data['wii.nsmbw.kamek'] = data.pop('kamek')
            if 'loader' in data: data['wii.nsmbw.loader'] = data.pop('loader')
            if 'reggieNext' in data: data['wii.nsmbw.reggieNext'] = data.pop('reggieNext')
            if 'riivolution' in data: data['wii.riivolution'] = data.pop('riivolution')

            project.update({
                'platform': 'Wii',
                'game': 'Wii.NSMBW',
            })


    def fix(self) -> None:
        # Fix save data if needed (for example, if a key was renamed) • This is for retrocompatibility
        if self.version <= '07e8158b': self._fix_07e8158b()
#----------------------------------------------------------------------
