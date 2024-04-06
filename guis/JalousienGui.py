from enum import Enum
from ContextIf import ContextIf
from guis.GuiIf import GuiIf
from nicegui import ui


class JalousienState(Enum):
    OPEN = 0
    STOP = 1
    CLOSE = 2


class JalousienGui(GuiIf):
    def __init__(self, context: ContextIf):
        self.context = context
        self.statusWohnzimmer = JalousienState.STOP
        self.statusArbeitszimmer = JalousienState.STOP
        self.mqttClient = None

    async def setup(self) -> None:

        self.mqttClient = await self.context.getMqttClient()
        # await self.mqttClient.subscribeIndependentTopic('/house/garage/tor/distance', self.__receivedDistance)

        with ui.row().classes('w-full'):
            ui.label("Wohnzimmer: ")
            ui.toggle(options={JalousienState.CLOSE: 'Rauf', JalousienState.STOP: 'STOP', JalousienState.OPEN: 'Runter'},
                      on_change=lambda e: self.mqttUpdate('Wohnzimmer', e.value)).bind_value(self, 'statusWohnzimmer')

        with ui.row().classes('w-full'):
            ui.label("Arbeitszimmer: ")
            ui.toggle(options={JalousienState.CLOSE: 'Rauf', JalousienState.STOP: 'STOP', JalousienState.OPEN: 'Runter'},
                      on_change=lambda e: self.mqttUpdate('Arbeitszimmer', e.value)).bind_value(self, 'statusArbeitszimmer')

    async def mqttUpdate(self, room: str, value: JalousienState) -> None:
        match (value):
            case JalousienState.OPEN:
                await self.mqttClient.publishIndependentTopic(f'/house/agents/ShellyJalousien/set/{room}', 'open')
            case JalousienState.STOP:
                await self.mqttClient.publishIndependentTopic(f'/house/agents/ShellyJalousien/set/{room}', 'stop')
            case JalousienState.CLOSE:
                await self.mqttClient.publishIndependentTopic(f'/house/agents/ShellyJalousien/set/{room}', 'close')
