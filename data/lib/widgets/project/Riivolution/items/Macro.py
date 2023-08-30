#----------------------------------------------------------------------

    # Libraries
from interface import implements
from data.lib.storage import XMLNode
from .IBaseItem import IBaseItem
from .Param import Param
#----------------------------------------------------------------------

    # Class
class Macro(implements(IBaseItem)):
    name: str = 'macro'

    def __init__(self, data: XMLNode = None) -> None:
        if not data: data = self.create().export()

        self.id = data.get_attribute('id', 'optionid') # Required
        self.name = data.get_attribute('name', 'Option Name') # Required

        self.param_children: list[Param] = data.get_children(Param.name)

    def export(self) -> XMLNode:
        return XMLNode(
            self.name,
            (
                {'id': self.id} |
                {'name': self.name}
            ),
            [p.export() for p in self.param_children]
        )

    def copy(self) -> 'Macro':
        return Macro(self.export())

    @staticmethod
    def create() -> 'Macro':
        return Macro(XMLNode(Macro.name))
#----------------------------------------------------------------------
