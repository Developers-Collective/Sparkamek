#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QDialog, QFrame, QLabel, QGridLayout, QWidget, QPushButton
from PySide6.QtCore import Qt, QSize
from data.lib.qtUtils import QGridFrame, QGridWidget, QSlidingStackedWidget, QScrollableGridWidget, QFileButton, QFiles, QBaseApplication, QNamedComboBox, QNamedToggleButton, QNamedLineEdit, QFlowScrollableWidget, QIconWidget, QUtilsColor, QPlatform, QLangData, QComboBoxItemModel
from data.lib.widgets.project.ProjectKeys import ProjectKeys

import os
#----------------------------------------------------------------------

    # Class
class OpenProjectDialog(QDialog):
    _lang: QLangData = QLangData.NoTranslation()
    _open_image_icon = None
    _open_file_icon = None
    _open_folder_icon = None

    _icon_path = os.path.abspath('./data/icons/sample/')

    _forbidden_paths = (
        None,
        '',
        '.',
        './'
    )

    icon_size = 64
    _color_link = QUtilsColor('#00aaff')

    _kamek_resouces_link = ''

    @staticmethod
    def init(app: QBaseApplication) -> None:
        OpenProjectDialog._lang = app.get_lang_data('OpenProjectDialog')
        OpenProjectDialog._color_link = app.COLOR_LINK
        OpenProjectDialog._open_image_icon = f'{app.save_data.get_icon_dir()}filebutton/image.png'
        OpenProjectDialog._open_file_icon = f'{app.save_data.get_icon_dir()}filebutton/file.png'
        OpenProjectDialog._open_folder_icon = f'{app.save_data.get_icon_dir()}filebutton/folder.png'

        match app.platform:
            case QPlatform.Windows:
                OpenProjectDialog._kamek_resouces_link = 'https://horizon.miraheze.org/wiki/Setting_Up_and_Compiling_the_Newer_Sources#Windows'

            case QPlatform.Linux:
                OpenProjectDialog._kamek_resouces_link = 'https://horizon.miraheze.org/wiki/Setting_Up_and_Compiling_the_Newer_Sources#Debian/Ubuntu_Linux'

            case QPlatform.MacOS:
                OpenProjectDialog._kamek_resouces_link = 'https://horizon.miraheze.org/wiki/Setting_Up_and_Compiling_the_Newer_Sources#macOS'

            case _:
                OpenProjectDialog._kamek_resouces_link = 'https://horizon.miraheze.org/wiki/Setting_Up_and_Compiling_the_Newer_Sources'


    def __init__(self, parent = None, data: dict = None) -> None:
        super().__init__(parent)

        self._data = data

        self._layout = QGridLayout()
        self._layout.setSpacing(0)
        self._layout.setContentsMargins(0, 0, 0, 0)

        right_buttons = QGridWidget()
        right_buttons.grid_layout.setSpacing(16)
        right_buttons.grid_layout.setContentsMargins(0, 0, 0, 0)

        self._cancel_button = QPushButton(self._lang.get('QPushButton.cancel'))
        self._cancel_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self._cancel_button.clicked.connect(self.new_reject)
        self._cancel_button.setProperty('color', 'white')
        self._cancel_button.setProperty('transparent', True)
        right_buttons.grid_layout.addWidget(self._cancel_button, 0, 0)

        self._load_button = QPushButton(self._lang.get('QPushButton.load'))
        self._load_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self._load_button.clicked.connect(self.accept)
        self._load_button.setProperty('color', 'main')
        right_buttons.grid_layout.addWidget(self._load_button, 0, 1)

        self.setWindowTitle(self._lang.get('title.' + ('edit' if data else 'open')))

        self._root = QSlidingStackedWidget()
        self._root.set_orientation(Qt.Orientation.Horizontal)
        self._pages = {}

        root_frame = QGridFrame()
        root_frame.grid_layout.addWidget(self._root, 0, 0)
        root_frame.grid_layout.setSpacing(0)
        root_frame.grid_layout.setContentsMargins(16, 16, 16, 16)

        self._pages['general'] = self._menu_general()
        self._root.addWidget(self._pages['general'])

        self._pages['icon'] = self._menu_icon()
        self._root.addWidget(self._pages['icon'])

        self._pages['loader'] = self._menu_loader()
        self._root.addWidget(self._pages['loader'])

        self._pages['kamek'] = self._menu_kamek()
        self._root.addWidget(self._pages['kamek'])

        self._pages['reggienext'] = self._menu_reggienext()
        self._root.addWidget(self._pages['reggienext'])

        self._pages['riivolution'] = self._menu_riivolution()
        self._root.addWidget(self._pages['riivolution'])

        self._frame = QGridFrame()
        self._frame.grid_layout.addWidget(right_buttons, 0, 0)
        self._frame.grid_layout.setAlignment(right_buttons, Qt.AlignmentFlag.AlignRight)
        self._frame.grid_layout.setSpacing(0)
        self._frame.grid_layout.setContentsMargins(16, 16, 16, 16)
        self._frame.setProperty('border-top', True)
        self._frame.setProperty('border-bottom', True)
        self._frame.setProperty('border-left', True)
        self._frame.setProperty('border-right', True)

        self.setMinimumSize(int(parent.window().size().width() * (205 / 256)), int(parent.window().size().height() * (13 / 15)))

        self._layout.addWidget(root_frame, 0, 0)
        self._layout.addWidget(self._frame, 1, 0)

        self.setLayout(self._layout)
        self._update_keywords()


    def _menu_general(self) -> QWidget:
        lang = self._lang.get('QSlidingStackedWidget.general')

        widget = QScrollableGridWidget()
        widget.scroll_layout.setSpacing(30)
        widget.scroll_layout.setContentsMargins(0, 0, 16, 0)

        topframe = QGridFrame()
        topframe.grid_layout.setSpacing(8)
        topframe.grid_layout.setContentsMargins(0, 0, 0, 0)
        widget.scroll_layout.addWidget(topframe, widget.scroll_layout.count(), 0)

        label = QLabel(lang.get('QLabel.title'))
        label.setProperty('h', 1)
        label.setProperty('margin-left', True)
        topframe.grid_layout.addWidget(label, 0, 0)

        frame = QFrame()
        frame.setProperty('separator', True)
        frame.setFixedHeight(4)
        topframe.grid_layout.addWidget(frame, 1, 0)

        root_frame = QGridFrame()
        root_frame.grid_layout.setSpacing(16)
        root_frame.grid_layout.setContentsMargins(0, 0, 0, 0)
        widget.scroll_layout.addWidget(root_frame, widget.scroll_layout.count(), 0)
        widget.scroll_layout.setAlignment(root_frame, Qt.AlignmentFlag.AlignTop)


        label = OpenProjectDialog._text_group(lang.get('QLabel.name.title'), lang.get('QLabel.name.description'))
        root_frame.grid_layout.addWidget(label, root_frame.grid_layout.count(), 0)

        self.name_entry = QNamedLineEdit(None, '', lang.get('QNamedLineEdit.name'))
        self.name_entry.setText(self._data['name'] if self._data else 'Project')
        root_frame.grid_layout.addWidget(self.name_entry, root_frame.grid_layout.count(), 0)


        return widget



    def _menu_icon(self) -> QWidget:
        lang = self._lang.get('QSlidingStackedWidget.icon')

        self.raw_icon = self._data['icon'] if self._data else os.path.abspath('./data/icons/questionMark.svg')

        widget = QScrollableGridWidget()
        widget.scroll_layout.setSpacing(30)
        widget.scroll_layout.setContentsMargins(0, 0, 0, 0)

        topframe = QGridFrame()
        topframe.grid_layout.setSpacing(8)
        topframe.grid_layout.setContentsMargins(0, 0, 0, 0)
        widget.scroll_layout.addWidget(topframe, widget.scroll_layout.count(), 0)

        label = QLabel(lang.get('QLabel.title'))
        label.setProperty('h', 1)
        label.setProperty('margin-left', True)
        topframe.grid_layout.addWidget(label, 0, 0)

        frame = QFrame()
        frame.setProperty('separator', True)
        frame.setFixedHeight(4)
        topframe.grid_layout.addWidget(frame, 1, 0)

        root_frame = QGridFrame()
        root_frame.grid_layout.setSpacing(16)
        root_frame.grid_layout.setContentsMargins(0, 0, 0, 0)
        widget.scroll_layout.addWidget(root_frame, widget.scroll_layout.count(), 0)
        widget.scroll_layout.setAlignment(root_frame, Qt.AlignmentFlag.AlignTop)

        widget.top = QGridFrame()
        widget.top.grid_layout.setSpacing(16)
        widget.top.grid_layout.setContentsMargins(0, 0, 0, 0)
        root_frame.grid_layout.addWidget(widget.top, root_frame.grid_layout.count(), 0)

        label = OpenProjectDialog._text_group(lang.get('QLabel.icon.title'), lang.get('QLabel.icon.description'))
        widget.top.grid_layout.addWidget(label, 0, 0, 1, 2)

        widget.top.icon_group = self.icon_with_text(self.raw_icon, lang.get('QLabel.currentIcon'))
        widget.top.grid_layout.addWidget(widget.top.icon_group, 1, 0)

        self.icon_button = QFileButton(
            self, lang.get('QFileButton.icon'),
            self.raw_icon,
            self._open_image_icon,
            QFiles.Dialog.OpenFileName,
            'All supported files (*.svg *.ico *.png *.jpg *.jpeg *.exe *.bat *.sh);;SVG (*.svg);;ICO (*.ico);;PNG (*.png);;JPEG (*.jpg *.jpeg);;Executable (*.exe);;Batch (*.bat);;Shell (*.sh)'
        )
        self.icon_button.path_changed.connect(self._icon_file_button_path_changed)
        self.icon_button.setMinimumWidth(int(self.icon_button.sizeHint().width() * 1.25))
        widget.top.grid_layout.addWidget(self.icon_button, 1, 1)


        frame = QFrame()
        frame.setProperty('border-top', True)
        frame.setFixedHeight(1)
        root_frame.grid_layout.addWidget(frame, root_frame.grid_layout.count(), 0)


        label = OpenProjectDialog._text_group(lang.get('QLabel.predefinedIcons.title'), lang.get('QLabel.predefinedIcons.description'))
        root_frame.grid_layout.addWidget(label, root_frame.grid_layout.count(), 0)


        widget.bottom = QFlowScrollableWidget()
        widget.bottom.scroll_layout.setSpacing(16)
        widget.bottom.scroll_layout.setContentsMargins(0, 0, 0, 0)
        root_frame.grid_layout.addWidget(widget.bottom, root_frame.grid_layout.count(), 0)

        for index, icon in enumerate(['../none.svg'] + os.listdir(self._icon_path)):
            if not icon.endswith('.svg'): continue
            b = self._generate_button(f'{self._icon_path}/{icon}')
            widget.bottom.scroll_layout.addWidget(b)

        widget.bottom.setFixedHeight(widget.bottom.heightMM() + 16) # Cuz weird things happen when resizing the window


        return widget



    def _menu_loader(self) -> QWidget:
        loader_data: dict = self._data['data'].get(ProjectKeys.Wii.NSMBW.Loader, None) if self._data else None

        lang = self._lang.get('QSlidingStackedWidget.loader')

        widget = QScrollableGridWidget()
        widget.scroll_layout.setSpacing(30)
        widget.scroll_layout.setContentsMargins(0, 0, 16, 0)

        topframe = QGridFrame()
        topframe.grid_layout.setSpacing(8)
        topframe.grid_layout.setContentsMargins(0, 0, 0, 0)
        widget.scroll_layout.addWidget(topframe, widget.scroll_layout.count(), 0)

        label = QLabel(lang.get('QLabel.title'))
        label.setProperty('h', 1)
        label.setProperty('margin-left', True)
        topframe.grid_layout.addWidget(label, 0, 0)

        frame = QFrame()
        frame.setProperty('separator', True)
        frame.setFixedHeight(4)
        topframe.grid_layout.addWidget(frame, 1, 0)

        root_frame = QGridFrame()
        root_frame.grid_layout.setSpacing(16)
        root_frame.grid_layout.setContentsMargins(0, 0, 0, 0)
        widget.scroll_layout.addWidget(root_frame, widget.scroll_layout.count(), 0)
        widget.scroll_layout.setAlignment(root_frame, Qt.AlignmentFlag.AlignTop)


        label = OpenProjectDialog._text_group(lang.get('QLabel.loaderFile.title'), lang.get('QLabel.loaderFile.description'))
        root_frame.grid_layout.addWidget(label, root_frame.grid_layout.count(), 0)

        kw = ('edit' if loader_data else 'open') + 'LoaderFile'
        l = {
            "title": lang.get(f'QFileButton.{kw}.title'),
            "dialog": lang.get(f'QFileButton.{kw}.dialog')
        }

        self.loader_file_button = QFileButton(
            None,
            l,
            loader_data['path'] if loader_data else None,
            self._open_file_icon,
            QFiles.Dialog.OpenFileName,
            'All supported files (*.s *.S);;ASM (*.s *.S)'
        )
        self.loader_file_button.setFixedWidth(350)
        root_frame.grid_layout.addWidget(self.loader_file_button, root_frame.grid_layout.count(), 0)
        root_frame.grid_layout.setAlignment(self.loader_file_button, Qt.AlignmentFlag.AlignLeft)


        frame = QFrame()
        frame.setProperty('border-top', True)
        frame.setFixedHeight(1)
        root_frame.grid_layout.addWidget(frame, root_frame.grid_layout.count(), 0)


        label = OpenProjectDialog._text_group(lang.get('QLabel.outputFile.title'), lang.get('QLabel.outputFile.description'))
        root_frame.grid_layout.addWidget(label, root_frame.grid_layout.count(), 0)

        kw = ('edit' if loader_data else 'open') + 'OutputFile'
        l = {
            "title": lang.get(f'QFileButton.{kw}.title'),
            "dialog": lang.get(f'QFileButton.{kw}.dialog')
        }

        self.loader_output_file_button = QFileButton(
            None,
            l,
            loader_data.get('outputFile', None) if loader_data else None,
            self._open_file_icon,
            QFiles.Dialog.OpenFileName,
            'All supported files (*.bin);;Binary (*.bin)'
        )
        self.loader_output_file_button.setFixedWidth(350)
        root_frame.grid_layout.addWidget(self.loader_output_file_button, root_frame.grid_layout.count(), 0)
        root_frame.grid_layout.setAlignment(self.loader_output_file_button, Qt.AlignmentFlag.AlignLeft)


        return widget



    def _menu_kamek(self) -> QWidget:
        kamek_data: dict = self._data['data'].get(ProjectKeys.Wii.NSMBW.Kamek, None) if self._data else None

        lang = self._lang.get('QSlidingStackedWidget.kamek')

        widget = QScrollableGridWidget()
        widget.scroll_layout.setSpacing(30)
        widget.scroll_layout.setContentsMargins(0, 0, 16, 0)

        topframe = QGridFrame()
        topframe.grid_layout.setSpacing(8)
        topframe.grid_layout.setContentsMargins(0, 0, 0, 0)
        widget.scroll_layout.addWidget(topframe, widget.scroll_layout.count(), 0)

        label = QLabel(lang.get('QLabel.title'))
        label.setProperty('h', 1)
        label.setProperty('margin-left', 16)
        topframe.grid_layout.addWidget(label, 0, 0)

        frame = QFrame()
        frame.setProperty('separator', True)
        frame.setFixedHeight(4)
        topframe.grid_layout.addWidget(frame, 1, 0)

        label = QLabel(lang.get('QLabel.resources').replace('%s', f'<a href="{self._kamek_resouces_link}" style=\"color: {self._color_link.hex}; text-decoration: none;\">Horizon Wiki</a>'))
        label.setProperty('brighttitle', True)
        label.setOpenExternalLinks(True)
        label.setProperty('margin-left', 16)
        topframe.grid_layout.addWidget(label, 2, 0)

        frame = QFrame()
        frame.setProperty('separator', True)
        frame.setFixedHeight(4)
        topframe.grid_layout.addWidget(frame, 3, 0)

        root_frame = QGridFrame()
        root_frame.grid_layout.setSpacing(16)
        root_frame.grid_layout.setContentsMargins(0, 0, 0, 0)
        widget.scroll_layout.addWidget(root_frame, widget.scroll_layout.count(), 0)
        widget.scroll_layout.setAlignment(root_frame, Qt.AlignmentFlag.AlignTop)


        label = OpenProjectDialog._text_group(lang.get('QLabel.kamekFile.title'), lang.get('QLabel.kamekFile.description'))
        root_frame.grid_layout.addWidget(label, root_frame.grid_layout.count(), 0)

        l = {
            "title": lang.get(f'QFileButton.kamekFile'),
            "dialog": lang.get(f'QFileButton.pattern.' + ('edit' if kamek_data else 'open')).replace('%s', lang.get(f'QFileButton.kamekFile'))
        }

        self._kamek_file_button = QFileButton(
            None,
            l,
            kamek_data.get('path', None) if kamek_data else None,
            self._open_file_icon,
            QFiles.Dialog.OpenFileName,
            'All supported files (*.yaml *.yml);;YAML (*.yaml *.yml)'
        )
        self._kamek_file_button.setFixedWidth(350)
        root_frame.grid_layout.addWidget(self._kamek_file_button, root_frame.grid_layout.count(), 0)
        root_frame.grid_layout.setAlignment(self._kamek_file_button, Qt.AlignmentFlag.AlignLeft)


        frame = QFrame()
        frame.setProperty('border-top', True)
        frame.setFixedHeight(1)
        root_frame.grid_layout.addWidget(frame, root_frame.grid_layout.count(), 0)


        label = OpenProjectDialog._text_group(lang.get('QLabel.buildFolder.title'), lang.get('QLabel.buildFolder.description'))
        root_frame.grid_layout.addWidget(label, root_frame.grid_layout.count(), 0)

        self._kamek_build_folder_entry = QNamedLineEdit(None, '', lang.get('QNamedLineEdit.buildFolder'))
        self._kamek_build_folder_entry.setText(kamek_data.get('build', None) if kamek_data else 'Build')
        if self._kamek_build_folder_entry.text() == '': self._kamek_build_folder_entry.setText('Build')
        root_frame.grid_layout.addWidget(self._kamek_build_folder_entry, root_frame.grid_layout.count(), 0)


        frame = QFrame()
        frame.setProperty('border-top', True)
        frame.setFixedHeight(1)
        root_frame.grid_layout.addWidget(frame, root_frame.grid_layout.count(), 0)


        label = OpenProjectDialog._text_group(lang.get('QLabel.copyType.title'), lang.get('QLabel.copyType.description'))
        root_frame.grid_layout.addWidget(label, root_frame.grid_layout.count(), 0)

        copy_type_model: QComboBoxItemModel = QComboBoxItemModel()

        self._kamek_copy_type_combo_box = QNamedComboBox(None, lang.get('QNamedComboBox.copyType.title'))
        copy_type_model.add_item(
            lang.get('QNamedComboBox.copyType.items.copy.title'),
            lang.get('QNamedComboBox.copyType.items.copy.title') + '\n' + lang.get('QNamedComboBox.copyType.items.copy.description'),
        )
        copy_type_model.add_item(
            lang.get('QNamedComboBox.copyType.items.move.title'),
            lang.get('QNamedComboBox.copyType.items.move.title') + '\n' + lang.get('QNamedComboBox.copyType.items.move.description'),
        )
        copy_type_model.bind(self._kamek_copy_type_combo_box.combo_box)
        self._kamek_copy_type_combo_box.setCurrentIndex(kamek_data.get('copyType', 1))
        root_frame.grid_layout.addWidget(self._kamek_copy_type_combo_box, root_frame.grid_layout.count(), 0)


        frame = QFrame()
        frame.setProperty('border-top', True)
        frame.setFixedHeight(1)
        root_frame.grid_layout.addWidget(frame, root_frame.grid_layout.count(), 0)


        label = OpenProjectDialog._text_group(lang.get('QLabel.outputFolder.title'), lang.get('QLabel.outputFolder.description'))
        root_frame.grid_layout.addWidget(label, root_frame.grid_layout.count(), 0)

        l = {
            "title": lang.get(f'QFileButton.outputFolder'),
            "dialog": lang.get(f'QFileButton.pattern.' + ('edit' if kamek_data else 'open')).replace('%s', lang.get(f'QFileButton.outputFolder'))
        }


        self._kamek_output_folder = QFileButton(
            None,
            l,
            kamek_data.get('outputFolder') if kamek_data else None,
            self._open_folder_icon,
            QFiles.Dialog.ExistingDirectory
        )
        self._kamek_output_folder.setFixedWidth(350)
        root_frame.grid_layout.addWidget(self._kamek_output_folder, root_frame.grid_layout.count(), 0)
        root_frame.grid_layout.setAlignment(self._kamek_output_folder, Qt.AlignmentFlag.AlignLeft)


        def generate_version(key: str, checked: bool) -> QNamedToggleButton:
            frame = QFrame()
            frame.setProperty('border-top', True)
            frame.setFixedHeight(1)
            root_frame.grid_layout.addWidget(frame, root_frame.grid_layout.count(), 0)

            label = OpenProjectDialog._text_group(lang.get(f'QLabel.{key}.title'), lang.get(f'QLabel.{key}.description'))
            root_frame.grid_layout.addWidget(label, root_frame.grid_layout.count(), 0)

            w = QNamedToggleButton()
            w.setText(lang.get(f'QNamedToggleButton.{key}'))
            w.setChecked(checked)
            root_frame.grid_layout.addWidget(w, root_frame.grid_layout.count(), 0)
            root_frame.grid_layout.setAlignment(w, Qt.AlignmentFlag.AlignLeft)

            return w


        self._kamek_generate_pal_v1_toggle = generate_version('generatePALv1', (kamek_data.get('generatePALv1', True) or kamek_data.get('generatePAL', True)) if kamek_data else True)
        self._kamek_generate_pal_v1_toggle.setDisabled(True)
        self._kamek_generate_pal_v2_toggle = generate_version('generatePALv2', (kamek_data.get('generatePALv2', False) or kamek_data.get('generatePAL', False)) if kamek_data else True)
        self._kamek_generate_ntsc_v1_toggle = generate_version('generateNTSCv1', (kamek_data.get('generateNTSCv1', False) or kamek_data.get('generateNTSC', False)) if kamek_data else True)
        self._kamek_generate_ntsc_v2_toggle = generate_version('generateNTSCv2', (kamek_data.get('generateNTSCv2', False) or kamek_data.get('generateNTSC', False)) if kamek_data else True)
        self._kamek_generate_jp_v1_toggle = generate_version('generateJPv1', (kamek_data.get('generateJPv1', False) or kamek_data.get('generateJP', False)) if kamek_data else True)
        self._kamek_generate_jp_v2_toggle = generate_version('generateJPv2', (kamek_data.get('generateJPv2', False) or kamek_data.get('generateJP', False)) if kamek_data else True)
        self._kamek_generate_tw_toggle = generate_version('generateTW', kamek_data.get('generateTW', False) if kamek_data else True)
        self._kamek_generate_kr_toggle = generate_version('generateKR', kamek_data.get('generateKR', False) if kamek_data else True)
        self._kamek_generate_cn_toggle = generate_version('generateCN', kamek_data.get('generateCN', False) if kamek_data else False)


        frame = QFrame()
        frame.setProperty('border-top', True)
        frame.setFixedHeight(1)
        root_frame.grid_layout.addWidget(frame, root_frame.grid_layout.count(), 0)

        label = OpenProjectDialog._text_group(lang.get(f'QLabel.nintendoDriverMode.title'), lang.get(f'QLabel.nintendoDriverMode.description'))
        root_frame.grid_layout.addWidget(label, root_frame.grid_layout.count(), 0)

        self._nintendo_driver_mode_toggle = QNamedToggleButton()
        self._nintendo_driver_mode_toggle.setText(lang.get(f'QNamedToggleButton.nintendoDriverMode'))
        self._nintendo_driver_mode_toggle.setChecked(kamek_data.get('nintendoDriverMode', False) if kamek_data else False)
        root_frame.grid_layout.addWidget(self._nintendo_driver_mode_toggle, root_frame.grid_layout.count(), 0)
        root_frame.grid_layout.setAlignment(self._nintendo_driver_mode_toggle, Qt.AlignmentFlag.AlignLeft)


        return widget



    def _menu_reggienext(self) -> QWidget:
        reggienext_data: dict = self._data['data'].get(ProjectKeys.Wii.NSMBW.ReggieNext, None) if self._data else None

        lang = self._lang.get('QSlidingStackedWidget.reggieNext')

        widget = QScrollableGridWidget()
        widget.scroll_layout.setSpacing(30)
        widget.scroll_layout.setContentsMargins(0, 0, 16, 0)

        topframe = QGridFrame()
        topframe.grid_layout.setSpacing(8)
        topframe.grid_layout.setContentsMargins(0, 0, 0, 0)
        widget.scroll_layout.addWidget(topframe, widget.scroll_layout.count(), 0)

        label = QLabel(lang.get('QLabel.title'))
        label.setProperty('h', 1)
        label.setProperty('margin-left', True)
        topframe.grid_layout.addWidget(label, 0, 0)

        frame = QFrame()
        frame.setProperty('separator', True)
        frame.setFixedHeight(4)
        topframe.grid_layout.addWidget(frame, 1, 0)

        root_frame = QGridFrame()
        root_frame.grid_layout.setSpacing(16)
        root_frame.grid_layout.setContentsMargins(0, 0, 0, 0)
        widget.scroll_layout.addWidget(root_frame, widget.scroll_layout.count(), 0)
        widget.scroll_layout.setAlignment(root_frame, Qt.AlignmentFlag.AlignTop)


        label = OpenProjectDialog._text_group(lang.get('QLabel.reggieNextFolder.title'), lang.get('QLabel.reggieNextFolder.description'))
        root_frame.grid_layout.addWidget(label, root_frame.grid_layout.count(), 0)

        kw = ('edit' if reggienext_data else 'open') + 'ReggieNextFolder'
        l = {
            "title": lang.get(f'QFileButton.{kw}.title'),
            "dialog": lang.get(f'QFileButton.{kw}.dialog')
        }

        self.reggie_folder_button = QFileButton(
            None,
            l,
            reggienext_data['path'] if reggienext_data else None,
            self._open_folder_icon,
            QFiles.Dialog.ExistingDirectory
        )
        self.reggie_folder_button.setFixedWidth(350)
        root_frame.grid_layout.addWidget(self.reggie_folder_button, root_frame.grid_layout.count(), 0)
        root_frame.grid_layout.setAlignment(self.reggie_folder_button, Qt.AlignmentFlag.AlignLeft)


        return widget



    def _menu_riivolution(self) -> QWidget:
        riivolution_data: dict = self._data['data'].get(ProjectKeys.Wii.Riivolution, None) if self._data else None

        lang = self._lang.get('QSlidingStackedWidget.riivolution')

        widget = QScrollableGridWidget()
        widget.scroll_layout.setSpacing(30)
        widget.scroll_layout.setContentsMargins(0, 0, 16, 0)

        topframe = QGridFrame()
        topframe.grid_layout.setSpacing(8)
        topframe.grid_layout.setContentsMargins(0, 0, 0, 0)
        widget.scroll_layout.addWidget(topframe, widget.scroll_layout.count(), 0)

        label = QLabel(lang.get('QLabel.title'))
        label.setProperty('h', 1)
        label.setProperty('margin-left', True)
        topframe.grid_layout.addWidget(label, 0, 0)

        frame = QFrame()
        frame.setProperty('separator', True)
        frame.setFixedHeight(4)
        topframe.grid_layout.addWidget(frame, 1, 0)

        root_frame = QGridFrame()
        root_frame.grid_layout.setSpacing(16)
        root_frame.grid_layout.setContentsMargins(0, 0, 0, 0)
        widget.scroll_layout.addWidget(root_frame, widget.scroll_layout.count(), 0)
        widget.scroll_layout.setAlignment(root_frame, Qt.AlignmentFlag.AlignTop)


        label = OpenProjectDialog._text_group(lang.get('QLabel.riivolutionFile.title'), lang.get('QLabel.riivolutionFile.description'))
        root_frame.grid_layout.addWidget(label, root_frame.grid_layout.count(), 0)

        kw = ('edit' if riivolution_data else 'open') + 'RiivolutionFile'
        l = {
            "title": lang.get(f'QFileButton.{kw}.title'),
            "dialog": lang.get(f'QFileButton.{kw}.dialog')
        }

        self.riivolution_file_button = QFileButton(
            None,
            l,
            riivolution_data['path'] if riivolution_data else None,
            self._open_file_icon,
            QFiles.Dialog.OpenFileName,
            'All supported files (*.xml);;XML (*.xml)'
        )
        self.riivolution_file_button.setFixedWidth(350)
        root_frame.grid_layout.addWidget(self.riivolution_file_button, root_frame.grid_layout.count(), 0)
        root_frame.grid_layout.setAlignment(self.riivolution_file_button, Qt.AlignmentFlag.AlignLeft)


        return widget



    def _text_group(title: str = '', description: str = '') -> QGridWidget:
        widget = QGridWidget()
        widget.grid_layout.setSpacing(0)
        widget.grid_layout.setContentsMargins(0, 0, 0, 0)

        label = QLabel(title)
        label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        label.setProperty('bigbrighttitle', True)
        label.setWordWrap(True)
        widget.grid_layout.addWidget(label, 0, 0)

        label = QLabel(description)
        label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        label.setProperty('brightnormal', True)
        label.setWordWrap(True)
        widget.grid_layout.addWidget(label, 1, 0)
        widget.grid_layout.setRowStretch(2, 1)

        return widget

    def icon_with_text(self, icon: str = None, text: str = '') -> QGridWidget:
        widget = QGridWidget()
        widget.grid_layout.setSpacing(16)
        widget.grid_layout.setContentsMargins(0, 0, 0, 0)

        label = QLabel(text)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setProperty('title', True)
        widget.grid_layout.addWidget(label, 0, 0)
        widget.grid_layout.setAlignment(label, Qt.AlignmentFlag.AlignCenter)

        widget.icon_widget = QIconWidget(None, icon, QSize(40, 40), True)
        widget.grid_layout.addWidget(widget.icon_widget, 1, 0)
        widget.grid_layout.setAlignment(widget.icon_widget, Qt.AlignmentFlag.AlignCenter)

        widget.grid_layout.setRowStretch(2, 1)

        return widget

    def _generate_button(self, path: str = None) -> QIconWidget:
        button = QIconWidget(None, path, QSize(self.icon_size, self.icon_size))
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        button.setProperty('imagebutton', True)
        button.mouseReleaseEvent = lambda _: self._icon_click(os.path.abspath(path))

        return button

    def _icon_click(self, path: str = None) -> None:
        if not path: return
        if not os.path.exists(path) or not os.path.isfile(path): return

        self._update(path)



    def _update(self, path: str = None) -> None:
        if not path: return
        if not os.path.isfile(path): return

        w = self._pages['icon']
        self.icon_button.setPath(path)
        w.top.icon_group.icon_widget.icon = path

    def _icon_file_button_path_changed(self, path: str = None) -> None:
        if not path: return
        self._update(path)



    def accept(self) -> None:
        if self._root.current_index == self._root.count() - 1:
            return super().accept()
        self._root.slide_in_next()
        self._update_keywords()

    def new_reject(self) -> None:
        if self._root.current_index == 0:
            return self.reject()
        self._root.slide_in_previous()
        self._update_keywords()

    def reject(self) -> None:
        return super().reject()

    def _update_keywords(self) -> None:
        if self._root.current_index < self._root.count() - 1:
            self._load_button.setText(self._lang.get('QPushButton.next'))
        else:
            self._load_button.setText(self._lang.get('QPushButton.load'))

        if self._root.current_index == 0:
            self._cancel_button.setText(self._lang.get('QPushButton.cancel'))
        else:
            self._cancel_button.setText(self._lang.get('QPushButton.back'))

    def _get_loader(self) -> dict | None:
        if self.loader_file_button.path() in self._forbidden_paths: return None

        return {
            'path': self.loader_file_button.path(),
            'outputFile': self.loader_output_file_button.path() if self.loader_output_file_button.path() not in self._forbidden_paths else None,
        }
    
    def _get_kamek(self) -> dict | None:
        if self._kamek_file_button.path() in self._forbidden_paths: return None

        build_folder = self._kamek_build_folder_entry.text() if self._kamek_build_folder_entry.text() else 'Build'
        new_build_folder = ''
        for c in build_folder:
            o = ord(c)
            if (
                (o >= 65 and o <= 90) # A-Z
                or (o >= 97 and o <= 122) # a-z
                or (o >= 48 and o <= 57) # 0-9
                or o == 95 # _
                or o == 45 # -
                or o == 46 # .
            ): new_build_folder += c
        
        if new_build_folder == '': new_build_folder = 'Build'

        return {
            'path': self._kamek_file_button.path(),
            'buildFolder': new_build_folder,
            'copyType': self._kamek_copy_type_combo_box.currentIndex(),
            'outputFolder': self._kamek_output_folder.path() if self._kamek_output_folder.path() not in self._forbidden_paths else None,
            'generatePALv1': self._kamek_generate_pal_v1_toggle.isChecked(),
            'generatePALv2': self._kamek_generate_pal_v2_toggle.isChecked(),
            'generateNTSCv1': self._kamek_generate_ntsc_v1_toggle.isChecked(),
            'generateNTSCv2': self._kamek_generate_ntsc_v2_toggle.isChecked(),
            'generateJPv1': self._kamek_generate_jp_v1_toggle.isChecked(),
            'generateJPv2': self._kamek_generate_jp_v2_toggle.isChecked(),
            'generateTW': self._kamek_generate_tw_toggle.isChecked(),
            'generateKR': self._kamek_generate_kr_toggle.isChecked(),
            'generateCN': self._kamek_generate_cn_toggle.isChecked(),
            'nintendoDriverMode': self._nintendo_driver_mode_toggle.isChecked()
        }

    def _get_reggienext(self) -> dict | None:
        if self.reggie_folder_button.path() in self._forbidden_paths: return None

        return {
            'path': self.reggie_folder_button.path()
        }

    def _get_riivolution(self) -> dict | None:
        if self.riivolution_file_button.path() in self._forbidden_paths: return None

        return {
            'path': self.riivolution_file_button.path()
        }


    def exec(self) -> dict | None:
        if super().exec():
            data = {
                'name': self.name_entry.text() if self.name_entry.text() else 'Project',
                'icon': self.icon_button.path() if self.icon_button.path() not in self._forbidden_paths else None,
                'data': {
                    ProjectKeys.Wii.NSMBW.Loader: self._get_loader(),
                    ProjectKeys.Wii.NSMBW.Kamek: self._get_kamek(),
                    ProjectKeys.Wii.NSMBW.ReggieNext: self._get_reggienext(),
                    ProjectKeys.Wii.Riivolution: self._get_riivolution()
                }
            }
            return data if any(data['data'].values()) else None
        return None
#----------------------------------------------------------------------
