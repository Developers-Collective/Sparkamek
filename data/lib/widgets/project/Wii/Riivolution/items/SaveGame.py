#----------------------------------------------------------------------

    # Libraries
from interface import implements
from data.lib.storage import XMLNode
from .IBaseItem import IBaseItem
#----------------------------------------------------------------------

    # Class
class SaveGame(implements(IBaseItem)):
    name: str = 'savegame'

    def __init__(self, data: XMLNode = None) -> None:
        if not data: data = self.create().export()

        self.external: str = data.get_attribute('external', 'folder') # Required
        self.clone: bool = data.get_attribute('clone', True) # Optional

    def export(self) -> XMLNode:
        return XMLNode(
            self.name,
            (
                {'external': self.external} |
                ({'resize': self.clone} if not self.clone else {})
            )
        )

    def copy(self) -> 'SaveGame':
        return SaveGame(self.export())

    @staticmethod
    def create() -> 'SaveGame':
        return SaveGame(XMLNode(SaveGame.name))
#----------------------------------------------------------------------
