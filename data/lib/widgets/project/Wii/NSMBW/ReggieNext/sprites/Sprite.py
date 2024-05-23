#----------------------------------------------------------------------

    # Libraries
from interface import implements
from data.lib.storage import XMLNode
from .IBaseSprite import IBaseSprite
from .BaseItem import BaseItem
from .Unknown import Unknown
from .Dependency import Dependency
from .ItemFabric import ItemFabric
#----------------------------------------------------------------------

    # Class
class Sprite(implements(IBaseSprite)):
    name: str = 'sprite'


    def __init__(self, data: XMLNode) -> None:
        self.id = data.get_attribute('id', 0)
        if not isinstance(self.id, int): self.id = 0

        self._sprite_name = data.get_attribute('name', '')
        self._asmhacks = self._bool_filter(data.get_attribute('asmhacks', False))
        self._sizehacks = self._bool_filter(data.get_attribute('sizehacks', False))
        self._noyoshi = self._bool_filter(data.get_attribute('noyoshi', False))
        self._yoshinotes = data.get_attribute('yoshinotes', '')
        self._notes = data.get_attribute('notes', '')
        self._advancednotes = data.get_attribute('advancednotes', '')
        self._phonebook = data.get_attribute('phonebook', '') # TF is this?

        self._extended = self._bool_filter(data.get_attribute('extended', False))

        dependency = data.get_first_child('dependency')
        self._dependency = Dependency(dependency) if dependency else Dependency(XMLNode('dependency', {}, [], None))
        self._children: list[BaseItem] = []

        for child in data.children:
            match child.name:
                case 'dependency': continue
                case _:
                    cls = ItemFabric.get(child.name)
                    if cls:
                        inst = cls(child)
                        inst.parent = self
                        self._children.append(inst)

                    else:
                        inst = Unknown(child)
                        inst.parent = self
                        self._children.append(inst)

                        print(f'Unknown sprite child: {child}')
                        # raise ValueError(f'Unknown sprite child: {child}')


    @property
    def sprite_name(self) -> str:
        return self._sprite_name

    @sprite_name.setter
    def sprite_name(self, value: str) -> None:
        self._sprite_name = value


    @property
    def asmhacks(self) -> bool:
        return self._asmhacks

    @asmhacks.setter
    def asmhacks(self, value: bool) -> None:
        self._asmhacks = value


    @property
    def sizehacks(self) -> bool:
        return self._sizehacks

    @sizehacks.setter
    def sizehacks(self, value: bool) -> None:
        self._sizehacks = value


    @property
    def noyoshi(self) -> bool:
        return self._noyoshi

    @noyoshi.setter
    def noyoshi(self, value: bool) -> None:
        self._noyoshi = value


    @property
    def yoshinotes(self) -> str:
        return self._yoshinotes

    @yoshinotes.setter
    def yoshinotes(self, value: str) -> None:
        self._yoshinotes = value


    @property
    def notes(self) -> str:
        return self._notes

    @notes.setter
    def notes(self, value: str) -> None:
        self._notes = value


    @property
    def advancednotes(self) -> str:
        return self._advancednotes

    @advancednotes.setter
    def advancednotes(self, value: str) -> None:
        self._advancednotes = value


    @property
    def phonebook(self) -> str:
        return self._phonebook

    @phonebook.setter
    def phonebook(self, value: str) -> None:
        self._phonebook = value


    @property
    def extended(self) -> bool:
        return self._extended

    @extended.setter
    def extended(self, value: bool) -> None:
        if self._extended == value: return
        self._extended = value

        for child in self._children:
            if value: child.convert_to_extended()
            else: child.convert_to_normal()


    @property
    def dependency(self) -> Dependency:
        return self._dependency


    @property
    def children(self) -> list[BaseItem]:
        return self._children


    @property
    def block_count(self) -> int:
        return max([c.block for c in self._children] + [0])


    def _bool_filter(self, value: bool) -> bool:
        return True if value == 'True' else False if value == 'False' else bool(value)


    def export(self) -> XMLNode:
        return XMLNode(
            'sprite',
            (
                {'id': self.id} |
                {'name': self._sprite_name} |
                ({'asmhacks': self._asmhacks} if self._asmhacks else {}) |
                ({'sizehacks': self._sizehacks} if self._sizehacks else {}) |
                ({'noyoshi': self._noyoshi} if self._noyoshi else {}) |
                ({'yoshinotes': self._yoshinotes} if self._yoshinotes else {}) |
                ({'notes': self._notes} if self._notes else {}) |
                ({'advancednotes': self._advancednotes} if self._advancednotes else {}) |
                ({'phonebook': self._phonebook} if self._phonebook else {}) |
                ({'extended': self._extended} if self._extended else {})
            ),
            ([self._dependency.export()] if self._dependency else []) + [c.export() for c in self._children]
        )


    def copy(self) -> 'Sprite':
        return Sprite(self.export())


    @staticmethod
    def create() -> 'Sprite':
        return Sprite(XMLNode('sprite', attributes = {'id': '0', 'name': 'New Sprite'}))
#----------------------------------------------------------------------
