#----------------------------------------------------------------------

    # Libraries
from interface import Interface
from data.lib.storage import XMLNode
#----------------------------------------------------------------------

    # Class
class IBaseItem(Interface):
    def __init__(self, data: XMLNode = None) -> None: pass

    def export(self) -> XMLNode: pass

    def copy(self) -> 'IBaseItem': pass

    @staticmethod
    def create() -> 'IBaseItem': pass
#----------------------------------------------------------------------
