
from abc import ABC, abstractmethod
from guis.GuiIf import GuiIf
from PythonLib.AsyncMqtt import AsyncMqtt
from PythonLib.AsyncScheduler import AsyncScheduler


class ContextIf(ABC):

    @abstractmethod
    async def getScheduler(self) -> AsyncScheduler:
        pass

    @abstractmethod
    async def getMqttClient(self) -> AsyncMqtt:
        pass

    @abstractmethod
    async def getChargeControlGui(self) -> GuiIf:
        pass

    @abstractmethod
    async def getGarageGui(self) -> GuiIf:
        pass

    @abstractmethod
    async def getJalousienGui(self) -> GuiIf:
        pass

    @abstractmethod
    async def getPvGui(self) -> GuiIf:
        pass

    @abstractmethod
    async def getGardenGui(self) -> GuiIf:
        pass
