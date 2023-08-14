#----------------------------------------------------------------------

    # Libraries
from data.lib.storage import XMLNode
from data.lib.widgets.project.ReggieNext.sprites.BaseSprite import BaseSprite
from .BaseSprite import BaseSprite
from .NybbleRange import NybbleRange
from .ReqNybble import ReqNybble
#----------------------------------------------------------------------

    # Class
class BaseItem(BaseSprite):
    name: str = 'BaseItem'

    def __init__(self, data: XMLNode) -> None:
        super().__init__(data)

        reqnybs = str(data.get_attribute('requirednybble', ''))
        requirednybbles = [NybbleRange(r) for r in reqnybs.split(',') if r.strip()] if reqnybs else []

        reqvals = str(data.get_attribute('requiredval', '')).split(',')
        requiredvals: list[list[int], list[int, int]] = []
        if reqvals == ['']: reqvals = []
        for r in reqvals:
            r = r.strip()
            if not r: continue

            if '-' in r:
                requiredvals.append([int(subr.strip()) for subr in r.split('-')])

            else:
                requiredvals.append([int(r)])

        self.requirednybblevals: list[ReqNybble] = []
        for i in range(len(requirednybbles)):
            val = requiredvals[i] if i < len(requiredvals) else [1]
            self.requirednybblevals.append(ReqNybble(requirednybbles[i], val))

        self.nybbles = NybbleRange(data.get_attribute('nybble', ''))

        self.comment = data.get_attribute('comment', '')
        self.comment2 = data.get_attribute('comment2', '')
        self.advanced = bool(data.get_attribute('advanced', False))
        self.advancedcomment = data.get_attribute('advancedcomment', '')

    def export(self) -> XMLNode:
        sup = super().export()

        return XMLNode(
            self.name,
            (
                ({'requirednybble': ','.join([nybble.nybbles.export() for nybble in self.requirednybblevals])} if self.requirednybblevals else {}) |
                ({'requiredval': ','.join([r.values.export() for r in self.requirednybblevals])} if self.requirednybblevals else {}) |
                ({'nybble': self.nybbles.export()} if self.nybbles.export() else {}) |
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
