#----------------------------------------------------------------------

    # Libraries
from data.lib.qtUtils import QBaseApplication
from ...Game import Game
from ..SwitchGameFactory import SwitchGameFactory
from .SMBWonder import SMBWonder
#----------------------------------------------------------------------

    # Class
class SMBWonderGame(Game):
    @staticmethod
    def init(app: QBaseApplication) -> None:
        SMBWonder.init(app)

    def __init__(self) -> None:
        super().__init__('Switch.SMBWonder', './data/icons/utils/Switch/SMBWonder/icon.png', SMBWonder)
#----------------------------------------------------------------------

    # Register
SwitchGameFactory.register('Switch.SMBWonder', SMBWonderGame)
#----------------------------------------------------------------------
