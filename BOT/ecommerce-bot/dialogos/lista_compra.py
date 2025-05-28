from botbuilder.dialogs import ComponentDialog, WaterfallDialog, WaterfallStepContext
from botbuilder.core import MessageFactory

class Listacompra(ComponentDialog):
    def __init__(self):
        super(Listacompra, self).__init__("Listacompra")

        self.add_dialog(
            WaterfallDialog(
                "ListacompraWaterfallDialog",
                [
                    self.prompt_option_step,
                ],
            )
        )

        self.initial_dialog_id = "ListacompraWaterfallDialog"

    async def prompt_option_step(self, step_context: WaterfallStepContext) :
        await step_context.context.send_activity("Você está consultando o extrato de compras.")
        return await step_context.end_dialog()
