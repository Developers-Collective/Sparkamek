#----------------------------------------------------------------------

    # Libraries
from .SubProjectWidgetBase import SubProjectWidgetBase
from data.lib.qtUtils import QBaseApplication
from data.lib.widgets.ProjectKeys import ProjectKeys
#----------------------------------------------------------------------

    # Class
class RiivolutionWidget(SubProjectWidgetBase):
    type: ProjectKeys = ProjectKeys.Riivolution

    def __init__(self, app: QBaseApplication, name: str, icon: str, data: dict) -> None:
        super().__init__(app, data)
#----------------------------------------------------------------------
