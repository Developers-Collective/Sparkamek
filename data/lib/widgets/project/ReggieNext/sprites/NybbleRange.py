#----------------------------------------------------------------------

    # Libraries
from .Nybble import Nybble
#----------------------------------------------------------------------

    # Class
class NybbleRange:
    def __init__(self, data: str | int | float | None) -> None:
        if data == '' or data == None:
            self.start = None
            self.end = None
            return

        if isinstance(data, float): data = str(data)
        if isinstance(data, int): data = str(data)
        info = data.split('-')

        if len(info) == 2:
            self.start = Nybble(info[0])
            self.end = Nybble(info[1])

        else:
            self.start = Nybble(info[0])
            self.end = None


    def export(self) -> str:
        if self.start == None:
            return ''

        if self.end == None:
            return self.start.export()
        
        return f'{self.start.export()}-{self.end.export()}'

    def copy(self) -> 'NybbleRange':
        return NybbleRange(self.export())


    @staticmethod
    def nybblebit2int(settings: int, from_nybble: int | None, from_bit: int, to_nybble: int, to_bit: int | None) -> int:
        if from_bit is None: from_bit = 0
        if to_bit is None: to_bit = 3

        first_bit_pos = 64 - (4 * to_nybble) + (3 - to_bit)
        last_bit_pos = 64 - (4 * from_nybble) + (3 - from_bit)

        fshit = int(pow(2, (last_bit_pos - first_bit_pos) + 1)) - 1

        return settings & (fshit << first_bit_pos)


    def convert2int(self) -> int:
        settings = 0xFFFFFFFFFFFFFFFF

        if self.end == None: return NybbleRange.nybblebit2int(settings, self.start.n, self.start.b, self.start.n, self.start.b)
        return NybbleRange.convert2int(settings, self.start.n, self.start.b, self.end.n, self.end.b)

    def convert2hex_formatted(self) -> int:
        s = f'{self.convert2int():016X}'
        return f'{s[0:4]} {s[4:8]} {s[8:12]} {s[12:16]}'
#----------------------------------------------------------------------
