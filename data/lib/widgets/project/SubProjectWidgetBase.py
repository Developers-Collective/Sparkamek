#----------------------------------------------------------------------

    # Libraries
from data.lib.qtUtils import QSubScrollableGridMainWindow, QBaseApplication
#----------------------------------------------------------------------

    # Class
class SubProjectWidgetBase(QSubScrollableGridMainWindow):
    def __init__(self, app: QBaseApplication, data: dict) -> None:
        super().__init__(app)

        self.scroll_layout.setContentsMargins(16, 16, 16, 16)
        self.scroll_layout.setSpacing(8)

        self._path = data['path']

    @property
    def path(self) -> str:
        return self._path

    def export(self) -> dict:
        return {
            'path': self._path
        }
#----------------------------------------------------------------------
