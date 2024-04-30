#----------------------------------------------------------------------

    # Libraries
from .NybbleRange import NybbleRange
from .ValueRange import ValueRange
from . import Sprite
#----------------------------------------------------------------------

    # Class
class ReqNybble:
    def __init__(self, nybbles: NybbleRange, values: list[int] | list[int, int], block: int = 0) -> None:
        super().__init__()

        self._parent: Sprite = None

        self._nybbles = nybbles
        self._values = ValueRange(values)
        self._block = block


    @property
    def parent(self) -> Sprite:
        return self._parent

    @parent.setter
    def parent(self, value: Sprite) -> None:
        self._parent = value


    @property
    def extended(self) -> bool:
        return self._parent.extended


    @property
    def nybbles(self) -> NybbleRange:
        return self._nybbles

    @nybbles.setter
    def nybbles(self, value: NybbleRange) -> None:
        self._nybbles = value


    @property
    def values(self) -> ValueRange:
        return self._values

    @values.setter
    def values(self, value: ValueRange) -> None:
        self._values = value


    @property
    def block(self) -> int:
        return self._block

    @block.setter
    def block(self, value: int) -> None:
        self._block = value
#----------------------------------------------------------------------
