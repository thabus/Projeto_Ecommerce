from botbuilder.dialogs import ComponentDialog, WaterfallDialog, WaterfallStepContext, TextPrompt, PromptOptions
from botbuilder.core import MessageFactory

from api.rotas import PedidoPagoAPI

class ListaCompra(ComponentDialog):
    def __init__(self):
        super(ListaCompra, self).__init__("ListaCompra")

        self.PROMPT_USER_ID = "userIdPromptForList"
        self.add_dialog(TextPrompt(self.PROMPT_USER_ID))

        self.add_dialog(
            WaterfallDialog(
                "ListaCompraWaterfallDialog",
                [
                    self.ask_for_user_id_step,
                    self.display_paid_orders_step,
                ],
            )
        )

        self.initial_dialog_id = "ListaCompraWaterfallDialog"
        self.pedido_pago_api = PedidoPagoAPI()

    async def ask_for_user_id_step(self, step_context: WaterfallStepContext):
        """
        Este passo pede o ID do usuário para filtrar as compras.
        """
        return await step_context.prompt(
            self.PROMPT_USER_ID,
            PromptOptions(prompt=MessageFactory.text("Por favor, informe o seu ID de usuário para vermos suas compras."))
        )

    async def display_paid_orders_step(self, step_context: WaterfallStepContext):
        usuario_id = step_context.result
        await step_context.context.send_activity("Buscando seu extrato de compras realizadas...")

        compras_realizadas = self.pedido_pago_api.verificar_lista_compras(usuario_id)

        resposta = ""
        if compras_realizadas:
            if isinstance(compras_realizadas, dict) and "message" in compras_realizadas:
                 resposta = "Não encontramos nenhuma compra realizada para o seu usuário."
            else:
                resposta_detalhada = "Aqui está a lista das suas compras realizadas:\n\n"
                for compra in compras_realizadas:
                    compra_id = compra.get('id', 'N/A')
                    produtos_nomes = compra.get('produtos', [])
                    valor_total = compra.get('valorTotal', 0.0)
                    data_pedido = compra.get('dataPedido', 'N/A')

                    resposta_detalhada += (
                        f"**ID do Pedido:** {compra_id}\n\n"
                        f"**Produtos:** {', '.join(produtos_nomes)}\n\n"
                        f"**Valor Total:** R$ {valor_total:.2f}\n\n"
                        f"**Data do Pedido:** {data_pedido}\n\n"
                        f"----------\n"
                    )

                resposta = resposta_detalhada.rstrip("----------\n")
        else:
            resposta = "Não encontramos nenhuma compra realizada para o seu usuário."

        await step_context.context.send_activity(MessageFactory.text(resposta))
        return await step_context.end_dialog()