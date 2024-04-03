from datetime import datetime
from ContextIf import ContextIf
from GuiIf import GuiIf
from nicegui import ui

from PythonLib.StringUtil import StringUtil

INPUT_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"


class ChargeControlGui(GuiIf):
    def __init__(self, context: ContextIf):
        self.context = context
        self.startTime = '00:00'
        self.endTime = '00:00'
        self.startDate = '2023-01-01'
        self.endDate = '2023-01-01'
        self.currentTime = ''
        self.automaticMode = None
        self.mqttClient = None
        self.timeString = None
        self.endDateTime = None
        self.startDateTime = None

    async def setup(self) -> None:

        self.mqttClient = await self.context.getMqttClient()
        await self.mqttClient.subscribeIndependentTopic('/house/agents/ChargeControl/data/OverallChargeControlState', self.__receivedOverallChargeControlState)
        await self.mqttClient.subscribeIndependentTopic('/house/agents/ChargeControl/data/TimeCharge/Time', self.__receivedCurrentTime)

        with ui.row().classes('w-full'):
            ui.label("Automatikbetrieb: ")
            ui.toggle({False: 'Aus', True: 'An'})\
                .bind_value(self, 'automaticMode')\
                .on("click", lambda e: self.automaticModeUpdate(e.sender.value))

        with ui.row().classes('w-full'):
            ui.label("Zeitgesteuertes Laden")
            ui.date(on_change=lambda e: self.updateTime()).bind_value(self, 'startDate')
            ui.time(on_change=lambda e: self.updateTime()).bind_value(self, 'startTime')
            ui.date(on_change=lambda e: self.updateTime()).bind_value(self, 'endDate')
            ui.time(on_change=lambda e: self.updateTime()).bind_value(self, 'endTime')

        with ui.row().classes('w-full'):
            ui.button('Update Zeiten', on_click=self.__update).classes('w-full').bind_text(self, 'timeString')

    async def __update(self) -> None:
        if self.startDateTime and self.endDateTime:
            await self.mqttClient.publishIndependentTopic('/house/agents/ChargeControl/control/TimeCharge/StartTime', self.startDateTime.strftime(INPUT_FORMAT))
            await self.mqttClient.publishIndependentTopic('/house/agents/ChargeControl/control/TimeCharge/EndTime', self.endDateTime.strftime(INPUT_FORMAT))

    async def updateTime(self) -> None:
        self.startDateTime = datetime.strptime(f'{self.startDate} {self.startTime}', "%Y-%m-%d %H:%M")
        self.endDateTime = datetime.strptime(f'{self.endDate} {self.endTime}', "%Y-%m-%d %H:%M")

        self.timeString = self.startDateTime.strftime("%d.%m.%Y %H:%M") + " - " + self.endDateTime.strftime("%d.%m.%Y %H:%M")

    async def automaticModeUpdate(self, value: bool) -> None:
        match (value):
            case True:
                await self.mqttClient.publishIndependentTopic('/house/agents/ChargeControl/control/AutomaticMode[On,Off]', 'On')
            case False:
                await self.mqttClient.publishIndependentTopic('/house/agents/ChargeControl/control/AutomaticMode[On,Off]', 'Off')

    def __receivedOverallChargeControlState(self, payload: str) -> None:
        self.automaticMode = (False if payload == 'Manuel' else True)

    def __receivedCurrentTime(self, payload: str) -> None:
        self.currentTime = payload
