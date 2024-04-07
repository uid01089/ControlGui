from datetime import datetime
from ContextIf import ContextIf
from guis.GuiIf import GuiIf
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
        self.currentTime = None
        self.automaticMode = None
        self.mqttClient = None
        self.timeString = None
        self.endDateTime = None
        self.startDateTime = None
        self.receivedStartDateTime = None
        self.receivedEndDateTime = None
        self.overallChargeControlState = None
        self.doChargingPVBased = None
        self.isChargingTimeBased = None
        self.egoChargerStatus = None
        self.egoChargerPL1 = None
        self.egoChargerPL2 = None
        self.egoChargerPL3 = None

    async def setup(self) -> None:

        self.mqttClient = await self.context.getMqttClient()
        await self.mqttClient.subscribeIndependentTopic('/house/agents/ChargeControl/data/OverallChargeControlState', self.__receivedOverallChargeControlState)
        await self.mqttClient.subscribeIndependentTopic('/house/agents/ChargeControl/data/TimeCharge/Time', self.__receivedCurrentTime)
        await self.mqttClient.subscribeIndependentTopic('/house/agents/ChargeControl/data/TimeCharge/StartTime', self.__receivedStartDateTime)
        await self.mqttClient.subscribeIndependentTopic('/house/agents/ChargeControl/data/TimeCharge/EndTime', self.__receivedEndDateTime)

        await self.mqttClient.subscribeIndependentTopic('/house/agents/ChargeControl/data/PVSurPlusCharge/doCharging', self.__receivedDoChargingPVBased)
        await self.mqttClient.subscribeIndependentTopic('/house/agents/ChargeControl/data/TimeCharge/isCharging', self.__receivedIsChargingTimeBased)

        await self.mqttClient.subscribeIndependentTopic('/house/agents/eGoCharger/data/Status', self.__receivedEgoChargerStatus)
        await self.mqttClient.subscribeIndependentTopic('/house/agents/eGoCharger/data/PowerChargingL1', self.__receivedEgoChargerPL1)
        await self.mqttClient.subscribeIndependentTopic('/house/agents/eGoCharger/data/PowerChargingL2', self.__receivedEgoChargerPL2)
        await self.mqttClient.subscribeIndependentTopic('/house/agents/eGoCharger/data/PowerChargingL3', self.__receivedEgoChargerPL3)

        with ui.row().classes('w-full'):
            ui.label("Automatikbetrieb: ")
            ui.toggle({False: 'Aus', True: 'An'})\
                .bind_value(self, 'automaticMode')\
                .on("click", lambda e: self.automaticModeUpdate(e.sender.value))
        with ui.row().classes('w-full'):
            ui.label("Betriebsmodus: ")
            ui.label().bind_text(self, 'overallChargeControlState')

        with ui.card():
            ui.markdown('**Wallbox**.')
            with ui.grid(columns=2):
                ui.label('ChargerStatus:')
                ui.label().bind_text(self, 'egoChargerStatus')

                ui.label('PowerL1:')
                ui.label().bind_text(self, 'egoChargerPL1')

                ui.label('PowerL2:')
                ui.label().bind_text(self, 'egoChargerPL2')

                ui.label('PowerL3:')
                ui.label().bind_text(self, 'egoChargerPL3')

        with ui.expansion('Zeitplan', icon='pending_actions').classes('bg-blue-50 w-full').bind_text(self, 'timeString'):

            with ui.row().classes('w-full'):
                ui.label("Empfangene Zeiten: ")
                with ui.row().classes('w-full'):
                    ui.label("Start: ")
                    ui.label().bind_text(self, 'receivedStartDateTime')
                with ui.row().classes('w-full'):
                    ui.label("Jetzt: ")
                    ui.label().bind_text(self, 'currentTime')
                with ui.row().classes('w-full'):
                    ui.label("Stop: ")
                    ui.label().bind_text(self, 'receivedEndDateTime')

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
        self.overallChargeControlState = payload

    def __receivedCurrentTime(self, payload: str) -> None:
        dateTimeObj = datetime.strptime(payload, INPUT_FORMAT)
        self.currentTime = dateTimeObj.strftime("%d.%m.%Y %H:%M")

    def __receivedStartDateTime(self, payload: str) -> None:
        dateTimeObj = datetime.strptime(payload, INPUT_FORMAT)
        self.receivedStartDateTime = dateTimeObj.strftime("%d.%m.%Y %H:%M")

    def __receivedEndDateTime(self, payload: str) -> None:
        dateTimeObj = datetime.strptime(payload, INPUT_FORMAT)
        self.receivedEndDateTime = dateTimeObj.strftime("%d.%m.%Y %H:%M")

    def __receivedDoChargingPVBased(self, payload: str) -> None:
        self.doChargingPVBased = payload

    def __receivedIsChargingTimeBased(self, payload: str) -> None:
        self.isChargingTimeBased = payload

    def __receivedEgoChargerStatus(self, payload: str) -> None:
        self.egoChargerStatus = payload

    def __receivedEgoChargerPL1(self, payload: str) -> None:
        self.egoChargerPL1 = payload

    def __receivedEgoChargerPL2(self, payload: str) -> None:
        self.egoChargerPL2 = payload

    def __receivedEgoChargerPL3(self, payload: str) -> None:
        self.egoChargerPL3 = payload
