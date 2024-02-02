#----------------------------------------------------------------------

    # Class
class Nybble:
    def __init__(self, data: str) -> None:
        info = data.split('.')

        if len(info) == 2:
            self.n = int(info[0])
            self.b = int(info[1]) - 1

        else:
            self.n = int(info[0])
            self.b = None


    def export(self) -> str:
        if self.b == None:
            return str(self.n)
        
        return f'{self.n}.{self.b + 1}'

    def copy(self) -> 'Nybble':
        return Nybble(self.export())

    @staticmethod
    def from_bits(bits: str) -> 'Nybble':
        bits_int = int(bits)

        nybble, bit = divmod(bits_int, 4)
        return Nybble(f'{nybble + 1}' + (f'.{bit + 1}' if bit != 0 else ''))
#----------------------------------------------------------------------
