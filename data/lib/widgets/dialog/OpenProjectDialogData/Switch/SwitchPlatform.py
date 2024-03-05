#----------------------------------------------------------------------

    # Libraries
from data.lib.QtUtils import QBaseApplication
from ..Platform import Platform
from ..PlatformFactory import PlatformFactory
from .SwitchGameFactory import SwitchGameFactory
#----------------------------------------------------------------------

    # Class
class SwitchPlatform(Platform):
    @staticmethod
    def init(app: QBaseApplication) -> None:
        SwitchGameFactory.init(app)

    def __init__(self) -> None:
        super().__init__('Switch', './data/icons/utils/Switch/icon.svg', SwitchGameFactory)
#----------------------------------------------------------------------

    # Register
PlatformFactory.register('Switch', SwitchPlatform)
#----------------------------------------------------------------------
