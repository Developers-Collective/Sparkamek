#----------------------------------------------------------------------

    # Libraries
from PyQt6.QtWidgets import QLabel, QFrame
from PyQt6.QtCore import Qt
from data.lib.qtUtils import QLangData, QGridFrame, QFileButton, QFiles, QBaseApplication
from data.lib.widgets.project import ProjectKeys
from ..BaseWidget import BaseWidget
#----------------------------------------------------------------------

    # Class
class RiivolutionWidget(BaseWidget):
    _lang: QLangData = QLangData.NoTranslation()

    _open_file_icon: str = ''

    _has_been_initialized: bool = False


    @staticmethod
    def init(app: QBaseApplication) -> None:
        if RiivolutionWidget._has_been_initialized: return

        RiivolutionWidget._lang = app.get_lang_data('OpenProjectDialog.Wii.Riivolution')
        RiivolutionWidget._color_link = app.COLOR_LINK
        RiivolutionWidget._open_file_icon = f'{app.save_data.get_icon_dir()}filebutton/file.png'

        RiivolutionWidget._has_been_initialized = True


    def __init__(self, data: dict) -> None:
        super().__init__()

        riivolution_data: dict = data['data'].get(ProjectKeys.Wii.Riivolution, None) if data else None

        lang = self._lang.get('QSlidingStackedWidget.riivolution')

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


        label = self._text_group(lang.get('QLabel.riivolutionFile.title'), lang.get('QLabel.riivolutionFile.description'))
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


    def get(self) -> dict | None:
        if self.riivolution_file_button.path() in self._forbidden_paths: return None

        return {
            'path': self.riivolution_file_button.path()
        }
#----------------------------------------------------------------------
