
from abc import ABC, abstractmethod


class GuiIf(ABC):

    @abstractmethod
    async def setup(self) -> None:
        pass
