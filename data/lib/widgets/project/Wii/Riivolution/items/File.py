#----------------------------------------------------------------------

    # Libraries
from interface import implements
from data.lib.storage import XMLNode
from .IBaseItem import IBaseItem
#----------------------------------------------------------------------

    # Class
class File(implements(IBaseItem)):
    name: str = 'file'

    def __init__(self, data: XMLNode = None) -> None:
        if not data: data = self.create().export()

        self.disc: str = data.get_attribute('disc', '/file') # Required
        self.external: str = data.get_attribute('external', 'file') # Required
        self.resize: bool = data.get_attribute('resize', True) # Optional
        self.create_: bool = data.get_attribute('create', False) # Optional
        self.offset: int = int(data.get_attribute('offset', 0)) # Optional
        self.length: int = int(data.get_attribute('length', 0)) # Optional

    def export(self) -> XMLNode:
        return XMLNode(
            self.name,
            (
                ({'disc': self.disc}) |
                {'external': self.external} |
                ({'resize': self.resize} if not self.resize else {}) |
                ({'create': self.create_} if self.create_ else {}) |
                ({'offset': self.offset} if self.offset else {}) |
                ({'length': self.length} if self.length else {})
            )
        )

    def copy(self) -> 'File':
        return File(self.export())

    @staticmethod
    def create() -> 'File':
        return File(XMLNode(File.name))
#----------------------------------------------------------------------
