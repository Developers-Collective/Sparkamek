#----------------------------------------------------------------------

    # Libraries
from interface import implements
from data.lib.storage import XMLNode
from .IBaseItem import IBaseItem
from .File import File
from .Folder import Folder
from .SaveGame import SaveGame
from .MemoryValue import MemoryValue
from .MemoryValueFile import MemoryValueFile
from .MemoryOcarina import MemoryOcarina
from .MemorySearchValue import MemorySearchValue
from .MemorySearchValueFile import MemorySearchValueFile
#----------------------------------------------------------------------

    # Class
class Patch(implements(IBaseItem)):
    name: str = 'patch'

    def __init__(self, data: XMLNode = None) -> None:
        if not data: data = self.create().export()
        
        self.id: str = data.get_attribute('id', 'newersmbw') # Required
        self.root: str = data.get_attribute('root', '') # Optional
        self.file_children: list[File] = [File(child) for child in data.get_children(File.name)]
        self.folder_children: list[Folder] = [Folder(child) for child in data.get_children(Folder.name)]
        self.savegame_children: list[SaveGame] = [SaveGame(child) for child in data.get_children(SaveGame.name)]

        self.memory_children: list[MemoryValue | MemoryValueFile | MemoryOcarina | MemorySearchValue | MemorySearchValueFile] = []

        for child in data.get_children(MemoryValue.name):
            if child.get_attribute('search', ''):
                if child.get_attribute('value', ''): self.memory_children.append(MemorySearchValue(child))
                elif child.get_attribute('valuefile', ''): self.memory_children.append(MemorySearchValueFile(child))

            elif child.get_attribute('ocarina', False): self.memory_children.append(MemoryOcarina(child))

            elif child.get_attribute('value', ''): self.memory_children.append(MemoryValue(child))
            elif child.get_attribute('valuefile', ''): self.memory_children.append(MemoryValueFile(child))

    def export(self) -> XMLNode:
        return XMLNode(
            self.name,
            (
                {'id': self.id}
            ),
            ([f.export() for f in self.file_children] if self.file_children else []) +
            ([f.export() for f in self.folder_children] if self.folder_children else []) +
            ([f.export() for f in self.savegame_children] if self.savegame_children else []) +
            ([f.export() for f in self.memory_children] if self.memory_children else [])
        )

    def copy(self) -> 'Patch':
        return Patch(self.export())

    @staticmethod
    def create() -> 'Patch':
        return Patch(XMLNode(Patch.name))
#----------------------------------------------------------------------
