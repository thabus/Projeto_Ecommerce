from botbuilder.dialogs import ComponentDialog, WaterfallDialog, WaterfallStepContext
from botbuilder.core import MessageFactory
from botbuilder.dialogs.prompts import TextPrompt, PromptOptions, NumberPrompt, ChoicePrompt, ConfirmPrompt
from botbuilder.dialogs.choices import Choice

# Importa as APIs necessárias do seu arquivo rotas.py
from api.rotas import ProductAPI, PedidoAPI, UsuarioAPI

class ComprarProdutoDialog(ComponentDialog):
    def __init__(self):
        super(ComprarProdutoDialog, self).__init__("ComprarProdutoDialog")

        # Nomes dos prompts
        self.PROMPT_USER_ID = "userIdPrompt"
        self.PROMPT_CHOICE_ORDER_TYPE = "choiceOrderTypePrompt"
        self.PROMPT_PENDING_ORDER_ID = "pendingOrderIdPrompt"
        self.PROMPT_PRODUCT_NAME = "productNamePrompt"
        self.PROMPT_ADD_MORE_PRODUCTS = "addMoreProductsPrompt"
        self.PROMPT_CARD_ID = "cardIdPrompt"
        self.PROMPT_CONFIRM_PAYMENT = "confirmPaymentPrompt"

        # Adiciona os prompts
        self.add_dialog(TextPrompt(self.PROMPT_USER_ID))
        self.add_dialog(ChoicePrompt(self.PROMPT_CHOICE_ORDER_TYPE))
        self.add_dialog(TextPrompt(self.PROMPT_PENDING_ORDER_ID))
        self.add_dialog(TextPrompt(self.PROMPT_PRODUCT_NAME))
        self.add_dialog(ConfirmPrompt(self.PROMPT_ADD_MORE_PRODUCTS))
        self.add_dialog(NumberPrompt(self.PROMPT_CARD_ID))
        self.add_dialog(ConfirmPrompt(self.PROMPT_CONFIRM_PAYMENT))


        # Define os passos do diálogo em cascata (Waterfall)
        self.add_dialog(
            WaterfallDialog(
                "comprarProdutoWaterfallDialog",
                [
                    self.ask_user_id_step,
                    self.verify_user_and_ask_order_type_step,
                    self.handle_order_type_choice_step,
                    self.process_new_or_pending_order_flow_step,
                    self.ask_card_id_or_confirm_new_order_payment_step,
                    self.create_and_process_payment_step,
                    self.final_step # Garante que final_step é o último
                ],
            )
        )

        self.initial_dialog_id = "comprarProdutoWaterfallDialog"
        self.product_api = ProductAPI()
        self.pedido_api = PedidoAPI()
        self.usuario_api = UsuarioAPI()

        self.produtos_para_novo_pedido_ids = []

    async def ask_user_id_step(self, step_context: WaterfallStepContext):
        return await step_context.prompt(
            self.PROMPT_USER_ID,
            PromptOptions(prompt=MessageFactory.text("Por favor, informe seu identificador de usuário (ID):"))
        )

    async def verify_user_and_ask_order_type_step(self, step_context: WaterfallStepContext):
        user_id = step_context.result
        step_context.values["user_id"] = user_id

        usuario_existente = self.usuario_api.buscar_usuario_por_id(user_id)

        if usuario_existente:
            step_context.values["user_name"] = usuario_existente.get("nome", "Usuário Desconhecido")
            welcome_message = MessageFactory.text(f"Olá, {step_context.values['user_name']}! Como posso ajudar com sua compra?")

            return await step_context.prompt(
                self.PROMPT_CHOICE_ORDER_TYPE,
                PromptOptions(
                    prompt=welcome_message,
                    choices=[Choice("Criar novo pedido"), Choice("Pagar pedido pendente")],
                    retry_prompt=MessageFactory.text("Opção inválida. Por favor, escolha 'Criar novo pedido' ou 'Pagar pedido pendente'.")
                )
            )
        else:
            await step_context.context.send_activity("Usuário não encontrado. Tente novamente ou digite 'SAIR' para voltar ao menu de opções.")
            return await step_context.end_dialog()

    async def handle_order_type_choice_step(self, step_context: WaterfallStepContext):
        choice = step_context.result.value
        step_context.values["order_type_choice"] = choice

        if choice == "Pagar pedido pendente":
            return await step_context.next(None)
        elif choice == "Criar novo pedido":
            self.produtos_para_novo_pedido_ids = []
            return await step_context.prompt(
                self.PROMPT_PRODUCT_NAME,
                PromptOptions(prompt=MessageFactory.text("Qual o nome do primeiro produto que você deseja adicionar ao novo pedido?"))
            )
        else:
            await step_context.context.send_activity("Não entendi sua escolha. Por favor, tente novamente.")
            return await step_context.replace_dialog(self.initial_dialog_id)

    async def process_new_or_pending_order_flow_step(self, step_context: WaterfallStepContext):
        user_id = step_context.values.get("user_id")
        order_type_choice = step_context.values.get("order_type_choice")

        if order_type_choice == "Pagar pedido pendente":
            pedidos_pendentes = self.pedido_api.listar_pedidos_por_usuario_e_status(user_id, "pendente")
            step_context.values["pedidos_pendentes_usuario"] = pedidos_pendentes

            if pedidos_pendentes:
                response_message = f"Seus pedidos pendentes, {step_context.values['user_name']}:\n\n"
                for pedido in pedidos_pendentes:
                    produtos_nomes = pedido.get('produtos', [])
                    response_message += (
                        f"**ID do Pedido:** {pedido.get('id', 'N/A')}\n"
                        f"**Produtos:** {', '.join(produtos_nomes) if produtos_nomes else 'N/A'}\n"
                        f"**Valor Total:** R$ {pedido.get('valorTotal', 0.0):.2f}\n"
                        f"**Data:** {pedido.get('dataPedido', 'N/A')}\n"
                        f"----------\n"
                    )
                response_message = response_message.rstrip("----------\n")

                await step_context.context.send_activity(MessageFactory.text(response_message))

                return await step_context.prompt(
                    self.PROMPT_PENDING_ORDER_ID,
                    PromptOptions(prompt=MessageFactory.text("Por favor, digite o ID do pedido que você deseja pagar."))
                )
            else:
                await step_context.context.send_activity("Você não possui pedidos pendentes no momento.")
                return await step_context.end_dialog()

        elif order_type_choice == "Criar novo pedido":
            product_name_input = step_context.result

            if isinstance(product_name_input, str) and product_name_input.upper() == "SAIR":
                return await step_context.next(False) # Avanca para o proximo passo, indicando que não quer mais produtos.

            produtos_encontrados = self.product_api.verificar_produtos(product_name_input)

            if produtos_encontrados:
                produto = produtos_encontrados[0]
                if produto.get('estoque', 0) > 0:
                    self.produtos_para_novo_pedido_ids.append(produto.get('id'))

                    return await step_context.prompt(
                        self.PROMPT_ADD_MORE_PRODUCTS,
                        PromptOptions(
                            prompt=MessageFactory.text(f"'{produto.get('nome')}' (R$ {produto.get('preco', 0.0):.2f}) adicionado. Deseja acrescentar mais algum produto?"),
                            retry_prompt=MessageFactory.text("Por favor, responda 'Sim' ou 'Não'.")
                        )
                    )
                else:
                    await step_context.context.send_activity(f"Desculpe, o produto '{product_name_input}' está fora de estoque no momento.")
                    return await step_context.end_dialog()
            else:
                await step_context.context.send_activity(f"Produto '{product_name_input}' não encontrado. Por favor, digite o nome novamente ou 'SAIR'.")
                return await step_context.replace_dialog(self.initial_dialog_id, step_context.values)

        return await step_context.end_dialog()


    async def ask_card_id_or_confirm_new_order_payment_step(self, step_context: WaterfallStepContext):
        user_id = step_context.values.get("user_id")
        order_type_choice = step_context.values.get("order_type_choice")

        if order_type_choice == "Pagar pedido pendente":
            pedido_id_to_pay = step_context.result

            if isinstance(pedido_id_to_pay, str) and pedido_id_to_pay.upper() == "SAIR":
                await step_context.context.send_activity("Operação cancelada. Voltando ao menu principal.")
                return await step_context.end_dialog()

            pedidos_pendentes_usuario = step_context.values.get("pedidos_pendentes_usuario", [])
            pedido_existe = next((p for p in pedidos_pendentes_usuario if p.get('id') == pedido_id_to_pay), None)

            if pedido_existe:
                step_context.values["pedido_a_pagar_id"] = pedido_id_to_pay
                step_context.values["pedido_a_pagar_details"] = pedido_existe
                return await step_context.prompt(
                    self.PROMPT_CARD_ID,
                    PromptOptions(prompt=MessageFactory.text("Pedido encontrado. Por favor, digite o ID do seu cartão de crédito para o pagamento."))
                )
            else:
                await step_context.context.send_activity("Pedido não encontrado ou não pertence a você. Tente novamente ou digite 'SAIR'.")
                return await step_context.end_dialog()

        elif order_type_choice == "Criar novo pedido":
            add_more_products_result = step_context.result

            if isinstance(add_more_products_result, bool) and add_more_products_result:
                return await step_context.prompt(
                    self.PROMPT_PRODUCT_NAME,
                    PromptOptions(prompt=MessageFactory.text("Ok! Qual o nome do próximo produto que você quer adicionar? (Digite 'SAIR' para finalizar a adição)"))
                )
            else: # Usuário não quer mais produtos (False) ou 'SAIR' veio do prompt do produto
                produtos_ids_compra = self.produtos_para_novo_pedido_ids

                if not produtos_ids_compra:
                    await step_context.context.send_activity("Nenhum produto foi adicionado ao seu pedido. Compra cancelada.")
                    return await step_context.end_dialog()

                await step_context.context.send_activity("Finalizando a adição de produtos. Criando seu pedido...")
                user_id = step_context.values.get("user_id")
                pedido_criado = self.pedido_api.criar_pedido(user_id, produtos_ids_compra)

                if pedido_criado:
                    step_context.values["pedido_criado_id"] = pedido_criado.get('id')
                    await step_context.context.send_activity(
                        f"Seu pedido '{pedido_criado.get('id')}' foi criado com status 'pendente'."
                    )
                    return await step_context.prompt(
                        self.PROMPT_CONFIRM_PAYMENT,
                        PromptOptions(
                            prompt=MessageFactory.text("Deseja realizar o pagamento agora?"),
                            retry_prompt=MessageFactory.text("Por favor, responda 'Sim' ou 'Não'.")
                        )
                    )
                else:
                    await step_context.context.send_activity("Não foi possível criar o pedido no momento. Por favor, tente novamente mais tarde.")
                    return await step_context.end_dialog()

        return await step_context.end_dialog()


    async def create_and_process_payment_step(self, step_context: WaterfallStepContext):
        """
        Passo 6: Lida com o processamento do pagamento.
        """
        order_type_choice = step_context.values.get("order_type_choice")

        cartao_id_raw = step_context.result

        if isinstance(cartao_id_raw, str) and cartao_id_raw.upper() == "SAIR":
            await step_context.context.send_activity("Operação de pagamento cancelada. Voltando ao menu principal.")
            return await step_context.end_dialog()

        cartao_id = None
        pedido_id_para_pagar = None

        if order_type_choice == "Pagar pedido pendente":
            try:
                cartao_id = int(cartao_id_raw)
            except ValueError:
                await step_context.context.send_activity("ID do cartão inválido. Por favor, digite um número ou 'SAIR'.")
                return await step_context.end_dialog()
            pedido_id_para_pagar = step_context.values.get("pedido_a_pagar_id")
        elif order_type_choice == "Criar novo pedido":
            confirm_payment_now = step_context.result

            if isinstance(confirm_payment_now, bool) and not confirm_payment_now:
                await step_context.context.send_activity("Seu pedido foi adicionado aos pendentes. Você pode pagá-lo mais tarde.")
                return await step_context.end_dialog()

            if isinstance(confirm_payment_now, bool) and confirm_payment_now and not step_context.values.get("card_id_asked_for_new_order"):
                step_context.values["card_id_asked_for_new_order"] = True
                return await step_context.prompt(
                    self.PROMPT_CARD_ID,
                    PromptOptions(prompt=MessageFactory.text("Por favor, digite o ID do seu cartão de crédito para o pagamento."))
                )

            try:
                cartao_id = int(cartao_id_raw)
            except ValueError:
                await step_context.context.send_activity("ID do cartão inválido. Por favor, digite um número ou 'SAIR'.")
                return await step_context.end_dialog()

            pedido_id_para_pagar = step_context.values.get("pedido_criado_id")

        if cartao_id is None or cartao_id <= 0:
            await step_context.context.send_activity("ID do cartão inválido ou não fornecido. Tente novamente ou digite 'SAIR'.")
            return await step_context.end_dialog()

        await step_context.context.send_activity("Processando o pagamento...")

        pedido_pago = self.pedido_api.processar_pagamento_pedido(pedido_id_para_pagar, cartao_id)

        if pedido_pago and pedido_pago.get('status') == 'pago':
            produtos_comprados_nomes = []
            if order_type_choice == "Pagar pedido pendente":
                pedido_details = step_context.values.get("pedido_a_pagar_details", {})
                produtos_comprados_nomes = pedido_details.get("produtos", [])
            else: # Novo pedido
                # Buscamos o pedido recém-criado completo para obter os nomes dos produtos
                pedido_recem_criado_completo = self.pedido_api.buscar_pedido_por_id(pedido_id_para_pagar)
                if pedido_recem_criado_completo:
                    produtos_comprados_nomes = pedido_recem_criado_completo.get("produtos", [])
                else:
                    produtos_comprados_nomes = ["produto(s)"] # Fallback

            response_message = (
                f"Pagamento do pedido '{pedido_id_para_pagar}' para "
                f"{', '.join(produtos_comprados_nomes) if produtos_comprados_nomes else 'seus produtos'} realizado com sucesso! "
                f"Status: {pedido_pago.get('status')}. "
                "Seu produto(s) será(ão) preparado(s) para envio."
            )
            await step_context.context.send_activity(MessageFactory.text(response_message))
        else:
            await step_context.context.send_activity(
                f"Desculpe, o pagamento do pedido '{pedido_id_para_pagar}' não pôde ser processado. "
                "Por favor, verifique os detalhes do seu cartão ou tente novamente mais tarde."
            )

        return await step_context.next(None) # Garante que o fluxo continua para o final_step

    async def final_step(self, step_context: WaterfallStepContext):
        """
        Passo final: Termina o diálogo de compra e limpa variáveis temporárias.
        """
        # Limpa a lista de produtos temporária para o próximo novo pedido
        self.produtos_para_novo_pedido_ids = []
        # Remove a flag do cartão de crédito para um novo fluxo
        if "card_id_asked_for_new_order" in step_context.values:
            del step_context.values["card_id_asked_for_new_order"]
        # Mensagem final ou volta ao menu principal
        await step_context.context.send_activity("Operação finalizada. Espero ter ajudado!")
        return await step_context.end_dialog()