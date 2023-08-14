#----------------------------------------------------------------------

    # Class
class ValueRange:
    def __init__(self, values: list[int] | list[int, int]) -> None:
        super().__init__()

        self.start = values[0]
        self.end = values[1] if len(values) > 1 else values[0]


    def export(self) -> str:
        if self.start == self.end:
            return str(self.start)

        return f'{self.start}-{self.end}'
#----------------------------------------------------------------------
