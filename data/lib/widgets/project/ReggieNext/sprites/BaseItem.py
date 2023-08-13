#----------------------------------------------------------------------

    # Libraries
from data.lib.storage import XMLNode
from data.lib.widgets.project.ReggieNext.sprites.BaseSprite import BaseSprite
from .BaseSprite import BaseSprite
from .NybbleRange import NybbleRange
#----------------------------------------------------------------------

    # Class
class BaseItem(BaseSprite):
    name: str = 'BaseItem'

    def __init__(self, data: XMLNode) -> None:
        super().__init__(data)

        reqnybs = str(data.get_attribute('requirednybble', ''))
        self.requirednybbles = [NybbleRange(r) for r in reqnybs.split(',') if r.strip()] if reqnybs else []

        reqvals = str(data.get_attribute('requiredval', '')).split(',')
        self.requiredvals = []
        if reqvals == ['']: reqvals = []
        for r in reqvals:
            r = r.strip()
            if not r: continue

            if '-' in r:
                self.requiredvals.append(tuple(int(subr.strip()) for subr in r.split('-')))

            else:
                self.requiredvals.append(int(r))

        self.nybble = NybbleRange(data.get_attribute('nybble', ''))

        self.comment = data.get_attribute('comment', '')
        self.comment2 = data.get_attribute('comment2', '')
        self.advanced = bool(data.get_attribute('advanced', False))
        self.advancedcomment = data.get_attribute('advancedcomment', '')

    def export(self) -> XMLNode:
        sup = super().export()

        reqvals = []
        for r in self.requiredvals:
            if isinstance(r, int):
                reqvals.append(str(r))

            else:
                reqvals.append(f'{r[0]}-{r[1]}')

        return XMLNode(
            self.name,
            (
                ({'requirednybble': ','.join([nybble.export() for nybble in self.requirednybbles])} if self.requirednybbles else {}) |
                ({'requiredval': ','.join(reqvals)} if reqvals else {}) |
                ({'nybble': self.nybble.export()} if self.nybble.export() else {}) |
                ({'comment': self.comment} if self.comment else {}) |
                ({'comment2': self.comment2} if self.comment2 else {}) |
                ({'advanced': self.advanced} if self.advanced else {}) |
                ({'advancedcomment': self.advancedcomment} if self.advancedcomment else {})
            ) | sup.attributes,
            sup.children,
            sup.value
        )

    def copy(self) -> 'BaseItem':
        return BaseItem(self.export())
#----------------------------------------------------------------------
