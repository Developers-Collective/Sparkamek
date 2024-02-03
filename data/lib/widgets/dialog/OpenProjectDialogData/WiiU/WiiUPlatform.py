#----------------------------------------------------------------------

    # Libraries
from ..Platform import Platform
from ..PlatformFactory import PlatformFactory
#----------------------------------------------------------------------

    # Class
class WiiUPlatform(Platform):
    def __init__(self) -> None:
        super().__init__('WiiU', './data/icons/utils/WiiU/icon.svg', None)
#----------------------------------------------------------------------

    # Register
PlatformFactory.register('WiiU', WiiUPlatform)
#----------------------------------------------------------------------
