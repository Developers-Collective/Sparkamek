#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QLabel, QFrame
from PySide6.QtCore import Qt
from data.lib.QtUtils import QLangData, QGridFrame, QFileButton, QNamedLineEdit, QNamedComboBox, QComboBoxItemModel, QNamedToggleButton, QFiles, QBaseApplication, QUtilsColor, QPlatform
from data.lib.widgets.project import ProjectKeys
from ...BaseWidget import BaseWidget
#----------------------------------------------------------------------

    # Class
class KamekWidget(BaseWidget):
    _kamek_resouces_link: str = ''
    _color_link: QUtilsColor = QUtilsColor('#00aaff')

    _lang: QLangData = QLangData.NoTranslation()

    _open_file_icon: str = ''
    _open_folder_icon: str = ''


    @staticmethod
    def init(app: QBaseApplication) -> None:
        KamekWidget._lang = app.get_lang_data('OpenProjectDialog.game.Wii.NSMBW.kamek')
        KamekWidget._color_link = app.COLOR_LINK
        KamekWidget._open_file_icon = f'{app.save_data.get_icon_dir()}filebutton/file.png'
        KamekWidget._open_folder_icon = f'{app.save_data.get_icon_dir()}filebutton/folder.png'

        match app.platform:
            case QPlatform.Windows:
                KamekWidget._kamek_resouces_link = 'https://horizon.miraheze.org/wiki/Setting_Up_and_Compiling_the_Newer_Sources#Windows'

            case QPlatform.Linux:
                KamekWidget._kamek_resouces_link = 'https://horizon.miraheze.org/wiki/Setting_Up_and_Compiling_the_Newer_Sources#Debian/Ubuntu_Linux'

            case QPlatform.MacOS:
                KamekWidget._kamek_resouces_link = 'https://horizon.miraheze.org/wiki/Setting_Up_and_Compiling_the_Newer_Sources#macOS'

            case _:
                KamekWidget._kamek_resouces_link = 'https://horizon.miraheze.org/wiki/Setting_Up_and_Compiling_the_Newer_Sources'


    def __init__(self, data: dict) -> None:
        super().__init__()

        kamek_data: dict = data['data'].get(ProjectKeys.Wii.NSMBW.Kamek, None) if data else None

        lang = self._lang

        self.scroll_layout.setSpacing(30)
        self.scroll_layout.setContentsMargins(0, 0, 16, 0)

        topframe = QGridFrame()
        topframe.grid_layout.setSpacing(8)
        topframe.grid_layout.setContentsMargins(0, 0, 0, 0)
        self.scroll_layout.addWidget(topframe, self.scroll_layout.count(), 0)

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
        self.scroll_layout.addWidget(root_frame, self.scroll_layout.count(), 0)
        self.scroll_layout.setAlignment(root_frame, Qt.AlignmentFlag.AlignTop)


        label = self._text_group(lang.get('QLabel.kamekFile.title'), lang.get('QLabel.kamekFile.description'))
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


        label = self._text_group(lang.get('QLabel.buildFolder.title'), lang.get('QLabel.buildFolder.description'))
        root_frame.grid_layout.addWidget(label, root_frame.grid_layout.count(), 0)

        self._kamek_build_folder_entry = QNamedLineEdit(None, '', lang.get('QNamedLineEdit.buildFolder'))
        self._kamek_build_folder_entry.setText(kamek_data.get('build', None) if kamek_data else 'Build')
        if self._kamek_build_folder_entry.text() == '': self._kamek_build_folder_entry.setText('Build')
        root_frame.grid_layout.addWidget(self._kamek_build_folder_entry, root_frame.grid_layout.count(), 0)


        frame = QFrame()
        frame.setProperty('border-top', True)
        frame.setFixedHeight(1)
        root_frame.grid_layout.addWidget(frame, root_frame.grid_layout.count(), 0)


        label = self._text_group(lang.get('QLabel.copyType.title'), lang.get('QLabel.copyType.description'))
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
        self._kamek_copy_type_combo_box.setCurrentIndex(kamek_data.get('copyType', 1) if kamek_data else 1)
        root_frame.grid_layout.addWidget(self._kamek_copy_type_combo_box, root_frame.grid_layout.count(), 0)


        frame = QFrame()
        frame.setProperty('border-top', True)
        frame.setFixedHeight(1)
        root_frame.grid_layout.addWidget(frame, root_frame.grid_layout.count(), 0)


        label = self._text_group(lang.get('QLabel.outputFolder.title'), lang.get('QLabel.outputFolder.description'))
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

            label = self._text_group(lang.get(f'QLabel.{key}.title'), lang.get(f'QLabel.{key}.description'))
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

        label = self._text_group(lang.get(f'QLabel.nintendoDriverMode.title'), lang.get(f'QLabel.nintendoDriverMode.description'))
        root_frame.grid_layout.addWidget(label, root_frame.grid_layout.count(), 0)

        self._nintendo_driver_mode_toggle = QNamedToggleButton()
        self._nintendo_driver_mode_toggle.setText(lang.get(f'QNamedToggleButton.nintendoDriverMode'))
        self._nintendo_driver_mode_toggle.setChecked(kamek_data.get('nintendoDriverMode', False) if kamek_data else False)
        root_frame.grid_layout.addWidget(self._nintendo_driver_mode_toggle, root_frame.grid_layout.count(), 0)
        root_frame.grid_layout.setAlignment(self._nintendo_driver_mode_toggle, Qt.AlignmentFlag.AlignLeft)


    def export(self) -> dict | None:
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
#----------------------------------------------------------------------
