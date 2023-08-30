#----------------------------------------------------------------------

    # Libraries
from interface import Interface
from data.lib.storage import XMLNode
#----------------------------------------------------------------------

    # Class
class IBaseSprite(Interface):
    def __init__(self, data: XMLNode) -> None: pass

    def export(self) -> XMLNode: pass

    def copy(self) -> 'IBaseSprite': pass

    @staticmethod
    def create() -> 'IBaseSprite': pass
#----------------------------------------------------------------------
