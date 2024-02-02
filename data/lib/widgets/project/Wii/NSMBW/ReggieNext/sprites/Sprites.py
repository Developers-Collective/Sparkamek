#----------------------------------------------------------------------

    # Libraries
from data.lib.storage import XML, XMLNode
from .Sprite import Sprite
#----------------------------------------------------------------------

    # Class
class Sprites:
    def __init__(self, data: XML = None) -> None:
        self.children = []

        if not data: return

        node: XMLNode = data.root
        if not node: return

        self.children = [Sprite(c) for c in node.children]

    def __getitem__(self, index: int) -> Sprite:
        return self.children[index]
    
    def __len__(self) -> int:
        return len(self.children)
    
    def __iter__(self) -> Sprite:
        return iter(self.children)
    
    def get(self, id: int) -> Sprite:
        return self.children[id]

    def get_by_id(self, id: int) -> Sprite | None:
        sprite = next((s for s in self.children if s.id == id), None)
        return sprite

    def index(self, sprite: Sprite) -> int:
        return self.children.index(sprite)
    
    def index_by_id(self, id: str) -> int:
        return self.index(self.get_by_id(id))

    def add(self, sprite: Sprite) -> None:
        if sprite.id is None: raise ValueError('Sprite ID cannot be None')
        if sprite.id in [s.id for s in self.children]: raise ValueError(f'Sprite ID already exists: {sprite.id}')
        self.children.append(sprite)
        self.sort_by_id()

    def remove(self, sprite: Sprite | int) -> None:
        if isinstance(sprite, int): self.children.pop(sprite)
        else: self.children.remove(sprite)

    def remove_by_id(self, id: str) -> None:
        self.remove(self.get_by_id(id))

    def replace(self, index: int, sprite: Sprite) -> None:
        self.children[index] = sprite
        self.sort_by_id()

    def replace_by_id(self, id: str, sprite: Sprite) -> None:
        self.replace(self.index_by_id(id), sprite)

    def sort_by_id(self) -> None:
        self.children.sort(key = lambda s: s.id)

    def get_next_free_id(self) -> int:
        if not self.children: return 0
        return max([s.id for s in self.children]) + 1

    def export(self) -> XML:
        return XML(
            XMLNode(
                'sprites',
                children = [c.export() for c in self.children]
            )
        )
#----------------------------------------------------------------------
