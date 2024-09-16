#----------------------------------------------------------------------------------------------------

    # Libraries
from string import Formatter
from parse import parse
from datetime import timedelta
from enum import Enum
#----------------------------------------------------------------------------------------------------

    # Enum
class StrfDeltaValue:
    def __init__(self, key: str, value: int) -> None:
        self._key = key
        self._value = value

    @property
    def key(self) -> str:
        return self._key

    @property
    def value(self) -> int:
        return self._value


class StrfDeltaType(Enum):
    Seconds = StrfDeltaValue('S', 1)
    Minutes = StrfDeltaValue('M', 60)
    Hours = StrfDeltaValue('H', 3600)
    Days = StrfDeltaValue('D', 86400)
    Weeks = StrfDeltaValue('W', 604800)
    Years = StrfDeltaValue('Y', 31536000)
#----------------------------------------------------------------------------------------------------

    # Function
def strfdelta(tdelta: timedelta | int, fmt: str = '{D:02}d {H:02}h {M:02}m {S:02}s', inputtype: StrfDeltaType | None = None) -> str:
    '''Convert a datetime.timedelta object or a regular number to a custom-
    formatted string, just like the stftime() method does for datetime.datetime
    objects.

    The fmt argument allows custom formatting to be specified.  Fields can 
    include seconds, minutes, hours, days, and weeks.  Each field is optional.

    Some examples:
        `'{D:02}d {H:02}h {M:02}m {S:02}s'` ➜ `'05d 08h 04m 02s'` (default)\n
        `'{W}w {D}d {H}:{M:02}:{S:02}'`     ➜ `'4w 5d 8:04:02'`\n
        `'{D:2}d {H:2}:{M:02}:{S:02}'`      ➜ `' 5d  8:04:02'`\n
        `'{H}h {S}s'`                       ➜ `'72h 800s'`\n

    Args:
        tdelta (timedelta | int): The timedelta to convert.
        fmt (str, optional): The format string. Defaults to '{D:02}d {H:02}h {M:02}m {S:02}s'.
        inputtype (StrfDeltaType, required if tdelta is int, useless if tdelta is timedelta): The type of input. Defaults to None.

    Returns:
        str: The formatted string.
    '''

    # Convert tdelta to integer seconds.
    if isinstance(tdelta, timedelta):
        remainder = int(tdelta.total_seconds())

    else:
        remainder = int(tdelta) * inputtype.value.value

    f = Formatter()
    desired_fields = [field_tuple[1] for field_tuple in f.parse(fmt)]
    constants = {t.value.key: t.value.value for t in StrfDeltaType}
    possible_fields = tuple(
        value[0]
            for value in sorted(
                tuple((k, v) for k, v in constants.items()),
                key = lambda x: x[1],
                reverse = True,
            )
    )
    values = {}

    for field in possible_fields:
        if field in desired_fields and field in constants:
            values[field], remainder = divmod(remainder, constants[field])

    return f.format(fmt, **values)



def deltastrf(string: str, fmt: str = '{D:02}d {H:02}h {M:02}m {S:02}s') -> timedelta:
    '''Convert a string to a datetime.timedelta object.

    Args:
        string (str): The string to convert.
        fmt (str, optional): The format string. Defaults to '{D:02}d {H:02}h {M:02}m {S:02}s'.

    Returns:
        timedelta: The timedelta object.
    '''

    possible_fields = tuple(t.value.key for t in StrfDeltaType)
    constants = {t.value.key: t.value.value for t in StrfDeltaType}

    parse_result = parse(fmt, string).named
    seconds = 0

    for field in parse_result.keys():
        if field in possible_fields:
            seconds += int(parse_result[field]) * constants[field]

    return timedelta(seconds = seconds)
#----------------------------------------------------------------------------------------------------
