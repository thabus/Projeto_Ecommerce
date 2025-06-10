from botbuilder.dialogs import ComponentDialog, WaterfallDialog, WaterfallStepContext
from botbuilder.core import MessageFactory

from api.rotas import PedidoPagoAPI

class ListaCompra(ComponentDialog):
    def __init__(self):
        super(ListaCompra, self).__init__("ListaCompra")

        self.add_dialog(
            WaterfallDialog(
                "ListaCompraWaterfallDialog",
                [
                    self.display_paid_orders_step,
                ],
            )
        )

        self.initial_dialog_id = "ListaCompraWaterfallDialog"
        self.pedido_pago_api = PedidoPagoAPI()

    async def display_paid_orders_step(self, step_context: WaterfallStepContext):
        await step_context.context.send_activity("Você está consultando o extrato de compras realizadas.")

        compras_realizadas = self.pedido_pago_api.verificar_lista_compras()

        if compras_realizadas:
            resposta = "Aqui está a lista das suas compras realizadas:\n\n"
            for compra in compras_realizadas:
                compra_id = compra.get('id', 'N/A')
                produtos_ids = compra.get('produtosIds', [])
                valor_total = compra.get('valorTotal', 0.0)
                data_pedido = compra.get('dataPedido', 'N/A')

                resposta += (
                    f"**ID do Pedido:** {compra_id}\n"
                    f"**Produtos IDs:** {', '.join(map(str, produtos_ids))}\n"
                    f"**Valor Total:** R$ {valor_total:.2f}\n"
                    f"**Data do Pedido:** {data_pedido}\n"
                    f"----------\n"
                )

            if compras_realizadas:
                resposta = resposta.rstrip("----------\n")
        else:
            resposta = "Não encontramos nenhuma compra realizada no seu extrato."

        await step_context.context.send_activity(MessageFactory.text(resposta))
        return await step_context.end_dialog()