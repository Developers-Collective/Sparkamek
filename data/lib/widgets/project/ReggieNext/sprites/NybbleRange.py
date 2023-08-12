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
#----------------------------------------------------------------------
