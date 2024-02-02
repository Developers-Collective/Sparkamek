#----------------------------------------------------------------------

    # Libraries
from interface import implements
from data.lib.storage import XMLNode
from .IBaseItem import IBaseItem
#----------------------------------------------------------------------

    # Class
class PatchRef(implements(IBaseItem)):
    name: str = 'patch'

    def __init__(self, data: XMLNode = None) -> None:
        if not data: data = self.create().export()

        self.id: str = data.get_attribute('id', 'patchid') # Required

    def export(self) -> XMLNode:
        return XMLNode(
            self.name,
            {'id': self.id}
        )

    def copy(self) -> 'PatchRef':
        return PatchRef(self.export())

    @staticmethod
    def create() -> 'PatchRef':
        return PatchRef(XMLNode(PatchRef.name))
#----------------------------------------------------------------------
