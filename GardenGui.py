from nicegui import ui
from ContextIf import ContextIf
from GuiIf import GuiIf
from PythonLib.StringUtil import StringUtil


class GardenGui(GuiIf):
    def __init__(self, context: ContextIf):
        self.context = context
        self.mqttClient = None
        self.wintermodus = None
        self.soc = None

    async def setup(self) -> None:

        self.mqttClient = await self.context.getMqttClient()

        # await self.mqttClient.subscribeIndependentTopic('/house/basement/ess/essinfo_common/BATT/soc', self.__receivedSoc)
        # await self.mqttClient.subscribeIndependentTopic('/house/agents/Ess2Mqtt/data/winterstatus', self.__receivedWinterModus)

        with ui.row().classes('w-full'):
            ui.label('SOC: ')
            ui.label('').bind_text(self, 'soc')

        with ui.row().classes('w-full'):
            ui.label("Wintermodus: ")
            ui.toggle(options={True: 'An', False: 'Aus'})\
                .bind_value(self, 'wintermodus')\
                .on("click", lambda e: self.mqttUpdate(e.sender.value))

    def __receivedWinterModus(self, payload: str) -> None:
        self.wintermodus = StringUtil.isBoolean(payload)

    def __receivedSoc(self, payload: str) -> None:
        self.soc = payload

    async def mqttUpdate(self, value: bool) -> None:
        match (value):
            case True:
                pass
                # await self.mqttClient.publishIndependentTopic('/house/agents/Ess2Mqtt/control/setWinter[On,Off]', 'On')
            case False:
                pass
                # await self.mqttClient.publishIndependentTopic('/house/agents/Ess2Mqtt/control/setWinter[On,Off]', 'Off')
