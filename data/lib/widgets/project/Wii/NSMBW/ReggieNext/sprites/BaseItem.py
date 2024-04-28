#----------------------------------------------------------------------

    # Libraries
from interface import implements
from data.lib.storage import XMLNode
from .IBaseSprite import IBaseSprite
from .NybbleRange import NybbleRange
from .ReqNybble import ReqNybble
#----------------------------------------------------------------------

    # Class
class BaseItem(implements(IBaseSprite)):
    name: str = 'BaseItem'

    def __init__(self, data: XMLNode) -> None:
        reqnybs = str(data.get_attribute('requirednybble', ''))
        requirednybbles = [NybbleRange(r) for r in reqnybs.split(',') if r.strip()] if reqnybs else []

        reqblocks = str(data.get_attribute('requiredblock', ''))
        requiredblocks = [int(s.strip()) for s in reqblocks.split(',')] if reqblocks else []

        reqvals = str(data.get_attribute('requiredval', '')).split(',')
        requiredvals: list[list[int], list[int, int]] = []
        if reqvals == ['']: reqvals = []
        for r in reqvals:
            r = r.strip()
            if not r: continue

            if '-' in r:
                requiredvals.append([int(subr.strip()) for subr in r.split('-')])

            else:
                requiredvals.append([int(r)])

        self._requirednybblevals: list[ReqNybble] = []
        for i in range(len(requirednybbles)):
            val = requiredvals[i] if i < len(requiredvals) else [1]
            block = requiredblocks[i] if i < len(requiredblocks) else None
            self._requirednybblevals.append(ReqNybble(requirednybbles[i], val, block))

        bits = data.get_attribute('bits', '')
        if bits: self._nybbles = NybbleRange.from_bits(bits)
        else: self._nybbles = NybbleRange(data.get_attribute('nybble', ''))

        self._block: int | None = data.get_attribute('block', 0)

        self._comment = data.get_attribute('comment', '')
        self._comment2 = data.get_attribute('comment2', '')
        self._advanced = bool(data.get_attribute('advanced', False))
        self._advancedcomment = data.get_attribute('advancedcomment', '')


    @property
    def requirednybblevals(self) -> list[ReqNybble]:
        return self._requirednybblevals


    @property
    def nybbles(self) -> NybbleRange:
        return self._nybbles


    @property
    def block(self) -> int:
        return self._block

    @block.setter
    def block(self, value: int) -> None:
        self._block = value


    @property
    def comment(self) -> str:
        return self._comment

    @comment.setter
    def comment(self, value: str) -> None:
        self._comment = value


    @property
    def comment2(self) -> str:
        return self._comment2

    @comment2.setter
    def comment2(self, value: str) -> None:
        self._comment2 = value


    @property
    def advanced(self) -> bool:
        return self._advanced

    @advanced.setter
    def advanced(self, value: bool) -> None:
        self._advanced = value


    @property
    def advancedcomment(self) -> str:
        return self._advancedcomment

    @advancedcomment.setter
    def advancedcomment(self, value: str) -> None:
        self._advancedcomment = value


    def export(self) -> XMLNode:
        return XMLNode(
            self.name,
            (
                ({'requirednybble': ','.join([nybble.nybbles.export() for nybble in self._requirednybblevals])} if self._requirednybblevals else {}) |
                ({'requiredval': ','.join([r.values.export() for r in self._requirednybblevals])} if self._requirednybblevals else {}) |
                ({'nybble': self._nybbles.export()} if self._nybbles.export() else {}) |
                ({'comment': self._comment} if self._comment else {}) |
                ({'comment2': self._comment2} if self._comment2 else {}) |
                ({'advanced': self._advanced} if self._advanced else {}) |
                ({'advancedcomment': self._advancedcomment} if self._advancedcomment else {})
            )
        )


    def copy(self) -> 'BaseItem':
        return BaseItem(self.export())


    @staticmethod
    def create() -> 'BaseItem':
        return BaseItem(XMLNode('BaseItem', attributes = {'nybble': 1}))


    def convert_to_extended(self) -> None:
        if self._nybbles.start.n >= 9 and self._nybbles.end.n >= 9:
            self._block = 2
            self._nybbles.start.n -= 8
            self._nybbles.end.n -= 8

        elif self._nybbles.start.n <= 8 and self._nybbles.end.n <= 8:
            self._block = 1

        else:
            if self._nybbles.start.n >= 8:
                self._nybbles.start.n -= 8

            if self._nybbles.end.n >= 8:
                self._nybbles.end.n -= 8

            self._block = 1

        for nybble in self._requirednybblevals:
            if nybble.nybbles.start.n >= 9 and nybble.nybbles.end.n >= 9:
                nybble.block = 2
                nybble.nybbles.start.n -= 8
                nybble.nybbles.end.n -= 8

            elif nybble.nybbles.start.n <= 8 and nybble.nybbles.end.n <= 8:
                nybble.block = 1

            else:
                if nybble.nybbles.start.n >= 8:
                    nybble.nybbles.start.n -= 8

                if nybble.nybbles.end.n >= 8:
                    nybble.nybbles.end.n -= 8

                nybble.block = 1


    def convert_to_normal(self) -> None:
        if self._block == 2:
            self._nybbles.start.n += 8
            self._nybbles.end.n += 8

        self._block = 0

        for nybble in self._requirednybblevals:
            if nybble.block == 1:
                nybble.nybbles.start.n += 8
                nybble.nybbles.end.n += 8

            nybble.block = 0
#----------------------------------------------------------------------
