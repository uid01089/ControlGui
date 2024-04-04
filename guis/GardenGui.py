from enum import Enum
from nicegui import ui
from ContextIf import ContextIf
from guis.GuiIf import GuiIf
from PythonLib.StringUtil import StringUtil


class GardenGui(GuiIf):
    def __init__(self, context: ContextIf):
        self.context = context
        self.mqttClient = None
        self.status = None
        self.mode = None
        self.charge = None
        self.errorMessage = None
        self.lastReceivedMode = None

    async def setup(self) -> None:

        self.mqttClient = await self.context.getMqttClient()

        await self.mqttClient.subscribeIndependentTopic('/house/agents/Automower/data/status', self.__receivedStatus)
        await self.mqttClient.subscribeIndependentTopic('/house/agents/Automower/data/mode/string', self.__receivedMode)
        await self.mqttClient.subscribeIndependentTopic('/house/agents/Automower/data/charge', self.__receivedCharge)
        await self.mqttClient.subscribeIndependentTopic('/house/agents/Automower/data/errorMessage', self.__receivedErrorMessage)
        await self.mqttClient.subscribeIndependentTopic('/house/agents/Automower/data/lastReceivedMode', self.__receivedLastReceivedMode)

        with ui.row().classes('w-full'):
            ui.label('Charge: ')
            ui.knob(0.0, show_value=True).bind_value(self, 'charge').disable()

        with ui.row().classes('w-full'):
            ui.label('Status: ')
            ui.label().bind_text(self, 'status')

        with ui.row().classes('w-full'):
            ui.label('Mode: ')
            ui.label().bind_text(self, 'mode')

        with ui.row().classes('w-full'):
            ui.label('ErrorMessage: ')
            ui.label().bind_text(self, 'errorMessage')

        with ui.row().classes('w-full'):
            ui.label('Letzter Kontact: ')
            ui.label().bind_text(self, 'lastReceivedMode')

        with ui.row().classes('w-full'):
            ui.label("Modus: ")
            ui.toggle(options={'home': 'Home', 'auto': 'Auto'})\
                .bind_value(self, 'mode')\
                .on("click", lambda e: self.statusUpdate(e.sender.value))

        with ui.row().classes('w-full'):
            ui.label("Start/Stop: ")
            ui.toggle(options={'start': 'Start', 'stop': 'Stop'})\
                .on("click", lambda e: self.startStopUpdate(e.sender.value))

    def __receivedStatus(self, payload: str) -> None:
        self.status = payload

    def __receivedErrorMessage(self, payload: str) -> None:
        self.errorMessage = payload

    def __receivedCharge(self, payload: str) -> None:
        self.charge = float(payload)

    def __receivedMode(self, payload: str) -> None:
        self.mode = payload.lower()

    def __receivedLastReceivedMode(self, payload: str) -> None:
        self.lastReceivedMode = payload

    async def statusUpdate(self, value: str) -> None:
        await self.mqttClient.publishIndependentTopic('/house/agents/Automower/control/mode[auto,home,eod,man]', value)

    async def startStopUpdate(self, value: str) -> None:
        await self.mqttClient.publishIndependentTopic('/house/agents/Automower/control/status[start,stop]', value)
