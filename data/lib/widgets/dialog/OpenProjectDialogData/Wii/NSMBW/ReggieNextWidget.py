#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QLabel, QFrame
from PySide6.QtCore import Qt
from data.lib.qtUtils import QLangData, QGridFrame, QFileButton, QFiles, QBaseApplication, QLangData
from data.lib.widgets.project import ProjectKeys
from ...BaseWidget import BaseWidget
#----------------------------------------------------------------------

    # Class
class ReggieNextWidget(BaseWidget):
    _lang: QLangData = QLangData.NoTranslation()

    _open_folder_icon: str = ''


    @staticmethod
    def init(app: QBaseApplication) -> None:
        ReggieNextWidget._lang = app.get_lang_data('OpenProjectDialog.game.Wii.NSMBW.reggieNext')
        ReggieNextWidget._open_folder_icon = f'{app.save_data.get_icon_dir()}filebutton/folder.png'


    def __init__(self, data: dict) -> None:
        super().__init__()

        reggienext_data: dict = data['data'].get(ProjectKeys.Wii.NSMBW.ReggieNext, None) if data else None

        lang = self._lang

        self.scroll_layout.setSpacing(30)
        self.scroll_layout.setContentsMargins(0, 0, 16, 0)

        topframe = QGridFrame()
        topframe.grid_layout.setSpacing(8)
        topframe.grid_layout.setContentsMargins(0, 0, 0, 0)
        self.scroll_layout.addWidget(topframe, self.scroll_layout.count(), 0)

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
        self.scroll_layout.addWidget(root_frame, self.scroll_layout.count(), 0)
        self.scroll_layout.setAlignment(root_frame, Qt.AlignmentFlag.AlignTop)


        label = self._text_group(lang.get('QLabel.reggieNextFolder.title'), lang.get('QLabel.reggieNextFolder.description'))
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


    def export(self) -> dict | None:
        if self.reggie_folder_button.path() in self._forbidden_paths: return None

        return {
            'path': self.reggie_folder_button.path()
        }
#----------------------------------------------------------------------
