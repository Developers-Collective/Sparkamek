#----------------------------------------------------------------------

    # Libraries
from data.lib.qtUtils import QBaseApplication
from ...Game import Game
from ..WiiGameFactory import WiiGameFactory
from .NSMBW import NSMBW
#----------------------------------------------------------------------

    # Class
class NSMBWGame(Game):
    @staticmethod
    def init(app: QBaseApplication) -> None:
        NSMBW.init(app)

    def __init__(self) -> None:
        super().__init__('Wii.NSMBW', './data/icons/utils/Wii/NSMBW/icon.svg', NSMBW)
#----------------------------------------------------------------------

    # Register
WiiGameFactory.register('Wii.NSMBW', NSMBWGame)
#----------------------------------------------------------------------
