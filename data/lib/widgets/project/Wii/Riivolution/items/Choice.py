#----------------------------------------------------------------------

    # Libraries
from interface import implements
from data.lib.storage import XMLNode
from .IBaseItem import IBaseItem
from .PatchRef import PatchRef
#----------------------------------------------------------------------

    # Class
class Choice(implements(IBaseItem)):
    name: str = 'choice'

    def __init__(self, data: XMLNode = None) -> None:
        if not data: data = self.create().export()

        self.name_: str = data.get_attribute('name', 'Choice Name') # Required

        self.patchref_children: list[PatchRef] = [PatchRef(p) for p in data.get_children(PatchRef.name) if p]

    def export(self) -> XMLNode:
        return XMLNode(
            self.name,
            {'name': self.name_},
            [p.export() for p in self.patchref_children]
        )

    def copy(self) -> 'Choice':
        return Choice(self.export())

    @staticmethod
    def create() -> 'Choice':
        return Choice(XMLNode(Choice.name))
#----------------------------------------------------------------------
