#----------------------------------------------------------------------

    # Libraries
from interface import implements
from data.lib.storage import XMLNode
from .IBaseItem import IBaseItem
#----------------------------------------------------------------------

    # Class
class Param(implements(IBaseItem)):
    name: str = 'param'

    def __init__(self, data: XMLNode = None) -> None:
        if not data: data = self.create().export()

        self.name: str = data.get_attribute('name', 'Param Name') # Required
        self.value: str = data.get_attribute('value', 'Param Value') # Required

    def export(self) -> XMLNode:
        return XMLNode(
            self.name,
            (
                {'name': self.name} |
                {'value': self.value}
            )
        )

    def copy(self) -> 'Param':
        return Param(self.export())

    @staticmethod
    def create() -> 'Param':
        return Param(XMLNode(Param.name))
#----------------------------------------------------------------------
