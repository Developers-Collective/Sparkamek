#----------------------------------------------------------------------

    # Libraries
from ..Platform import Platform
from ..PlatformFactory import PlatformFactory
#----------------------------------------------------------------------

    # Class
class SwitchPlatform(Platform):
    def __init__(self) -> None:
        super().__init__('Switch', './data/icons/utils/Switch/icon.svg', None)
#----------------------------------------------------------------------

    # Register
PlatformFactory.register('Switch', SwitchPlatform)
#----------------------------------------------------------------------
