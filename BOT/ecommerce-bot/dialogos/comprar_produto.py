from botbuilder.dialogs import ComponentDialog, WaterfallDialog, WaterfallStepContext
from botbuilder.core import MessageFactory
from botbuilder.dialogs.prompts import TextPrompt, PromptOptions, NumberPrompt


from api.rotas import ProductAPI, PedidoAPI

class ComprarProdutoDialog(ComponentDialog):
    def __init__(self):
        super(ComprarProdutoDialog, self).__init__("ComprarProdutoDialog")

        self.add_dialog(TextPrompt("produtoNomePrompt"))
        self.add_dialog(TextPrompt("clienteIdPrompt"))
        self.add_dialog(NumberPrompt("cartaoIdPrompt"))

        self.add_dialog(
            WaterfallDialog(
                "comprarProdutoWaterfallDialog",
                [
                    self.ask_product_name_step,
                    self.verify_product_and_ask_client_id_step,
                    self.ask_card_id_step,
                    self.create_and_process_order_step,
                ],
            )
        )

        self.initial_dialog_id = "comprarProdutoWaterfallDialog"
        self.product_api = ProductAPI()
        self.pedido_api = PedidoAPI()

    async def ask_product_name_step(self, step_context: WaterfallStepContext):
        """
        Primeiro passo: Pergunta ao usuário o nome do produto.
        """
        prompt_message = MessageFactory.text("Qual produto você gostaria de comprar?")
        return await step_context.prompt("produtoNomePrompt", PromptOptions(prompt=prompt_message))

    async def verify_product_and_ask_client_id_step(self, step_context: WaterfallStepContext):
        """
        Segundo passo: Verifica o produto e pergunta o ID do cliente.
        """
        product_name = step_context.result

        step_context.values["product_name"] = product_name

        produtos_encontrados = self.product_api.verificar_produtos(product_name)

        if produtos_encontrados:
            produto = produtos_encontrados[0]

            if produto.get('estoque', 0) > 0:
                step_context.values["produto_id"] = produto.get('id')
                step_context.values["produto_nome"] = produto.get('nome')
                step_context.values["produto_preco"] = produto.get('preco')

                confirmation_message = MessageFactory.text(
                    f"Ótimo! Encontramos o produto '{produto.get('nome')}' (R$ {produto.get('preco'):.2f}) em estoque. "
                    "Por favor, informe seu ID de cliente para prosseguir."
                )
                return await step_context.prompt("clienteIdPrompt", PromptOptions(prompt=confirmation_message))
            else:
                await step_context.context.send_activity(
                    f"Desculpe, o produto '{product_name}' está fora de estoque no momento."
                )
                return await step_context.end_dialog()
        else:
            await step_context.context.send_activity(
                f"Desculpe, não conseguimos encontrar o produto '{product_name}'. "
                "Por favor, verifique o nome e tente novamente."
            )
            return await step_context.end_dialog()

    async def ask_card_id_step(self, step_context: WaterfallStepContext):
        """
        Terceiro passo: Pergunta o ID do cartão de crédito.
        """
        client_id = step_context.result
        step_context.values["client_id"] = client_id

        if not client_id:
            await step_context.context.send_activity("Parece que você não forneceu um ID de cliente válido. Por favor, tente novamente.")
            return await step_context.end_dialog()

        prompt_message = MessageFactory.text(
            f"Obrigado, {client_id}! Agora, por favor, digite o ID do seu cartão de crédito (apenas números)."
        )
        return await step_context.prompt("cartaoIdPrompt", PromptOptions(prompt=prompt_message))

    async def create_and_process_order_step(self, step_context: WaterfallStepContext):
        """
        Último passo: Cria o pedido e processa o pagamento.
        """
        card_id = int(step_context.result)
        step_context.values["card_id"] = card_id

        product_id = step_context.values.get("produto_id")
        product_name = step_context.values.get("produto_nome")
        client_id = step_context.values.get("client_id")

        await step_context.context.send_activity("Criando seu pedido...")

        pedido_criado = self.pedido_api.criar_pedido(client_id, [product_id])

        if pedido_criado:
            pedido_id = pedido_criado.get('id')
            await step_context.context.send_activity(
                f"Pedido '{pedido_id}' criado com sucesso, status 'pendente'."
            )

            await step_context.context.send_activity("Processando o pagamento...")

            pedido_pago = self.pedido_api.processar_pagamento_pedido(pedido_id, card_id)

            if pedido_pago and pedido_pago.get('status') == 'pago':
                await step_context.context.send_activity(
                    f"Pagamento do pedido '{pedido_id}' para '{product_name}' realizado com sucesso! "
                    f"Status: {pedido_pago.get('status')}. "
                    "Seu produto será preparado para envio."
                )
            else:
                await step_context.context.send_activity(
                    f"Desculpe, o pagamento do pedido '{pedido_id}' não pôde ser processado. "
                    "Por favor, verifique os detalhes do seu cartão ou tente novamente mais tarde."
                )
        else:
            await step_context.context.send_activity(
                "Não foi possível criar o pedido no momento. Por favor, tente novamente mais tarde."
            )

        return await step_context.end_dialog()