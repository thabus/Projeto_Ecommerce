from botbuilder.dialogs import ComponentDialog, WaterfallDialog, WaterfallStepContext
from botbuilder.core import MessageFactory
from botbuilder.dialogs.prompts import TextPrompt, PromptOptions

class VerificarPedidoDialog(ComponentDialog):
    def __init__(self):
        super(VerificarPedidoDialog, self).__init__("VerificarPedidoDialog")

        self.add_dialog(TextPrompt("nomePrompt"))

        self.add_dialog(
            WaterfallDialog(
                "verificarPedidoWaterfallDialog",
                [
                    self.prompt_option_step,
                    self.prompt_process_product_name_step,

                ],
            )
        )

        self.initial_dialog_id = "verificarPedidoWaterfallDialog"

    async def prompt_process_product_name_step(self, step_context: WaterfallStepContext):
        nomeProduto = step_context.result

        # substituir pela API
        pedidos = [
            {"produto": "Camisa", "status": "Enviado"},
            {"produto": "Calça", "status": "Processando"},
        ]
        resultado = next((p for p in pedidos if p["produto"].lower() == nomeProduto.lower()), None)

        if resultado:
            resposta = f"O status do seu pedido '{nomeProduto}' é: {resultado['status']}."
        else:
            resposta = f"Não encontramos nenhum pedido para o produto '{nomeProduto}'."

        await step_context.context.send_activity(MessageFactory.text(resposta))
        return await step_context.end_dialog()


