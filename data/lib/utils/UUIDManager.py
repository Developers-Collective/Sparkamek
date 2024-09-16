#----------------------------------------------------------------------

    # Libraries
from uuid import UUID, uuid4
#----------------------------------------------------------------------

    # Class
class UUIDManager:
    def __init__(self) -> None:
        self._used = set()


    def get(self, auto_add: bool = True) -> UUID:
        while True:
            uuid = uuid4()
            if uuid not in self._used:
                if auto_add: self._used.add(uuid)
                return uuid


    def register(self, uuid: UUID) -> None:
        if uuid in self._used: raise ValueError('UUID already used')
        self._used.add(uuid)


    def release(self, uuid: UUID) -> None:
        self._used.remove(uuid)


    def clear(self) -> None:
        self._used.clear()


    def from_str(self, uuid: str) -> UUID:
        uuid = UUID(uuid)

        if uuid in self._used: raise ValueError('UUID already used')
        self._used.add(uuid)

        return uuid
#----------------------------------------------------------------------
