#----------------------------------------------------------------------

    # Libraries
from data.lib.storage import XMLNode
from .NybbleRange import NybbleRange
from .ValueRange import ValueRange
#----------------------------------------------------------------------

    # Class
class ReqNybble:
    def __init__(self, nybbles: NybbleRange, values: list[int] | list[int, int]) -> None:
        super().__init__()

        self.nybbles = nybbles
        self.values = ValueRange(values)
#----------------------------------------------------------------------
