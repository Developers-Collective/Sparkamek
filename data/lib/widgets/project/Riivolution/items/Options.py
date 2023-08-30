#----------------------------------------------------------------------

    # Libraries
from interface import implements
from data.lib.storage import XMLNode
from .IBaseItem import IBaseItem
#----------------------------------------------------------------------

    # Class
class Options(implements(IBaseItem)):
    name: str = 'options'

    def __init__(self, data: XMLNode = None) -> None:
        if not data: data = self.create().export()

    def export(self) -> XMLNode:
        return XMLNode(
            self.name
        )

    def copy(self) -> 'Options':
        return Options(self.export())

    @staticmethod
    def create() -> 'Options':
        return Options(XMLNode(Options.name))
#----------------------------------------------------------------------
