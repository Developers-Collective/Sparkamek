#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QDialog, QFrame, QLabel, QGridLayout, QWidget, QPushButton
from PySide6.QtCore import Qt, QSize
from collections import namedtuple
from data.lib.qtUtils import QGridFrame, QGridWidget, QSlidingStackedWidget, QScrollableGridWidget, QFileButton, QFiles, QBaseApplication, QNamedComboBox, QNamedToggleButton, QNamedLineEdit, QFlowScrollableWidget, QIconWidget
from data.lib.widgets.ProjectKeys import ProjectKeys

import os
#----------------------------------------------------------------------

    # Class
class OpenProjectDialog(QDialog):
    _lang = {}
    _open_image_icon = None
    _open_file_icon = None
    _open_folder_icon = None

    _icon_path = os.path.abspath('./data/icons/sample/')

    icon_size = 64

    @staticmethod
    def init(app: QBaseApplication) -> None:
        OpenProjectDialog._lang = app.save_data.language_data['OpenProjectDialog']
        OpenProjectDialog._open_image_icon = f'{app.save_data.get_icon_dir()}filebutton/image.png'
        OpenProjectDialog._open_file_icon = f'{app.save_data.get_icon_dir()}filebutton/file.png'
        OpenProjectDialog._open_folder_icon = f'{app.save_data.get_icon_dir()}filebutton/folder.png'

    def __init__(self, parent = None, data: dict = None) -> None:
        super().__init__(parent)

        self._data = data

        self._layout = QGridLayout()
        self._layout.setSpacing(0)
        self._layout.setContentsMargins(0, 0, 0, 0)

        right_buttons = QGridWidget()
        right_buttons.grid_layout.setSpacing(16)
        right_buttons.grid_layout.setContentsMargins(0, 0, 0, 0)

        self._cancel_button = QPushButton(self._lang['QPushButton']['cancel'])
        self._cancel_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self._cancel_button.clicked.connect(self.reject)
        self._cancel_button.setProperty('color', 'white')
        self._cancel_button.setProperty('transparent', True)
        right_buttons.grid_layout.addWidget(self._cancel_button, 0, 0)

        self._load_button = QPushButton(self._lang['QPushButton']['load'])
        self._load_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self._load_button.clicked.connect(self.accept)
        self._load_button.setProperty('color', 'main')
        right_buttons.grid_layout.addWidget(self._load_button, 0, 1)

        self.setWindowTitle(self._lang['title']['edit' if data else 'open'])

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
        lang = self._lang['QSlidingStackedWidget']['general']
        widget = QScrollableGridWidget()
        widget.scroll_layout.setSpacing(0)
        widget.scroll_layout.setContentsMargins(0, 0, 16, 0)

        root_frame = QGridFrame()
        root_frame.grid_layout.setSpacing(16)
        root_frame.grid_layout.setContentsMargins(0, 0, 0, 0)
        widget.scroll_layout.addWidget(root_frame, 0, 0)
        widget.scroll_layout.setAlignment(root_frame, Qt.AlignmentFlag.AlignTop)


        label = OpenProjectDialog._text_group(lang['QLabel']['name']['title'], lang['QLabel']['name']['description'])
        root_frame.grid_layout.addWidget(label, root_frame.grid_layout.count(), 0)

        self.name_entry = QNamedLineEdit(None, '', lang['QNamedLineEdit']['name'])
        self.name_entry.setText(self._data['name'] if self._data else 'Project')
        root_frame.grid_layout.addWidget(self.name_entry, root_frame.grid_layout.count(), 0)


        return widget



    def _menu_icon(self) -> QWidget:
        lang = self._lang['QSlidingStackedWidget']['icon']

        self.raw_icon = self._data['icon'] if self._data else os.path.abspath('./data/icons/questionMark.svg')

        widget = QGridFrame()
        widget.grid_layout.setSpacing(16)
        widget.grid_layout.setContentsMargins(0, 0, 0, 0)

        root_frame = QGridFrame()
        root_frame.grid_layout.setSpacing(16)
        root_frame.grid_layout.setContentsMargins(0, 0, 16, 0)
        widget.grid_layout.addWidget(root_frame, 0, 0)
        widget.grid_layout.setAlignment(root_frame, Qt.AlignmentFlag.AlignTop)

        widget.top = QGridFrame()
        widget.top.grid_layout.setSpacing(16)
        widget.top.grid_layout.setContentsMargins(0, 0, 0, 0)
        root_frame.grid_layout.addWidget(widget.top, root_frame.grid_layout.count(), 0)

        label = OpenProjectDialog._text_group(lang['QLabel']['icon']['title'], lang['QLabel']['icon']['description'])
        widget.top.grid_layout.addWidget(label, 0, 0, 1, 2)

        widget.top.icon_group = self.icon_with_text(self.raw_icon, lang['QLabel']['currentIcon'])
        widget.top.grid_layout.addWidget(widget.top.icon_group, 1, 0)

        self.icon_button = QFileButton(
            self, lang['QFileButton']['icon'],
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


        label = OpenProjectDialog._text_group(lang['QLabel']['predefinedIcons']['title'], lang['QLabel']['predefinedIcons']['description'])
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
        loader_data = self._data['data'].get(ProjectKeys.Loader.value, None) if self._data else None

        lang = self._lang['QSlidingStackedWidget']['loader']
        widget = QScrollableGridWidget()
        widget.scroll_layout.setSpacing(0)
        widget.scroll_layout.setContentsMargins(0, 0, 16, 0)

        root_frame = QGridFrame()
        root_frame.grid_layout.setSpacing(16)
        root_frame.grid_layout.setContentsMargins(0, 0, 0, 0)
        widget.scroll_layout.addWidget(root_frame, 0, 0)
        widget.scroll_layout.setAlignment(root_frame, Qt.AlignmentFlag.AlignTop)


        label = OpenProjectDialog._text_group(lang['QLabel']['loaderFile']['title'], lang['QLabel']['loaderFile']['description'])
        root_frame.grid_layout.addWidget(label, root_frame.grid_layout.count(), 0)

        kw = ('edit' if loader_data else 'open') + 'LoaderFile'
        l = {
            "title": lang['QFileButton'][kw]['title'],
            "dialog": lang['QFileButton'][kw]['dialog']
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


        return widget



    def _menu_kamek(self) -> QWidget:
        kamek_data = self._data['data'].get(ProjectKeys.Kamek.value, None) if self._data else None

        lang = self._lang['QSlidingStackedWidget']['kamek']
        widget = QScrollableGridWidget()
        widget.scroll_layout.setSpacing(0)
        widget.scroll_layout.setContentsMargins(0, 0, 16, 0)

        root_frame = QGridFrame()
        root_frame.grid_layout.setSpacing(16)
        root_frame.grid_layout.setContentsMargins(0, 0, 0, 0)
        widget.scroll_layout.addWidget(root_frame, 0, 0)
        widget.scroll_layout.setAlignment(root_frame, Qt.AlignmentFlag.AlignTop)


        label = OpenProjectDialog._text_group(lang['QLabel']['kamekFile']['title'], lang['QLabel']['kamekFile']['description'])
        root_frame.grid_layout.addWidget(label, root_frame.grid_layout.count(), 0)

        kw = ('edit' if kamek_data else 'open') + 'KamekFile'
        l = {
            "title": lang['QFileButton'][kw]['title'],
            "dialog": lang['QFileButton'][kw]['dialog']
        }

        self.kamek_file_button = QFileButton(
            None,
            l,
            kamek_data['path'] if kamek_data else None,
            self._open_file_icon,
            QFiles.Dialog.OpenFileName,
            'All supported files (*.yaml *.yml);;YAML (*.yaml *.yml)'
        )
        self.kamek_file_button.setFixedWidth(350)
        root_frame.grid_layout.addWidget(self.kamek_file_button, root_frame.grid_layout.count(), 0)
        root_frame.grid_layout.setAlignment(self.kamek_file_button, Qt.AlignmentFlag.AlignLeft)


        return widget



    def _menu_reggienext(self) -> QWidget:
        reggienext_data = self._data['data'].get(ProjectKeys.ReggieNext.value, None) if self._data else None

        lang = self._lang['QSlidingStackedWidget']['reggieNext']
        widget = QScrollableGridWidget()
        widget.scroll_layout.setSpacing(0)
        widget.scroll_layout.setContentsMargins(0, 0, 16, 0)

        root_frame = QGridFrame()
        root_frame.grid_layout.setSpacing(16)
        root_frame.grid_layout.setContentsMargins(0, 0, 0, 0)
        widget.scroll_layout.addWidget(root_frame, 0, 0)
        widget.scroll_layout.setAlignment(root_frame, Qt.AlignmentFlag.AlignTop)


        label = OpenProjectDialog._text_group(lang['QLabel']['reggieNextFolder']['title'], lang['QLabel']['reggieNextFolder']['description'])
        root_frame.grid_layout.addWidget(label, root_frame.grid_layout.count(), 0)

        kw = ('edit' if reggienext_data else 'open') + 'ReggieNextFolder'
        l = {
            "title": lang['QFileButton'][kw]['title'],
            "dialog": lang['QFileButton'][kw]['dialog']
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
        riivolution_data = self._data['data'].get(ProjectKeys.Riivolution.value, None) if self._data else None

        lang = self._lang['QSlidingStackedWidget']['riivolution']
        widget = QScrollableGridWidget()
        widget.scroll_layout.setSpacing(0)
        widget.scroll_layout.setContentsMargins(0, 0, 16, 0)

        root_frame = QGridFrame()
        root_frame.grid_layout.setSpacing(16)
        root_frame.grid_layout.setContentsMargins(0, 0, 0, 0)
        widget.scroll_layout.addWidget(root_frame, 0, 0)
        widget.scroll_layout.setAlignment(root_frame, Qt.AlignmentFlag.AlignTop)


        label = OpenProjectDialog._text_group(lang['QLabel']['riivolutionFile']['title'], lang['QLabel']['riivolutionFile']['description'])
        root_frame.grid_layout.addWidget(label, root_frame.grid_layout.count(), 0)

        kw = ('edit' if riivolution_data else 'open') + 'RiivolutionFile'
        l = {
            "title": lang['QFileButton'][kw]['title'],
            "dialog": lang['QFileButton'][kw]['dialog']
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

    def reject(self) -> None:
        if self._root.current_index == 0:
            return super().reject()
        self._root.slide_in_previous()
        self._update_keywords()

    def _update_keywords(self) -> None:
        if self._root.current_index < self._root.count() - 1:
            self._load_button.setText(self._lang['QPushButton']['next'])
        else:
            self._load_button.setText(self._lang['QPushButton']['load'])

        if self._root.current_index == 0:
            self._cancel_button.setText(self._lang['QPushButton']['cancel'])
        else:
            self._cancel_button.setText(self._lang['QPushButton']['back'])

    def _get_loader(self) -> dict | None:
        if self.loader_file_button.path() in ['', '.', './']: return None

        return {
            'path': self.loader_file_button.path()
        }
    
    def _get_kamek(self) -> dict | None:
        if self.kamek_file_button.path() in ['', '.', './']: return None

        return {
            'path': self.kamek_file_button.path()
        }
    
    def _get_reggienext(self) -> dict | None:
        if self.reggie_folder_button.path() in ['', '.', './']: return None

        return {
            'path': self.reggie_folder_button.path()
        }
    
    def _get_riivolution(self) -> dict | None:
        if self.riivolution_file_button.path() in ['', '.', './']: return None

        return {
            'path': self.riivolution_file_button.path()
        }


    def exec(self) -> dict | None:
        if super().exec():
            return {
                'name': self.name_entry.text() if self.name_entry.text() else 'Project',
                'icon': self.icon_button.path() if self.icon_button.path() not in ['', '.', './'] else None,
                'data': {
                    ProjectKeys.Loader.value: self._get_loader(),
                    ProjectKeys.Kamek.value: self._get_kamek(),
                    ProjectKeys.ReggieNext.value: self._get_reggienext(),
                    ProjectKeys.Riivolution.value: self._get_riivolution()
                }
            }
        return None
#----------------------------------------------------------------------
