#----------------------------------------------------------------------

    # Libraries
from interface import implements
from data.lib.storage import XMLNode
from .IBaseItem import IBaseItem
#----------------------------------------------------------------------

    # Class
class MemoryOcarina(implements(IBaseItem)):
    name: str = 'memory'

    def __init__(self, data: XMLNode = None) -> None:
        if not data: data = self.create().export()

        self.offset: int = data.get_attribute('offset', 0) # Required
        self.value: int = int(str(data.get_attribute('value', 0)), 16) # Required

    def export(self) -> XMLNode:
        return XMLNode(
            self.name,
            (
                {'offset': self.offset} |
                {('value'): self.value} |
                {'ocarina': True}
            )
        )

    def copy(self) -> 'MemoryOcarina':
        return MemoryOcarina(self.export())

    @staticmethod
    def create() -> 'MemoryOcarina':
        return MemoryOcarina(XMLNode(MemoryOcarina.name))
#----------------------------------------------------------------------
