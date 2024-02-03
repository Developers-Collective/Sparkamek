#----------------------------------------------------------------------

    # Libraries
from data.lib.qtUtils import QBaseApplication
from ...Game import Game
from ..WiiUGameFactory import WiiUGameFactory
from .NSMBU import NSMBU
#----------------------------------------------------------------------

    # Class
class NSMBUGame(Game):
    @staticmethod
    def init(app: QBaseApplication) -> None:
        NSMBU.init(app)

    def __init__(self) -> None:
        super().__init__('WiiU.NSMBU', './data/icons/utils/WiiU/NSMBU/icon.svg', NSMBU)
#----------------------------------------------------------------------

    # Register
WiiUGameFactory.register('WiiU.NSMBU', NSMBUGame)
#----------------------------------------------------------------------
