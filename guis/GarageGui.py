from nicegui import ui
from ContextIf import ContextIf
from guis.GuiIf import GuiIf


class GarageGui(GuiIf):
    def __init__(self, context: ContextIf):
        self.context = context
        self.distance = 0
        self.time = ""
        self.testCtr = ""
        self.mqttClient = None

    async def setup(self) -> None:

        self.mqttClient = await self.context.getMqttClient()
        await self.mqttClient.subscribeIndependentTopic('/house/garage/tor/distance', self.__receivedDistance)
        await self.mqttClient.subscribeIndependentTopic('/house/garage/tor/time', self.__receivedTime)
        await self.mqttClient.subscribeIndependentTopic('/test/ctr', self.__receivedTestCtr)

        with ui.row().classes('w-full'):
            ui.label("Distanz: ")
            ui.label("").bind_text_from(self, 'distance')
            ui.label("").bind_text_from(self, 'time')
            ui.label("").bind_text_from(self, 'testCtr')

        with ui.row().classes('w-full'):
            ui.button('Auf/Zu!', on_click=self.__update).classes('w-full')

    async def __update(self) -> None:
        await self.mqttClient.publishIndependentTopic("/house/agents/ShellyKlickKlack/set", "shellies/house/garage/toraufzu/relay/0/command")

    def __receivedDistance(self, payload: str) -> None:
        self.distance = int(payload)

    def __receivedTime(self, payload: str) -> None:
        self.time = payload

    def __receivedTestCtr(self, payload: str) -> None:
        self.testCtr = payload
