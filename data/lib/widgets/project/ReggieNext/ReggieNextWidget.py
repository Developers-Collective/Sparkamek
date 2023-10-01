#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QDockWidget, QPushButton, QFileDialog
from PySide6.QtCore import Qt
from ..SubProjectWidgetBase import SubProjectWidgetBase
from data.lib.qtUtils import QBaseApplication, QGridWidget, QSaveData
from data.lib.widgets.ProjectKeys import ProjectKeys
from .SpriteListDockWidget import SpriteListDockWidget
from .ItemDataPropertyDockWidget import ItemDataPropertyDockWidget
from .SpriteWidget import SpriteWidget
from .sprites.Sprite import Sprite
from .ImportDialog import ImportDialog
from data.lib.storage.xml import XML, XMLNode
import os, traceback
#----------------------------------------------------------------------

    # Class
class ReggieNextWidget(SubProjectWidgetBase):
    type: ProjectKeys = ProjectKeys.ReggieNext

    _clear_icon = None
    _reset_icon = None
    _import_icon = None
    _export_icon = None
    _create_icon = None
    _delete_icon = None

    _lang = {}

    def init(app: QBaseApplication) -> None:
        ReggieNextWidget._lang = app.get_lang_data('QMainWindow.QSlidingStackedWidget.mainMenu.projects.ReggieNextWidget')
        ReggieNextWidget._clear_icon = app.get_icon('pushbutton/clear.png', True, QSaveData.IconMode.Local)
        ReggieNextWidget._reset_icon = app.get_icon('pushbutton/reset.png', True, QSaveData.IconMode.Local)
        ReggieNextWidget._import_icon = app.get_icon('pushbutton/import.png', True, QSaveData.IconMode.Local)
        ReggieNextWidget._export_icon = app.get_icon('pushbutton/export.png', True, QSaveData.IconMode.Local)
        ReggieNextWidget._create_icon = app.get_icon('pushbutton/create.png', True, QSaveData.IconMode.Local)
        ReggieNextWidget._delete_icon = app.get_icon('pushbutton/delete.png', True, QSaveData.IconMode.Local)

        SpriteListDockWidget.init(app)
        SpriteWidget.init(app)
        ItemDataPropertyDockWidget.init(app)

    def __init__(self, app: QBaseApplication, name: str, icon: str, data: dict) -> None:
        super().__init__(app, data)

        self.scroll_layout.setSpacing(10)

        dockwidgets = data.get('dockwidgets', {})

        self._sprite_list_dock_widget = SpriteListDockWidget(app, name, icon, data)
        self._sprite_list_dock_widget.selected_sprite_changed.connect(self._sprite_selection_changed)
        self._sprite_list_dock_widget.save_clicked.connect(self._save_clicked)

        self._item_data_property_dock_widget = ItemDataPropertyDockWidget(app, name, icon, data)

        if 'spriteList' in dockwidgets: self._sprite_list_dock_widget.load_dict(self, dockwidgets['spriteList'])
        else: self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self._sprite_list_dock_widget)

        if 'itemDataProperty' in dockwidgets: self._item_data_property_dock_widget.load_dict(self, dockwidgets['itemDataProperty'])
        else: self.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, self._item_data_property_dock_widget)


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

        self._import_button = QPushButton(self._lang.get_data('QPushButton.import'))
        self._import_button.setIcon(self._import_icon)
        self._import_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self._import_button.setProperty('icon-padding', True)
        self._import_button.setProperty('color', 'main')
        self._import_button.clicked.connect(self._import)
        topframe.grid_layout.addWidget(self._import_button, 0, 0, Qt.AlignmentFlag.AlignLeft)

        self._export_button = QPushButton(self._lang.get_data('QPushButton.export'))
        self._export_button.setIcon(self._export_icon)
        self._export_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self._export_button.setProperty('icon-padding', True)
        self._export_button.setProperty('color', 'main')
        self._export_button.clicked.connect(self._export)
        self._export_button.setEnabled(False)
        topframe.grid_layout.addWidget(self._export_button, 0, 1, Qt.AlignmentFlag.AlignRight)


        topframe = QGridWidget()
        topframe.grid_layout.setContentsMargins(0, 0, 0, 0)
        topframe.grid_layout.setSpacing(8)
        self._root.scroll_layout.addWidget(topframe, 2, 0, Qt.AlignmentFlag.AlignTop)

        self._reset_button = QPushButton(self._lang.get_data('QPushButton.reset'))
        self._reset_button.setIcon(self._reset_icon)
        self._reset_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self._reset_button.setProperty('icon-padding', True)
        self._reset_button.setProperty('color', 'main')
        self._reset_button.clicked.connect(self._reset)
        self._reset_button.setEnabled(False)
        topframe.grid_layout.addWidget(self._reset_button, 0, 0, Qt.AlignmentFlag.AlignLeft)

        self._clear_button = QPushButton(self._lang.get_data('QPushButton.clear'))
        self._clear_button.setIcon(self._clear_icon)
        self._clear_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self._clear_button.setProperty('icon-padding', True)
        self._clear_button.setProperty('color', 'main')
        self._clear_button.clicked.connect(self._clear)
        self._clear_button.setEnabled(False)
        topframe.grid_layout.addWidget(self._clear_button, 0, 1, Qt.AlignmentFlag.AlignRight)


        self._sprite_widget = SpriteWidget(self._path)
        self._sprite_widget.sprite_edited.connect(self._sprite_edited)
        self._sprite_widget.current_sprite_changed.connect(self._item_data_property_dock_widget.update_title)
        self._sprite_widget.property_entry_selected.connect(self._item_data_property_dock_widget.set_widget)
        self._root.scroll_layout.addWidget(self._sprite_widget, 3, 0)


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
        self.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, self._item_data_property_dock_widget)


    def export(self) -> dict:
        return super().export()


    def _set_sprite(self, sprite: Sprite | None) -> None:
        self._current_sprite = sprite
        self._prev_info = (sprite.id, sprite.name) if sprite is not None else None
        self._draw_current_sprite()
        self._update_buttons()


    def _draw_current_sprite(self) -> None:
        self._sprite_widget.sprite = self._current_sprite.copy() if self._current_sprite is not None else None


    def _update_buttons(self) -> None:
        self._delete_button.setEnabled(self._current_sprite is not None)
        self._export_button.setEnabled(self._current_sprite is not None)
        self._clear_button.setEnabled(self._current_sprite is not None)
        self._reset_button.setEnabled(self._current_sprite is not None)


    def _create(self) -> None:
        if self._current_sprite is not None: self._save_current_sprite()
        self._sprite_list_dock_widget.deselect_sprite()

        self._current_sprite = Sprite(XMLNode('sprite', {'id': 0, 'name': 'New Sprite'}, [], None))
        self._prev_info = None
        self._sprite_modified = True

        self._draw_current_sprite()
        self._update_buttons()
        self._delete_button.setEnabled(False)
        self._reset_button.setEnabled(False)

    def _delete(self) -> None:
        if self._current_sprite:
            self._save_current_sprite()
            self._sprite_list_dock_widget.delete_sprite(self._current_sprite)

    def _import(self) -> None:
        path = QFileDialog.getOpenFileName(
            parent = self,
            dir = self._path,
            caption = self._lang.get_data('QFileDialog.import'),
            filter = 'XML (*.xml)'
        )[0]

        if not path: return

        try:
            root = XML.parse_file(path).root
            if root.name == 'sprite': ls = [root]
            elif root.name == 'sprites':
                ls = [c for c in root.children if c.name == 'sprite']
                if not ls: raise Exception('Invalid sprite')
            else: raise Exception('Invalid sprite')

            len_ls = len(ls)
            for i, s in enumerate(ls, 1):
                sprite = Sprite(s)
                fixed_sprite = ImportDialog(self._app.window, self._lang.get_data('ImportDialog'), sprite, i, len_ls).exec()

                if not fixed_sprite: return
                self._sprite_list_dock_widget.import_item(fixed_sprite)

        except Exception as e:
            return self._app.show_alert(
                self._app.get_lang_data('QSystemTrayIcon.showMessage.ReggieNextWidget.errorWhileImportingSprite.message').replace('%s', str(e)),
                raise_duration = self._app.ALERT_RAISE_DURATION,
                pause_duration = self._app.ALERT_PAUSE_DURATION,
                fade_duration = self._app.ALERT_FADE_DURATION,
                color = 'main'
            )

    def _export(self) -> None:
        if not self._current_sprite: return

        path = QFileDialog.getSaveFileName(
            parent = self,
            dir = self._path,
            caption = self._lang.get_data('QFileDialog.export'),
            filter = 'XML (*.xml)'
        )[0]

        if not path: return

        try:
            sprite = self._current_sprite.copy()
            sprite.id = 0

            with open(path, 'w', encoding = 'utf-8') as f:
                f.write(f'\t{sprite.export().export()}')

            return self._app.show_alert(
                self._app.get_lang_data('QSystemTrayIcon.showMessage.ReggieNextWidget.successfullyExportedSprite.message').replace('%s', sprite.sprite_name),
                raise_duration = self._app.ALERT_RAISE_DURATION,
                pause_duration = self._app.ALERT_PAUSE_DURATION,
                fade_duration = self._app.ALERT_FADE_DURATION,
                color = 'main'
            )

        except Exception as e:
            return self._app.show_alert(
                self._app.get_lang_data('QSystemTrayIcon.showMessage.ReggieNextWidget.errorWhileExportingSprite.message').replace('%s', str(e)),
                raise_duration = self._app.ALERT_RAISE_DURATION,
                pause_duration = self._app.ALERT_PAUSE_DURATION,
                fade_duration = self._app.ALERT_FADE_DURATION,
                color = 'main'
            )

    def _reset(self) -> None:
        self._sprite_widget.sprite = self._current_sprite.copy() if self._current_sprite is not None else None
        self._sprite_modified = False
        self._delete_button.setEnabled(True)

    def _clear(self) -> None:
        self._sprite_widget.sprite = Sprite(XMLNode('sprite', {'id': 0, 'name': 'New Sprite'}, [], None))
        self._sprite_modified = True
        self._delete_button.setEnabled(False)

    def _save_current_sprite(self) -> None:
        if not self._sprite_modified: return
        if self._current_sprite is None: return

        self._sprite_modified = False
        self._current_sprite = self._sprite_widget.sprite

        if self._prev_info is None: self._sprite_list_dock_widget.update_sprite((self._current_sprite.id, self._current_sprite.name), self._current_sprite)
        else: self._sprite_list_dock_widget.update_sprite(self._prev_info, self._current_sprite)

        self._current_sprite = None
        self._prev_info = None

        self._update_buttons()


    def _sprite_selection_changed(self, selected: Sprite | None, deselected: Sprite | None) -> None:
        if deselected: self._save_current_sprite()
        if not deselected and self._current_sprite is not None: self._save_current_sprite()

        self._set_sprite(selected)


    def _sprite_edited(self) -> None:
        self._sprite_modified = True


    def _save_clicked(self) -> None:
        self._save_current_sprite()
        if not self._sprite_list_dock_widget.sprites.children:
            return self._app.show_alert(
                self._app.get_lang_data('QSystemTrayIcon.showMessage.ReggieNextWidget.cantSaveEmptyData.message'),
                raise_duration = self._app.ALERT_RAISE_DURATION,
                pause_duration = self._app.ALERT_PAUSE_DURATION,
                fade_duration = self._app.ALERT_FADE_DURATION,
                color = 'main'
            )

        try:
            path = f'{self.path}/spritedata.xml'
            if not os.path.exists(f'{path}.bak'):
                os.rename(path, f'{path}.bak')

            with open(path, 'w', encoding = 'utf-8') as f:
                f.write(str(self._sprite_list_dock_widget.sprites.export().export(indent = 2)))

            self._app.show_alert(
                self._app.get_lang_data('QSystemTrayIcon.showMessage.ReggieNextWidget.successfullySaved.message'),
                raise_duration = self._app.ALERT_RAISE_DURATION,
                pause_duration = self._app.ALERT_PAUSE_DURATION,
                fade_duration = self._app.ALERT_FADE_DURATION,
                color = 'main'
            )

        except Exception as e:
            self._app.show_alert(
                self._app.get_lang_data('QSystemTrayIcon.showMessage.ReggieNextWidget.errorWhileSaving.message').replace('%s', str(e)),
                raise_duration = self._app.ALERT_RAISE_DURATION,
                pause_duration = self._app.ALERT_PAUSE_DURATION,
                fade_duration = self._app.ALERT_FADE_DURATION,
                color = 'main'
            )
#----------------------------------------------------------------------
