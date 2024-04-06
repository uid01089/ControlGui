import paho.mqtt.client as pahoMqtt
from guis.ChargeControlGui import ChargeControlGui
from ContextIf import ContextIf


from guis.GarageGui import GarageGui
from guis.GardenGui import GardenGui
from guis.GuiIf import GuiIf
from guis.JalousienGui import JalousienGui
from guis.PvGui import PvGui
from PythonLib.AsyncMqtt import AsyncMqtt
from PythonLib.AsyncScheduler import AsyncScheduler


class Context(ContextIf):
    def __init__(self) -> None:
        self.scheduler = AsyncScheduler()
        self.mqttClient = AsyncMqtt("koserver.iot", "/house/agents/ControlGui", pahoMqtt.Client("ControlGui3", protocol=pahoMqtt.MQTTv311))
        self.chargeControlGui = ChargeControlGui(self)
        self.garageGui = GarageGui(self)
        self.jalousienGui = JalousienGui(self)
        self.pvGui = PvGui(self)
        self.gardenGui = GardenGui(self)

    async def getScheduler(self) -> AsyncScheduler:
        return self.scheduler

    async def getMqttClient(self) -> AsyncMqtt:
        return self.mqttClient

    async def getChargeControlGui(self) -> GuiIf:
        return self.chargeControlGui

    async def getGarageGui(self) -> GuiIf:
        return self.garageGui

    async def getJalousienGui(self) -> GuiIf:
        return self.jalousienGui

    async def getPvGui(self) -> GuiIf:
        return self.pvGui

    async def getGardenGui(self) -> GuiIf:
        return self.gardenGui

    async def setup(self) -> None:
        await self.mqttClient.connectAndRun()
