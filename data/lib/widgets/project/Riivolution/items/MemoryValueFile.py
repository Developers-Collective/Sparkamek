#----------------------------------------------------------------------

    # Libraries
from interface import implements
from data.lib.storage import XMLNode
from .IBaseItem import IBaseItem
#----------------------------------------------------------------------

    # Class
class MemoryValueFile(implements(IBaseItem)):
    name: str = 'memory'
    key: str = 'memoryvaluefile'

    def __init__(self, data: XMLNode = None) -> None:
        if not data: data = self.create().export()

        self.offset: int = data.get_attribute('offset', 0) # Required
        self.valuefile: str = data.get_attribute('valuefile', '/file.bin') # Required
        self.comment: str = data.get_attribute('comment', '') # Optional

    def export(self) -> XMLNode:
        return XMLNode(
            self.name,
            (
                {'offset': self.offset} |
                {('valuefile'): self.valuefile} |
                ({'comment': self.comment} if self.comment else {})
            )
        )

    def copy(self) -> 'MemoryValueFile':
        return MemoryValueFile(self.export())

    @staticmethod
    def create() -> 'MemoryValueFile':
        return MemoryValueFile(XMLNode(MemoryValueFile.name))
#----------------------------------------------------------------------
