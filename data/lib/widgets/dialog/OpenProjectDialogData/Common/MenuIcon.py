#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QLabel, QFrame
from PySide6.QtCore import Qt, QSize
from data.lib.QtUtils import QLangData, QGridFrame, QFileButton, QFiles, QBaseApplication, QFlowScrollableWidget, QIconWidget
from .BaseMenu import BaseMenu
import os
#----------------------------------------------------------------------

    # Class
class MenuIcon(BaseMenu):
    _lang: QLangData = QLangData.NoTranslation()

    _open_image_icon: str = ''

    _icon_path = os.path.abspath('./data/icons/sample/')
    _icon_size = 64


    @staticmethod
    def init(app: QBaseApplication) -> None:
        MenuIcon._lang = app.get_lang_data('OpenProjectDialog.QSlidingStackedWidget.icon')
        MenuIcon._open_image_icon = f'{app.save_data.get_icon_dir()}filebutton/image.png'


    def __init__(self, data: dict) -> None:
        super().__init__()

        lang = self._lang

        self.raw_icon = data['icon'] if data else os.path.abspath('./data/icons/questionMark.svg')

        self.layout_.setSpacing(30)
        self.layout_.setContentsMargins(16, 16, 16, 16)

        topframe = QGridFrame()
        topframe.layout_.setSpacing(8)
        topframe.layout_.setContentsMargins(0, 0, 0, 0)
        self.layout_.addWidget(topframe, self.layout_.count(), 0)

        label = QLabel(lang.get('QLabel.title'))
        label.setProperty('h', 1)
        label.setProperty('margin-left', True)
        topframe.layout_.addWidget(label, 0, 0)

        frame = QFrame()
        frame.setProperty('separator', True)
        frame.setFixedHeight(4)
        topframe.layout_.addWidget(frame, 1, 0)

        root_frame = QGridFrame()
        root_frame.layout_.setSpacing(16)
        root_frame.layout_.setContentsMargins(0, 0, 0, 0)
        self.layout_.addWidget(root_frame, self.layout_.count(), 0)
        self.layout_.setAlignment(root_frame, Qt.AlignmentFlag.AlignTop)

        self._top = QGridFrame()
        self._top.layout_.setSpacing(16)
        self._top.layout_.setContentsMargins(0, 0, 0, 0)
        root_frame.layout_.addWidget(self._top, root_frame.layout_.count(), 0)

        label = self._text_group(lang.get('QLabel.icon.title'), lang.get('QLabel.icon.description'))
        self._top.layout_.addWidget(label, 0, 0, 1, 2)

        self._top.icon_group = self.icon_with_text(self.raw_icon, lang.get('QLabel.currentIcon'))
        self._top.layout_.addWidget(self._top.icon_group, 1, 0)

        self.icon_button = QFileButton(
            self, lang.get('QFileButton.icon'),
            self.raw_icon,
            self._open_image_icon,
            QFiles.Dialog.OpenFileName,
            'All supported files (*.svg *.ico *.png *.jpg *.jpeg *.exe *.bat *.sh);;SVG (*.svg);;ICO (*.ico);;PNG (*.png);;JPEG (*.jpg *.jpeg);;Executable (*.exe);;Batch (*.bat);;Shell (*.sh)'
        )
        self.icon_button.path_changed.connect(self._icon_file_button_path_changed)
        self.icon_button.setMinimumWidth(int(self.icon_button.sizeHint().width() * 1.25))
        self._top.layout_.addWidget(self.icon_button, 1, 1)


        frame = QFrame()
        frame.setProperty('border-top', True)
        frame.setFixedHeight(1)
        root_frame.layout_.addWidget(frame, root_frame.layout_.count(), 0)


        label = self._text_group(lang.get('QLabel.predefinedIcons.title'), lang.get('QLabel.predefinedIcons.description'))
        root_frame.layout_.addWidget(label, root_frame.layout_.count(), 0)


        self._bottom = QFlowScrollableWidget()
        self._bottom.layout_.setSpacing(16)
        self._bottom.layout_.setContentsMargins(0, 0, 0, 0)
        root_frame.layout_.addWidget(self._bottom, root_frame.layout_.count(), 0)

        for index, icon in enumerate(['../none.svg'] + os.listdir(self._icon_path)):
            if not icon.endswith('.svg'): continue
            b = self._generate_button(f'{self._icon_path}/{icon}')
            self._bottom.layout_.addWidget(b)

        self._bottom.setFixedHeight(self._bottom.heightMM() + 16) # Cuz weird things happen when resizing the window


    def _generate_button(self, path: str = None) -> QIconWidget:
        button = QIconWidget(None, path, QSize(self._icon_size, self._icon_size))
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

        self.icon_button.setPath(path)
        self._top.icon_group.icon_widget.icon = path


    def _icon_file_button_path_changed(self, path: str = None) -> None:
        if not path: return
        self._update(path)


    def export(self) -> dict:
        return {
            'icon': self.icon_button.path() if self.icon_button.path() not in self._forbidden_paths else None
        }
#----------------------------------------------------------------------
