#----------------------------------------------------------------------

    # Libraries
from .SubProjectWidgetBase import SubProjectWidgetBase
from data.lib.qtUtils import QBaseApplication
#----------------------------------------------------------------------

    # Class
class ReggieNextWidget(SubProjectWidgetBase):
    def __init__(self, app: QBaseApplication, data: dict) -> None:
        super().__init__(app, data)
#----------------------------------------------------------------------
