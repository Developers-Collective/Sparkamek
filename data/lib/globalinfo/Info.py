#----------------------------------------------------------------------

    # Libraries
from ..qtUtils import QSaveData, QUtilsColor
import os
#----------------------------------------------------------------------

    # Class
class Info:
    def __new__(cls) -> None:
        return None

    build: str = '07e7d473'
    version: str = 'Experimental'

    application_name: str = 'Sparkamek'

    save_path: str = os.path.abspath('./data/save.dat').replace('\\', '/')

    main_color_set: QSaveData.ColorSet = QSaveData.ColorSet(
        'blue',
        QUtilsColor.from_hex('#1473E6'),
        QUtilsColor.from_hex('#0D66D0'),
        QUtilsColor.from_hex('#1B80FC'),
        QUtilsColor.from_hex('#375782'),
    )
    neutral_color_set: QSaveData.ColorSet = QSaveData.ColorSet(
        'white',
        QUtilsColor.from_hex('#E3E3E3'),
        QUtilsColor.from_hex('#D7D7D7'),
        QUtilsColor.from_hex('#EFEFEF'),
        QUtilsColor.from_hex('#CACACA'),
    )

    icon_path: str = './data/icons/Sparkamek.svg'
#----------------------------------------------------------------------
