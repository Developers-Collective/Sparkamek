#----------------------------------------------------------------------

    # Libraries
import os
#----------------------------------------------------------------------

    # Class
class KamekConstants:
    def __new__(cls) -> None:
        return None

    LocalVersionsNSMBW = '/tools/versions-nsmbw.txt'
    GlobalVersionsNSMBW = os.path.abspath('./data/game/SMN/versions/versions-nsmbw.txt')

    @staticmethod
    def get_versions_nsmbw(cwd: str) -> str:
        path = f'{cwd}{KamekConstants.LocalVersionsNSMBW}'

        if not os.path.exists(path):
            path = KamekConstants.GlobalVersionsNSMBW

        return path

    LocalErrorsNSMBW = '/tools/versions-nsmbw-errors/'
    GlobalErrorsNSMBW = os.path.abspath('./data/game/SMN/versions/versions-nsmbw-errors/')

    @staticmethod
    def get_errors_nsmbw(cwd: str) -> str:
        path = f'{cwd}{KamekConstants.LocalErrorsNSMBW}'

        if not os.path.exists(path):
            path = KamekConstants.GlobalErrorsNSMBW

        return path
#----------------------------------------------------------------------
