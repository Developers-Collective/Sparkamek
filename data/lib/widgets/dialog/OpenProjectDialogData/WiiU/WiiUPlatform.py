#----------------------------------------------------------------------

    # Libraries
from data.lib.QtUtils import QBaseApplication
from ..Platform import Platform
from ..PlatformFactory import PlatformFactory
from .WiiUGameFactory import WiiUGameFactory
#----------------------------------------------------------------------

    # Class
class WiiUPlatform(Platform):
    @staticmethod
    def init(app: QBaseApplication) -> None:
        WiiUGameFactory.init(app)

    def __init__(self) -> None:
        super().__init__('WiiU', './data/icons/utils/WiiU/icon.svg', WiiUGameFactory)
#----------------------------------------------------------------------

    # Register
PlatformFactory.register('WiiU', WiiUPlatform)
#----------------------------------------------------------------------
