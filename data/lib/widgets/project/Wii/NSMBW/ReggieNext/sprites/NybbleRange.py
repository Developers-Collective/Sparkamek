#----------------------------------------------------------------------

    # Libraries
from .Nybble import Nybble
#----------------------------------------------------------------------

    # Class
class NybbleRange:
    def __init__(self, data: str | int | float | None) -> None:
        if data == '' or data == None:
            self._start = None
            self._end = None
            return

        if isinstance(data, float): data = str(data)
        if isinstance(data, int): data = str(data)
        info = data.split('-')

        if len(info) == 2:
            self._start = Nybble(info[0])
            self._end = Nybble(info[1])

        else:
            self._start = Nybble(info[0])
            self._end = None


    @property
    def start(self) -> Nybble:
        return self._start

    @start.setter
    def start(self, value: Nybble) -> None:
        self._start = value


    @property
    def end(self) -> Nybble | None:
        return self._end

    @end.setter
    def end(self, value: Nybble | None) -> None:
        self._end = value


    def export(self) -> str:
        if self._start == None:
            return ''

        if self._end == None:
            return self._start.export()
        
        return f'{self._start.export()}-{self._end.export()}'

    def copy(self) -> 'NybbleRange':
        return NybbleRange(self.export())


    @staticmethod
    def nybblebit2int(settings: int, from_nybble: int | None, from_bit: int, to_nybble: int, to_bit: int | None, block: int = 0) -> int:
        if from_bit is None: from_bit = 0
        if to_bit is None: to_bit = 3

        size = 64 if block == 0 else 32

        first_bit_pos = size - (4 * to_nybble) + (3 - to_bit)
        last_bit_pos = size - (4 * from_nybble) + (3 - from_bit)

        fshit = int(pow(2, (last_bit_pos - first_bit_pos) + 1)) - 1

        return settings & (fshit << first_bit_pos)


    def convert2int(self, block = 0) -> int:
        if self._start == None: return 0

        settings = 0xFFFFFFFFFFFFFFFF if block == 0 else 0xFFFFFFFF

        if self._end == None: return NybbleRange.nybblebit2int(settings, self._start.n, self._start.b, self._start.n, self._start.b, block)
        return NybbleRange.nybblebit2int(settings, self._start.n, self._start.b, self._end.n, self._end.b, block)


    def convert2hex_formatted(self, block: int) -> str:
        if block == 0: s = f'{self.convert2int(block):016X}'
        else: s = f'{self.convert2int(block):08X}'

        formatted = ''
        for i in range(0, len(s), 4):
            formatted += f'{s[i:i + 4]} '

        return formatted.strip()


    @staticmethod
    def from_bits(bits: str) -> 'NybbleRange':
        if bits == '' or bits is None: return NybbleRange('1')
        if not isinstance(bits, str): bits = str(bits)

        bit_list = bits.replace(' ', '').split('-')

        if len(bit_list) == 2: return NybbleRange(f'{Nybble.from_bits(bit_list[0]).export()}-{Nybble.from_bits(bit_list[1]).export()}')
        else: return NybbleRange(Nybble.from_bits(bit_list[0]).export())
#----------------------------------------------------------------------
