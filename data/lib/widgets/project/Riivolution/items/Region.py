#----------------------------------------------------------------------

    # Libraries
from interface import implements
from data.lib.storage import XMLNode
from .IBaseItem import IBaseItem
#----------------------------------------------------------------------

    # Class
class Region(implements(IBaseItem)):
    name: str = 'region'

    def __init__(self, data: XMLNode = None) -> None:
        if not data: data = self.create().export()

        self.type = data.get_attribute('type', 'P') # Required

    def export(self) -> XMLNode:
        return XMLNode(
            self.name,
            (
                {'type': self.type}
            )
        )

    def copy(self) -> 'Region':
        return Region(self.export())

    @staticmethod
    def create() -> 'Region':
        return Region(XMLNode(Region.name, attributes = {'type': 'P'}))
#----------------------------------------------------------------------
