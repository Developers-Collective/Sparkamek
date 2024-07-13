#----------------------------------------------------------------------

    # Libraries
from data.lib.QtUtils.QtCore.QLogsColor import QLogsColor
#----------------------------------------------------------------------

    # Class
class ProjectException(Exception):
    def __init__(self, msg: str, type: QLogsColor) -> None:
        super().__init__(msg)

        self._msg = msg
        self._type = type

    @property
    def msg(self) -> str:
        return self._msg

    @property
    def type(self) -> QLogsColor:
        return self._type
#----------------------------------------------------------------------
