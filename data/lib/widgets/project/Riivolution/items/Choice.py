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

        self.name: str = data.get_attribute('name', 'Choice Name') # Required

        self.patchref_children: list[PatchRef] = data.get_children(PatchRef.name)

    def export(self) -> XMLNode:
        return XMLNode(
            self.name,
            {'name': self.name},
            [p.export() for p in self.patchref_children]
        )

    def copy(self) -> 'Choice':
        return Choice(self.export())

    @staticmethod
    def create() -> 'Choice':
        return Choice(XMLNode(Choice.name))
#----------------------------------------------------------------------
