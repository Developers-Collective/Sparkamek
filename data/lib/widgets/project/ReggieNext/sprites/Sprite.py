#----------------------------------------------------------------------

    # Libraries
from interface import implements
from data.lib.storage import XMLNode
from .IBaseSprite import IBaseSprite
from .BaseItem import BaseItem
from .Dependency import Dependency
from .DualBox import DualBox
from .CheckBox import CheckBox
from .Value import Value
from .List import List
from .External import External
#----------------------------------------------------------------------

    # Class
class Sprite(implements(IBaseSprite)):
    name: str = 'sprite'

    def __init__(self, data: XMLNode) -> None:
        self.id = data.get_attribute('id', None)
        self.sprite_name = data.get_attribute('name', '')
        self.asmhacks = self._bool_filter(data.get_attribute('asmhacks', False))
        self.sizehacks = self._bool_filter(data.get_attribute('sizehacks', False))
        self.noyoshi = self._bool_filter(data.get_attribute('noyoshi', False))
        self.yoshinotes = data.get_attribute('yoshinotes', '')
        self.notes = data.get_attribute('notes', '')
        self.advancednotes = data.get_attribute('advancednotes', '')
        self.phonebook = data.get_attribute('phonebook', '') # TF is this?

        dependency = data.get_first_child('dependency')
        self.dependency = Dependency(dependency) if dependency else Dependency(XMLNode('dependency', {}, [], None))
        self.children: list[BaseItem] = []

        for child in data.children:
            match child.name:
                case 'dependency': continue
                case 'dualbox': self.children.append(DualBox(child))
                case 'checkbox': self.children.append(CheckBox(child))
                case 'value': self.children.append(Value(child))
                case 'list': self.children.append(List(child))
                case 'external': self.children.append(External(child))
                case _:
                    print(f'Unknown sprite child: {child}')
                    # raise ValueError(f'Unknown sprite child: {child}')

    def _bool_filter(self, value: bool) -> bool:
        return True if value == 'True' else False if value == 'False' else bool(value)

    def export(self) -> XMLNode:
        return XMLNode(
            'sprite',
            (
                ({'id': self.id} if self.id is not None else {}) |
                ({'name': self.sprite_name} if self.sprite_name else {}) |
                ({'asmhacks': self.asmhacks} if self.asmhacks else {}) |
                ({'sizehacks': self.sizehacks} if self.sizehacks else {}) |
                ({'noyoshi': self.noyoshi} if self.noyoshi else {}) |
                ({'yoshinotes': self.yoshinotes} if self.yoshinotes else {}) |
                ({'notes': self.notes} if self.notes else {}) |
                ({'advancednotes': self.advancednotes} if self.advancednotes else {}) |
                ({'phonebook': self.phonebook} if self.phonebook else {})
            ),
            ([self.dependency.export()] if self.dependency else []) + [c.export() for c in self.children]
        )

    def copy(self) -> 'Sprite':
        return Sprite(self.export())

    @staticmethod
    def create() -> 'Sprite':
        return Sprite(XMLNode('sprite', attributes = {'id': '0', 'name': 'New Sprite'}))
#----------------------------------------------------------------------
