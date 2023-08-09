#----------------------------------------------------------------------

    # Libraries
from enum import Enum
from data.lib.qtUtils import QUtilsColor
#----------------------------------------------------------------------

    # Class
class LogType(Enum):
    Error = QUtilsColor.from_hex('#E61E14')
    Warning = QUtilsColor.from_hex('#D2A800')
    Success = QUtilsColor.from_hex('#00D20A')
    Info = QUtilsColor.from_hex('#1473E6')
#----------------------------------------------------------------------
