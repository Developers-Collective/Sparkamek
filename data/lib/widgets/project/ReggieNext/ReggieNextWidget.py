#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QDockWidget
from PySide6.QtCore import Qt
from ..SubProjectWidgetBase import SubProjectWidgetBase
from data.lib.qtUtils import QBaseApplication
from data.lib.widgets.ProjectKeys import ProjectKeys
from .SpriteListDockWidget import SpriteListDockWidget
#----------------------------------------------------------------------

    # Class
class ReggieNextWidget(SubProjectWidgetBase):
    type: ProjectKeys = ProjectKeys.ReggieNext

    _lang = {}

    def init(app: QBaseApplication) -> None:
        ReggieNextWidget._lang = app.get_lang_data('QMainWindow.QSlidingStackedWidget.mainMenu.projects.ReggieNextWidget')

        SpriteListDockWidget.init(app)

    def __init__(self, app: QBaseApplication, name: str, icon: str, data: dict) -> None:
        super().__init__(app, data)

        self.scroll_layout.setSpacing(20)

        dockwidgets = data.get('dockwidgets', {})

        self._sprite_list_dock_widget = SpriteListDockWidget(app, name, icon, data)

        if 'spriteList' in dockwidgets: self._sprite_list_dock_widget.load_dict(self, dockwidgets['spriteList'])
        else: self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self._sprite_list_dock_widget)


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
#----------------------------------------------------------------------
