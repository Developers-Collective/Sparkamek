#----------------------------------------------------------------------

    # Libraries
from interface import implements
from data.lib.storage import XMLNode
from .IBaseItem import IBaseItem
#----------------------------------------------------------------------

    # Class
class MemorySearchValueFile(implements(IBaseItem)):
    name: str = 'memory'

    def __init__(self, data: XMLNode = None) -> None:
        if not data: data = self.create().export()

        self.original: str = str(data.get_attribute('original', '')) # Required
        self.valuefile: str = data.get_attribute('valuefile', '') # Required
        self.align: int = data.get_attribute('align', 1) # Optional
        self.comment: str = data.get_attribute('comment', '') # Optional

    def export(self) -> XMLNode:
        return XMLNode(
            self.name,
            (
                {'original': self.original} |
                {('valuefile'): self.valuefile} |
                ({'align': self.align} if self.align != 1 else {}) |
                {'search': True} |
                ({'comment': self.comment} if self.comment else {})
            )
        )

    def copy(self) -> 'MemorySearchValueFile':
        return MemorySearchValueFile(self.export())

    @staticmethod
    def create() -> 'MemorySearchValueFile':
        return MemorySearchValueFile(XMLNode(MemorySearchValueFile.name))
#----------------------------------------------------------------------
