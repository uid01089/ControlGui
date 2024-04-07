from nicegui import ui
from ContextIf import ContextIf
from guis.GuiIf import GuiIf
from PythonLib.StringUtil import StringUtil


class PvGui(GuiIf):
    def __init__(self, context: ContextIf):
        self.context = context
        self.mqttClient = None
        self.wintermodus = None
        self.soc = None
        self.pcsPvTotalPower = None

    async def setup(self) -> None:

        self.mqttClient = await self.context.getMqttClient()

        await self.mqttClient.subscribeIndependentTopic('/house/basement/ess/essinfo_common/BATT/soc', self.__receivedSoc)
        await self.mqttClient.subscribeIndependentTopic('/house/basement/ess/essinfo_home/statistics/pcs_pv_total_power', self.__receivedPcsPvTotalPower)
        await self.mqttClient.subscribeIndependentTopic('/house/agents/Ess2Mqtt/data/winterstatus', self.__receivedWinterModus)

        with ui.row().classes('w-full'):
            ui.label('SOC: ')
            ui.knob(0.0, show_value=True).bind_value(self, 'soc').disable()
            ui.label('Power [W]: ')
            ui.label().bind_text(self, 'pcsPvTotalPower')

        with ui.row().classes('w-full'):
            ui.label("Wintermodus: ")
            ui.toggle(options={True: 'An', False: 'Aus'})\
                .bind_value(self, 'wintermodus')\
                .on("click", lambda e: self.mqttUpdate(e.sender.value))

    def __receivedWinterModus(self, payload: str) -> None:
        self.wintermodus = StringUtil.isBoolean(payload)

    def __receivedPcsPvTotalPower(self, payload: str) -> None:
        self.pcsPvTotalPower = int(payload)

    def __receivedSoc(self, payload: str) -> None:
        self.soc = float(payload) / 100

    async def mqttUpdate(self, value: bool) -> None:
        match (value):
            case True:
                await self.mqttClient.publishIndependentTopic('/house/agents/Ess2Mqtt/control/setWinter[On,Off]', 'On')
            case False:
                await self.mqttClient.publishIndependentTopic('/house/agents/Ess2Mqtt/control/setWinter[On,Off]', 'Off')
