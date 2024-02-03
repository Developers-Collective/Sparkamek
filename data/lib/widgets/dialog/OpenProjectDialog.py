#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QDialog, QGridLayout, QPushButton
from PySide6.QtCore import Qt
from enum import IntEnum

from data.lib.qtUtils import QGridFrame, QGridWidget, QBaseApplication, QLangData, QProgressIndicatorWidget, QProgressIndicator

from .OpenProjectDialogData.Common import BaseMenu, MenuGeneral, MenuIcon, MenuPlatform, MenuGame, MenuGameInfo
from .OpenProjectDialogData.Platform import Platform
from .OpenProjectDialogData.Game import Game
from .OpenProjectDialogData.GameInfo import GameInfo
#----------------------------------------------------------------------

    # Class
class OpenProjectDialog(QDialog):
    class Menus(IntEnum):
        General = 0
        Icon = 1
        Platform = 2
        Game = 3
        GameInfo = 4


    _lang: QLangData = QLangData.NoTranslation()

    _open_image_icon: str = ''

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

        Platform.init(app)
        Game.init(app)
        GameInfo.init(app)

        MenuGeneral.init(app)
        MenuIcon.init(app)
        MenuPlatform.init(app)
        MenuGame.init(app)


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

        root_frame = QGridFrame()
        root_frame.grid_layout.setSpacing(0)
        root_frame.grid_layout.setContentsMargins(0, 0, 0, 0)

        self._menus: dict[OpenProjectDialog.Menus, BaseMenu] = {
            OpenProjectDialog.Menus.General: MenuGeneral(self._data),
            OpenProjectDialog.Menus.Icon: MenuIcon(self._data),
            OpenProjectDialog.Menus.Platform: MenuPlatform(self._data),
            OpenProjectDialog.Menus.Game: MenuGame(self._data),
            OpenProjectDialog.Menus.GameInfo: MenuGameInfo(self._data),
        }

        self._progress_indicator_widget = QProgressIndicatorWidget(
            None,
            QProgressIndicator.Direction.Top2Bottom,
            False,
            content_margins = (0, 0, 0, 0),
        )
        for menu in self._menus.values():
            menu.can_continue_changed.connect(self._update_continue)
            self._progress_indicator_widget.add_widget(menu)

        root_frame.grid_layout.addWidget(self._progress_indicator_widget, 0, 0)
        self._progress_indicator_widget.set_current_index(0)

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
        self._menus[OpenProjectDialog.Menus.General].update_continue()
        self._update_keywords()


    @property
    def _current_index(self) -> int:
        return self._progress_indicator_widget.current_index()

    @_current_index.setter
    def _current_index(self, value: int) -> None:
        self._progress_indicator_widget.set_current_index(value)
        self._update_keywords()


    def accept(self) -> None:
        if self._current_index == self._progress_indicator_widget.count() - 1:
            return super().accept()

        if self._current_index == OpenProjectDialog.Menus.Platform:
            if self._menus[OpenProjectDialog.Menus.Platform].selected_platform is None:
                return

            factory = self._menus[OpenProjectDialog.Menus.Platform].selected_platform.game_factory
            self._menus[OpenProjectDialog.Menus.Game].set_factory(factory)

        elif self._current_index == OpenProjectDialog.Menus.Game:
            if self._menus[OpenProjectDialog.Menus.Game].selected_game is None:
                return

            game = self._menus[OpenProjectDialog.Menus.Game].selected_game
            self._menus[OpenProjectDialog.Menus.GameInfo].set_game(game.game_info(self._data))

        self._current_index = self._current_index + 1
        self._menus[self._current_index].update_continue()
        self._update_keywords()


    def new_reject(self) -> None:
        if self._current_index == 0:
            return self.reject()
        self._current_index = self._current_index - 1
        self._menus[self._current_index].update_continue()
        self._update_keywords()


    def reject(self) -> None:
        return super().reject()


    def _update_keywords(self) -> None:
        if self._current_index < self._progress_indicator_widget.count() - 1:
            self._load_button.setText(self._lang.get('QPushButton.next'))
        else:
            self._load_button.setText(self._lang.get('QPushButton.load'))

        if self._current_index == 0:
            self._cancel_button.setText(self._lang.get('QPushButton.cancel'))
        else:
            self._cancel_button.setText(self._lang.get('QPushButton.back'))

    def _update_continue(self, can_continue: bool) -> None:
        self._load_button.setEnabled(can_continue)


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
