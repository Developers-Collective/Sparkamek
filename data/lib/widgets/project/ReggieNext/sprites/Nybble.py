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
#----------------------------------------------------------------------
