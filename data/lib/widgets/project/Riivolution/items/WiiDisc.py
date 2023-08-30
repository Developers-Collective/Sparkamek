#----------------------------------------------------------------------

    # Libraries
from data.lib.storage import XML, XMLNode
from .ID import ID
from .Options import Options
from .Patch import Patch
#----------------------------------------------------------------------

    # Class
class WiiDisc: # Doc at https://riivolution.github.io/wiki/Patch_Format/
    def __init__(self, data: XML = None) -> None:
        if not data: data = self.create().export()

        node: XMLNode = data.root
        if not node: raise ValueError('Invalid XML data')

        self._version: int = int(node.get_attribute('version', 1)) # Required
        self._shiftfiles: bool = bool(node.get_attribute('shiftfiles', False)) # Optional
        self._root: str = node.get_attribute('root', '') # Optional
        self._log: bool = bool(node.get_attribute('log', False)) # Optional

        self._id = ID(node.get_first_child('id'))
        self._options = Options(node.get_first_child('options'))
        self._patch = Patch(node.get_first_child('patch'))

    def export(self) -> XML:
        return XML(
            XMLNode(
                'wiidisc',
                (
                    {'version': self._version} |
                    ({'shiftfiles': self._shiftfiles} if self._shiftfiles else {}) |
                    {'root': self._root} if self._root else {} |
                    ({'log': self._log} if self._log else {})
                ),
                [
                    self._id.export(),
                    self._options.export(),
                    self._patch.export()
                ]
            )
        )

    def copy(self) -> 'WiiDisc':
        return WiiDisc(self.export())

    @staticmethod
    def create() -> 'WiiDisc':
        return WiiDisc(XML(XMLNode('wiidisc', attributes = {'version': 1, 'shiftfiles': True, 'root': '/NewerSMBW', 'log': True})))
#----------------------------------------------------------------------
