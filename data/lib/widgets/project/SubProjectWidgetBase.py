#----------------------------------------------------------------------

    # Libraries
from data.lib.qtUtils import QSubScrollableGridMainWindow, QBaseApplication, QSaveData
from data.lib.widgets.ProjectKeys import ProjectKeys
#----------------------------------------------------------------------

    # Class
class SubProjectWidgetBase(QSubScrollableGridMainWindow):
    type: ProjectKeys = None

    def init(app: QBaseApplication) -> None:
        pass

    def __init__(self, app: QBaseApplication, data: dict) -> None:
        super().__init__(app)

        if not self.type: raise NotImplementedError('SubProjectWidgetBase.type must be set')

        self.scroll_layout.setContentsMargins(16, 16, 16, 16)
        self.scroll_layout.setSpacing(8)

        self._path = data['path']

    @property
    def path(self) -> str:
        return self._path

    def export(self) -> dict:
        return {
            'path': self._path,
            'dockwidgets': self._save_dock_widgets()
        }

    @property
    def task_is_running(self) -> bool:
        return False

    def _save_dock_widgets(self) -> dict:
        return {}

    def reset_dock_widgets(self) -> None:
        pass

    def settings_updated(self, settings: QSaveData) -> None:
        pass
#----------------------------------------------------------------------
