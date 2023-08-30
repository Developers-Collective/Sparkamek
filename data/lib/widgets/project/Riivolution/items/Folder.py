#----------------------------------------------------------------------

    # Libraries
from interface import implements
from data.lib.storage import XMLNode
from .IBaseItem import IBaseItem
#----------------------------------------------------------------------

    # Class
class Folder(implements(IBaseItem)):
    name: str = 'folder'

    def __init__(self, data: XMLNode = None) -> None:
        if not data: data = self.create().export()

        self.disc: str = data.get_attribute('disc', '') # Optional
        self.external: str = data.get_attribute('external', 'folder') # Required
        self.resize: bool = data.get_attribute('resize', True) # Optional
        self.create_: bool = data.get_attribute('create', False) # Optional
        self.recursive: bool = data.get_attribute('recursive', True) # Optional
        self.length: int = int(data.get_attribute('length', 0)) # Optional

    def export(self) -> XMLNode:
        return XMLNode(
            self.name,
            (
                ({'disc': self.disc} if self.disc else {}) |
                {'external': self.external} |
                ({'resize': self.resize} if not self.resize else {}) |
                ({'create': self.create_} if self.create_ else {}) |
                ({'recursive': self.recursive} if not self.recursive else {}) |
                ({'length': self.length} if self.length else {})
            )
        )

    def copy(self) -> 'Folder':
        return Folder(self.export())

    @staticmethod
    def create() -> 'Folder':
        return Folder(XMLNode(Folder.name))
#----------------------------------------------------------------------
