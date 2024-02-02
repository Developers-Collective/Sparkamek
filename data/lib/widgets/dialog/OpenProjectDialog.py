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

    _open_image_icon: str = ''


    _icon_path = os.path.abspath('./data/icons/sample/')

    _forbidden_paths = (
        None,
        '',
        '.',
        './'
    )

    @staticmethod
    def init(app: QBaseApplication) -> None:
        OpenProjectDialog._lang = app.get_lang_data('OpenProjectDialog')
        OpenProjectDialog._open_image_icon = f'{app.save_data.get_icon_dir()}filebutton/image.png'


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

        # self._pages['general'] = self._menu_general()
        # self._root.addWidget(self._pages['general'])

        # self._pages['icon'] = self._menu_icon()
        # self._root.addWidget(self._pages['icon'])

        # self._pages['loader'] = self._menu_loader()
        # self._root.addWidget(self._pages['loader'])

        # self._pages['kamek'] = self._menu_kamek()
        # self._root.addWidget(self._pages['kamek'])

        # self._pages['reggienext'] = self._menu_reggienext()
        # self._root.addWidget(self._pages['reggienext'])

        # self._pages['riivolution'] = self._menu_riivolution()
        # self._root.addWidget(self._pages['riivolution'])

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


    def exec(self) -> dict | None:
        if super().exec():
            data = {
                # 'name': self.name_entry.text() if self.name_entry.text() else 'Project',
                # 'icon': self.icon_button.path() if self.icon_button.path() not in self._forbidden_paths else None,
                # 'data': {
                #     ProjectKeys.Wii.NSMBW.Loader: self._get_loader(),
                #     ProjectKeys.Wii.NSMBW.Kamek: self._get_kamek(),
                #     ProjectKeys.Wii.NSMBW.ReggieNext: self._get_reggienext(),
                #     ProjectKeys.Wii.Riivolution: self._get_riivolution()
                # }
            }
            return data if any(data['data'].values()) else None
        return None
#----------------------------------------------------------------------
