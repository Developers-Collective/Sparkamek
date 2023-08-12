#----------------------------------------------------------------------

    # Libraries
import xml.dom.minidom as minidom
from typing import Union
#----------------------------------------------------------------------

    # Class
class XMLNode:
        def __init__(self, name: str, attributes: dict, children: list, value: int | float | str | None) -> None:
            self._name = name
            self._attributes = attributes
            self._children = children
            self._value = value


        @property
        def name(self) -> str:
            return self._name
        
        @property
        def attributes(self) -> dict[str, int | float | str | None]:
            return self._attributes
        
        @property
        def children(self) -> list['XMLNode']:
            return self._children
        
        @property
        def value(self) -> int | float | str | None:
            return self._value


        def get_attribute(self, name: str, default: int | float | str | None = None) -> int | float | str | None:
            return self.attributes.get(name, default)


        def get_first_child(self, name: str) -> Union['XMLNode', None]:
            for child in self.children:
                if child.name == name: return child
            return None

        def get_children(self, name: str) -> list:
            return [child for child in self.children if child.name == name]


        def __repr__(self) -> str:
            attr = ' '.join([f'{key}="{value}"' for key, value in self.attributes.items()])

            s = f'<{self.name}'
            if attr: s += f' {attr}'

            if self.value is not None: s += f'>{self.value}</{self.name}>'
            else: s += '/>'

            for child in self.children:
                s += '\n\t' + str(child)

            if self.children: s += f'\n</{self.name}>'

            return s.replace('\n', '\n\t')

        def __str__(self) -> str:
            return self.__repr__()



class XML:
    def __init__(self, root_name: str, children: list[XMLNode]) -> None:
        self._root_name = root_name
        self._children = children


    @property
    def root_name(self) -> str:
        return self._root_name
    
    @property
    def children(self) -> list[XMLNode]:
        return self._children


    def __repr__(self) -> str:
        s = f'<{self.root_name}>'

        for child in self.children:
            s += '\n\t' + str(child)

        return s + f'\n</{self.root_name}>'


    @staticmethod
    def parse_file(file_path: str) -> 'XML':
        with open(file_path, 'r') as file:
            return XML.parse(file.read())

    @staticmethod
    def parse(text: str) -> 'XML':
        doc = minidom.parseString(text)
        root: minidom.Element = doc.documentElement

        children = []
        for child in root.childNodes:
            if child.nodeType == minidom.Node.ELEMENT_NODE:
                children.append(XML._parse_element(child))

        return XML(root.tagName, children)


    @staticmethod
    def _parse_element(element: minidom.Element) -> XMLNode:
        attributes = {}
        children = []
        value = None

        for key, dvalue in element.attributes.items():
            attributes[key] = XML._convert(dvalue)

        for child in element.childNodes:
            child: minidom.Element

            if child.nodeType == minidom.Node.ELEMENT_NODE:
                children.append(XML._parse_element(child))

            elif child.nodeType == minidom.Node.TEXT_NODE:
                if v := child.nodeValue.strip():
                    value = XML._convert(v)

        return XMLNode(element.tagName, attributes, children, value)


    @staticmethod
    def _convert(val):
        constructors = [int, float, str]
        for c in constructors:
            try:
                return c(val)

            except ValueError:
                pass
#----------------------------------------------------------------------
