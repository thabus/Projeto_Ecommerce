from botbuilder.dialogs import ComponentDialog, WaterfallDialog, WaterfallStepContext, ListStyle
from botbuilder.core import MessageFactory
from botbuilder.dialogs.prompts import TextPrompt, PromptOptions, ChoicePrompt
from botbuilder.dialogs.choices import Choice 

from api.rotas import PedidoAPI

class VerificarPedidoDialog(ComponentDialog):
    def __init__(self):
        super(VerificarPedidoDialog, self).__init__("VerificarPedidoDialog")

        self.add_dialog(TextPrompt("nomePrompt"))
        self.add_dialog(ChoicePrompt("continueChoicePrompt"))

        self.add_dialog(
            WaterfallDialog(
                "verificarPedidoWaterfallDialog",
                [
                    self.prompt_option_step,
                    self.prompt_process_product_name_step,
                    self.ask_to_continue_step,
                    self.process_continue_step,
                ],
            )
        )

        self.initial_dialog_id = "verificarPedidoWaterfallDialog"
        self.pedido_api = PedidoAPI()

    async def prompt_option_step(self, step_context: WaterfallStepContext):
        prompt = MessageFactory.text("Informe o nome do produto do pedido que deseja consultar.")
        return await step_context.prompt("nomePrompt", PromptOptions(prompt=prompt))

    async def prompt_process_product_name_step(self, step_context: WaterfallStepContext):
        nomeProduto = step_context.result

        pedidos_encontrados = self.pedido_api.verificar_pedidos_por_produto(nomeProduto)

        if pedidos_encontrados:
            resposta = f"Encontrei os seguintes pedidos para o produto '{nomeProduto}':\n\n"

            for pedido in pedidos_encontrados:
                pedido_id = pedido.get('id', 'N/A')
                status = pedido.get('status', 'N/A')
                valor_total = pedido.get('valorTotal', 0.0)
                data_pedido = pedido.get('dataPedido', 'N/A')
                usuario_nome = pedido.get('usuarioNome', 'N/A')

                resposta += (
                    f"**ID do Pedido:** {pedido_id}\n\n"
                    f"**Usuario:** {usuario_nome}\n\n"
                    f"**Valor Total:** R$ {valor_total:.2f}\n\n"
                    f"**Data do Pedido:** {data_pedido}\n\n"
                    f"**Status:** {status}\n\n"
                    f"----------\n\n"
                )

            if pedidos_encontrados:
                resposta = resposta.rstrip("----------\n")
        else:
            resposta = f"Não encontramos nenhum pedido para o produto '{nomeProduto}'."

        await step_context.context.send_activity(MessageFactory.text(resposta))
        return await step_context.next(None)
    
    async def ask_to_continue_step(self, step_context: WaterfallStepContext):

        return await step_context.prompt(
            "continueChoicePrompt",
            PromptOptions(
                prompt=MessageFactory.text("Deseja consultar outro produto?"),
                choices=[Choice("Sim"), Choice("Não")],
                style=ListStyle.suggested_action,
            ),
        )

    async def process_continue_step(self, step_context: WaterfallStepContext):

        if step_context.result.value == "Sim": 
            # Reinicia o diálogo atual
            return await step_context.replace_dialog(self.initial_dialog_id)
        else:
            # Encerra o diálogo atual e volta para o menu principal
            return await step_context.end_dialog()