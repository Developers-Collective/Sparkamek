#----------------------------------------------------------------------

    # Libraries
from data.lib.storage import XMLNode
from .NybbleRange import NybbleRange
from .ValueRange import ValueRange
#----------------------------------------------------------------------

    # Class
class ReqNybble:
    def __init__(self, nybbles: NybbleRange, values: list[int] | list[int, int], block: int = 0) -> None:
        super().__init__()

        self._nybbles = nybbles
        self._values = ValueRange(values)
        self._block = block


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
