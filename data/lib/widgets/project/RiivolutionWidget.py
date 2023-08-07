#----------------------------------------------------------------------

    # Libraries
from .SubProjectWidgetBase import SubProjectWidgetBase
from data.lib.qtUtils import QBaseApplication
#----------------------------------------------------------------------

    # Class
class RiivolutionWidget(SubProjectWidgetBase):
    def __init__(self, app: QBaseApplication, name: str, icon: str, data: dict) -> None:
        super().__init__(app, data)
#----------------------------------------------------------------------
