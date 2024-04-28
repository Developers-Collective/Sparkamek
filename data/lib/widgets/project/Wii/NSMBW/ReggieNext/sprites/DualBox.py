#----------------------------------------------------------------------

    # Libraries
from data.lib.storage import XMLNode
from data.lib.widgets.project.Wii.NSMBW.ReggieNext.sprites.BaseItem import BaseItem
from .BaseItem import BaseItem
#----------------------------------------------------------------------

    # Class
class DualBox(BaseItem):
    name: str = 'dualbox'


    def __init__(self, data: XMLNode) -> None:
        super().__init__(data)

        self._title1 = data.get_attribute('title1', '')
        self._title2 = data.get_attribute('title2', '')


    @property
    def title1(self) -> str:
        return self._title1

    @title1.setter
    def title1(self, value: str) -> None:
        self._title1 = value


    @property
    def title2(self) -> str:
        return self._title2

    @title2.setter
    def title2(self, value: str) -> None:
        self._title2 = value


    def export(self) -> XMLNode:
        sup = super().export()

        return XMLNode(
            self.name,
            (
                ({'title1': self._title1} if self._title1 else {}) |
                ({'title2': self._title2} if self._title2 else {})
            ) | sup.attributes,
            sup.children,
            sup.value
        )


    def copy(self) -> 'DualBox':
        return DualBox(self.export())


    @staticmethod
    def create() -> 'DualBox':
        return DualBox(XMLNode('dualbox', attributes = {'nybble': 1, 'title1': 'New DualBox', 'title2': 'New DualBox'}))
#----------------------------------------------------------------------
