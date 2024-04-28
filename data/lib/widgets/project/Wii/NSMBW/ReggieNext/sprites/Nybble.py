#----------------------------------------------------------------------

    # Class
class Nybble:
    def __init__(self, data: str) -> None:
        info = data.split('.')

        if len(info) == 2:
            self._n = int(info[0])
            self._b = int(info[1]) - 1

        else:
            self._n = int(info[0])
            self._b = None


    @property
    def n(self) -> int:
        return self._n

    @n.setter
    def n(self, value: int) -> None:
        self._n = value


    @property
    def b(self) -> int:
        return self._b

    @b.setter
    def b(self, value: int) -> None:
        self._b = value


    def export(self) -> str:
        if self._b == None:
            return str(self._n)
        
        return f'{self._n}.{self._b + 1}'


    def copy(self) -> 'Nybble':
        return Nybble(self.export())


    @staticmethod
    def from_bits(bits: str) -> 'Nybble':
        bits_int = int(bits)

        nybble, bit = divmod(bits_int, 4)
        return Nybble(f'{nybble + 1}' + (f'.{bit + 1}' if bit != 0 else ''))
#----------------------------------------------------------------------
