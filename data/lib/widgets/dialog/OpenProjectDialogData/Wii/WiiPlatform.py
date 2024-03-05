#----------------------------------------------------------------------

    # Libraries
from data.lib.QtUtils import QBaseApplication
from ..Platform import Platform
from ..PlatformFactory import PlatformFactory
from .WiiGameFactory import WiiGameFactory
#----------------------------------------------------------------------

    # Class
class WiiPlatform(Platform):
    @staticmethod
    def init(app: QBaseApplication) -> None:
        WiiGameFactory.init(app)

    def __init__(self) -> None:
        super().__init__('Wii', './data/icons/utils/Wii/icon.svg', WiiGameFactory)
#----------------------------------------------------------------------

    # Register
PlatformFactory.register('Wii', WiiPlatform)
#----------------------------------------------------------------------
