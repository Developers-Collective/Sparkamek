#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QPushButton
from ..SubProjectWidgetBase import SubProjectWidgetBase
from data.lib.qtUtils import QBaseApplication
from data.lib.widgets.ProjectKeys import ProjectKeys
#----------------------------------------------------------------------

    # Class
class LoaderWidget(SubProjectWidgetBase):
    type: ProjectKeys = ProjectKeys.Loader

    def __init__(self, app: QBaseApplication, name: str, icon: str, data: dict) -> None:
        super().__init__(app, data)
#----------------------------------------------------------------------
