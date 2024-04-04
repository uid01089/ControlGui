
import logging

from nicegui import app, ui

from Context import Context
from ContextIf import ContextIf


from guis.GuiIf import GuiIf
from PythonLib.DateUtil import DateTimeUtilities
from PythonLib.JsonUtil import JsonUtil

logger = logging.getLogger('ControlGui')


class ControlGui(GuiIf):
    def __init__(self, context: ContextIf) -> None:
        self.context = context
        self.mqttClient = None
        self.scheduler = None
        self.chargerControlGui = None
        self.garageGui = None
        self.jalousienGui = None
        self.pvGui = None
        self.gardenGui = None

    async def setup(self) -> None:

        self.mqttClient = await self.context.getMqttClient()
        self.scheduler = await self.context.getScheduler()
        self.chargerControlGui = await self.context.getChargeControlGui()
        self.garageGui = await self.context.getGarageGui()
        self.jalousienGui = await self.context.getJalousienGui()
        self.pvGui = await self.context.getPvGui()
        self.gardenGui = await self.context.getGardenGui()

        await self.scheduler.scheduleEach(self.__keepAlive, 10000)

        with ui.expansion('PV Anlage', icon='solar_power').classes('bg-blue-50 w-full'):
            await self.pvGui.setup()

        with ui.expansion('E-Auto laden', icon='ev_station').classes('bg-blue-50 w-full'):
            await self.chargerControlGui.setup()

        with ui.expansion('Garage', icon='garage').classes('bg-blue-50 w-full'):
            await self.garageGui.setup()

        with ui.expansion('Jalousien', icon='roller_shades').classes('bg-blue-50 w-full'):
            await self.jalousienGui.setup()

        with ui.expansion('Garten', icon='local_florist').classes('bg-blue-50 w-full'):
            await self.gardenGui.setup()

    async def __keepAlive(self) -> None:
        await self.mqttClient.publishIndependentTopic('/house/agents/ControlGui/heartbeat', DateTimeUtilities.getCurrentDateString())
        await self.mqttClient.publishIndependentTopic('/house/agents/ControlGui/subscriptions', JsonUtil.obj2Json(await self.mqttClient.getSubscriptionCatalog()))


async def main() -> None:
    logging.basicConfig(level=logging.INFO)
    logging.getLogger('ControlGui').setLevel(logging.DEBUG)
    logging.getLogger('PythonLib.Mqtt').setLevel(logging.INFO)

    context = Context()
    await context.setup()

    controlGui = ControlGui(context)
    await controlGui.setup()

app.on_startup(main)
ui.run()
