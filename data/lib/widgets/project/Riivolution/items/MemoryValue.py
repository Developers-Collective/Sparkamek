#----------------------------------------------------------------------

    # Libraries
from interface import implements
from data.lib.storage import XMLNode
from .IBaseItem import IBaseItem
#----------------------------------------------------------------------

    # Class
class MemoryValue(implements(IBaseItem)):
    name: str = 'memory'
    key: str = 'memoryvalue'

    def __init__(self, data: XMLNode = None) -> None:
        if not data: data = self.create().export()

        self.offset: int = data.get_attribute('offset', 0) # Required
        self.value: int = int(str(data.get_attribute('value', 0)), 16) # Required
        self.original: int = int(str(data.get_attribute('original', 0)), 16) # Optional
        self.comment: str = data.get_attribute('comment', '') # Optional

    def export(self) -> XMLNode:
        return XMLNode(
            self.name,
            (
                {'offset': self.offset} |
                {('value'): self.value} |
                ({'original': self.original} if self.original else {}) |
                ({'comment': self.comment} if self.comment else {})
            )
        )

    def copy(self) -> 'MemoryValue':
        return MemoryValue(self.export())

    @staticmethod
    def create() -> 'MemoryValue':
        return MemoryValue(XMLNode(MemoryValue.name))
#----------------------------------------------------------------------
