#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QDockWidget, QPushButton
from PySide6.QtCore import Qt
from ..SubProjectWidgetBase import SubProjectWidgetBase
from data.lib.qtUtils import QBaseApplication, QGridWidget, QSaveData
from data.lib.widgets.ProjectKeys import ProjectKeys
from .SpriteListDockWidget import SpriteListDockWidget
from .sprites.Sprite import Sprite
from data.lib.storage.xml import XMLNode
#----------------------------------------------------------------------

    # Class
class ReggieNextWidget(SubProjectWidgetBase):
    type: ProjectKeys = ProjectKeys.ReggieNext

    _clear_icon = None
    _reset_icon = None
    _create_icon = None
    _delete_icon = None

    _lang = {}

    def init(app: QBaseApplication) -> None:
        ReggieNextWidget._lang = app.get_lang_data('QMainWindow.QSlidingStackedWidget.mainMenu.projects.ReggieNextWidget')
        ReggieNextWidget._clear_icon = app.get_icon('pushbutton/clear.png', True, QSaveData.IconMode.Local)
        ReggieNextWidget._reset_icon = app.get_icon('pushbutton/reset.png', True, QSaveData.IconMode.Local)
        ReggieNextWidget._create_icon = app.get_icon('pushbutton/create.png', True, QSaveData.IconMode.Local)
        ReggieNextWidget._delete_icon = app.get_icon('pushbutton/delete.png', True, QSaveData.IconMode.Local)

        SpriteListDockWidget.init(app)

    def __init__(self, app: QBaseApplication, name: str, icon: str, data: dict) -> None:
        super().__init__(app, data)

        self.scroll_layout.setSpacing(20)

        dockwidgets = data.get('dockwidgets', {})

        self._sprite_list_dock_widget = SpriteListDockWidget(app, name, icon, data)
        self._sprite_list_dock_widget.selected_sprite_changed.connect(self._sprite_selection_changed)

        if 'spriteList' in dockwidgets: self._sprite_list_dock_widget.load_dict(self, dockwidgets['spriteList'])
        else: self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self._sprite_list_dock_widget)


        self._current_sprite: Sprite = None
        self._prev_info = None
        self._sprite_modified = False


        topframe = QGridWidget()
        topframe.grid_layout.setContentsMargins(0, 0, 0, 0)
        topframe.grid_layout.setSpacing(8)
        self._root.scroll_layout.addWidget(topframe, 0, 0, Qt.AlignmentFlag.AlignTop)

        self._create_button = QPushButton(self._lang.get_data('QPushButton.create'))
        self._create_button.setIcon(self._create_icon)
        self._create_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self._create_button.setProperty('icon-padding', True)
        self._create_button.setProperty('color', 'main')
        self._create_button.clicked.connect(self._create)
        topframe.grid_layout.addWidget(self._create_button, 0, 0, Qt.AlignmentFlag.AlignLeft)

        self._delete_button = QPushButton(self._lang.get_data('QPushButton.delete'))
        self._delete_button.setIcon(self._delete_icon)
        self._delete_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self._delete_button.setProperty('icon-padding', True)
        self._delete_button.setProperty('color', 'main')
        self._delete_button.clicked.connect(self._delete)
        self._delete_button.setEnabled(False)
        topframe.grid_layout.addWidget(self._delete_button, 0, 1, Qt.AlignmentFlag.AlignRight)


        topframe = QGridWidget()
        topframe.grid_layout.setContentsMargins(0, 0, 0, 0)
        topframe.grid_layout.setSpacing(8)
        self._root.scroll_layout.addWidget(topframe, 1, 0, Qt.AlignmentFlag.AlignTop)

        self._reset_button = QPushButton(self._lang.get_data('QPushButton.reset'))
        self._reset_button.setIcon(self._reset_icon)
        self._reset_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self._reset_button.setProperty('icon-padding', True)
        self._reset_button.setProperty('color', 'main')
        self._reset_button.clicked.connect(self._reset)
        topframe.grid_layout.addWidget(self._reset_button, 0, 0, Qt.AlignmentFlag.AlignLeft)

        self._clear_button = QPushButton(self._lang.get_data('QPushButton.clear'))
        self._clear_button.setIcon(self._clear_icon)
        self._clear_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self._clear_button.setProperty('icon-padding', True)
        self._clear_button.setProperty('color', 'main')
        self._clear_button.clicked.connect(self._clear)
        topframe.grid_layout.addWidget(self._clear_button, 0, 1, Qt.AlignmentFlag.AlignRight)


    @property
    def task_is_running(self) -> bool:
        return False


    def _save_dock_widgets(self) -> dict:
        self._sprite_list_dock_widget.terminate_task()

        dockwidgets = {}

        for dw in self.findChildren(QDockWidget):
            dockwidgets[dw.objectName()] = dw.to_dict()

        return dockwidgets


    def reset_dock_widgets(self) -> None:
        for dw in [self._sprite_list_dock_widget]:
            dw.setVisible(True)
            dw.setFloating(False)

        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self._sprite_list_dock_widget)


    def export(self) -> dict:
        return super().export()


    def _set_sprite(self, sprite: Sprite | None) -> None:
        self._current_sprite = sprite
        self._prev_info = (sprite.id, sprite.name) if sprite is not None else None
        self._draw_current_sprite()
        self._update_buttons()


    def _draw_current_sprite(self) -> None:
        print('draw current sprite', self._current_sprite.name if self._current_sprite else None)


    def _update_buttons(self) -> None:
        self._delete_button.setEnabled(self._current_sprite is not None)


    def _create(self) -> None:
        if self._current_sprite is not None: self._save_current_sprite()
        self._sprite_list_dock_widget.deselect_sprite()

        self._current_sprite = Sprite(XMLNode('sprite', {'id': 0, 'name': 'New Sprite'}, [], None))
        self._prev_info = None
        self._sprite_modified = True

        self._draw_current_sprite()
        self._update_buttons()

    def _delete(self) -> None:
        if self._prev_info: self._sprite_list_dock_widget.delete_sprite(self._prev_info)

    def _reset(self) -> None:
        pass

    def _clear(self) -> None:
        pass

    def _save_current_sprite(self) -> None:
        if not self._sprite_modified: return
        if self._current_sprite is None: return

        self._sprite_modified = False

        if self._prev_info is None: self._sprite_list_dock_widget.update_sprite((self._current_sprite.id, self._current_sprite.name), self._current_sprite)
        else: self._sprite_list_dock_widget.update_sprite(self._prev_info, self._current_sprite)

        self._current_sprite = None
        self._prev_info = None

        self._update_buttons()


    def _sprite_selection_changed(self, selected: Sprite | None, deselected: Sprite | None) -> None:
        if deselected: self._save_current_sprite()
        if not deselected and self._current_sprite is not None: self._save_current_sprite()

        self._set_sprite(selected)
#----------------------------------------------------------------------
