from botbuilder.dialogs import ComponentDialog, WaterfallDialog, WaterfallStepContext
from botbuilder.core import MessageFactory
from botbuilder.dialogs.prompts import TextPrompt, PromptOptions, NumberPrompt, ChoicePrompt, ConfirmPrompt
from botbuilder.dialogs.choices import Choice

from api.rotas import ProductAPI, PedidoAPI, UsuarioAPI

class ComprarProdutoDialog(ComponentDialog):
    def __init__(self):
        super(ComprarProdutoDialog, self).__init__("ComprarProdutoDialog")

        self.PROMPT_USER_ID = "userIdPrompt"
        self.PROMPT_CHOICE_ORDER_TYPE = "choiceOrderTypePrompt"
        self.PROMPT_PENDING_ORDER_ID = "pendingOrderIdPrompt"
        self.PROMPT_PRODUCT_NAME = "productNamePrompt"
        self.PROMPT_CHOOSE_PRODUCT_ID = "chooseProductIdPrompt"
        self.PROMPT_ADD_MORE_PRODUCTS = "addMoreProductsPrompt"
        self.PROMPT_CARD_ID = "cardIdPrompt"
        self.PROMPT_CONFIRM_PAYMENT = "confirmPaymentPrompt"

        self.add_dialog(TextPrompt(self.PROMPT_USER_ID))
        self.add_dialog(ChoicePrompt(self.PROMPT_CHOICE_ORDER_TYPE))
        self.add_dialog(TextPrompt(self.PROMPT_PENDING_ORDER_ID))
        self.add_dialog(TextPrompt(self.PROMPT_PRODUCT_NAME))
        self.add_dialog(TextPrompt(self.PROMPT_CHOOSE_PRODUCT_ID))
        self.add_dialog(ConfirmPrompt(self.PROMPT_ADD_MORE_PRODUCTS))
        self.add_dialog(NumberPrompt(self.PROMPT_CARD_ID))
        self.add_dialog(ConfirmPrompt(self.PROMPT_CONFIRM_PAYMENT))

        self.add_dialog(
            WaterfallDialog(
                "comprarProdutoWaterfallDialog",
                [
                    self.ask_user_id_step,
                    self.verify_user_and_ask_order_type_step,
                    self.handle_order_type_choice_step,
                    self.process_new_or_pending_order_flow_step,
                    self.select_product_from_list_step,
                    self.ask_card_id_or_confirm_new_order_payment_step,
                    self.ask_for_card_id_step,
                    self.process_payment_step,
                    self.final_step
                ],
            )
        )

        self.initial_dialog_id = "comprarProdutoWaterfallDialog"
        self.product_api = ProductAPI()
        self.pedido_api = PedidoAPI()
        self.usuario_api = UsuarioAPI()
        self.produtos_para_novo_pedido_ids = []

    async def ask_user_id_step(self, step_context: WaterfallStepContext):
        if step_context.options and isinstance(step_context.options, dict):
            step_context.values.update(step_context.options)
            return await step_context.next(step_context.values.get("user_id"))
        return await step_context.prompt(self.PROMPT_USER_ID, PromptOptions(prompt=MessageFactory.text("Por favor, informe seu identificador de usuário (ID):")))

    async def verify_user_and_ask_order_type_step(self, step_context: WaterfallStepContext):
        user_id = step_context.result
        if "user_id" not in step_context.values: step_context.values["user_id"] = user_id
        if "order_type_choice" in step_context.values: return await step_context.next(Choice(value=step_context.values["order_type_choice"]))
        usuario_existente = self.usuario_api.buscar_usuario_por_id(user_id)
        if usuario_existente:
            step_context.values["user_name"] = usuario_existente.get("nome", "Usuário Desconhecido")
            welcome_message = MessageFactory.text(f"Olá, {step_context.values['user_name']}! Como posso ajudar?")
            return await step_context.prompt(self.PROMPT_CHOICE_ORDER_TYPE, PromptOptions(prompt=welcome_message, choices=[Choice("Criar novo pedido"), Choice("Pagar pedido pendente")]))
        else:
            await step_context.context.send_activity("Usuário não encontrado."); return await step_context.end_dialog()

    async def handle_order_type_choice_step(self, step_context: WaterfallStepContext):
        choice = step_context.result.value
        if "order_type_choice" not in step_context.values:
            step_context.values["order_type_choice"] = choice
            if choice == "Criar novo pedido": self.produtos_para_novo_pedido_ids = []
        if choice == "Pagar pedido pendente": return await step_context.next(None)
        elif choice == "Criar novo pedido": return await step_context.prompt(self.PROMPT_PRODUCT_NAME, PromptOptions(prompt=MessageFactory.text("Qual o nome do produto que você deseja adicionar?")))
        else: await step_context.context.send_activity("Não entendi sua escolha."); return await step_context.replace_dialog(self.initial_dialog_id)

    async def process_new_or_pending_order_flow_step(self, step_context: WaterfallStepContext):
        order_type_choice = step_context.values.get("order_type_choice")
        if order_type_choice == "Criar novo pedido":
            product_name_input = step_context.result
            if isinstance(product_name_input, str) and product_name_input.upper() == "SAIR": return await step_context.next(None)
            produtos_encontrados = self.product_api.verificar_produtos(product_name_input)
            if not produtos_encontrados: await step_context.context.send_activity(f"Produto '{product_name_input}' não encontrado."); return await step_context.replace_dialog(self.initial_dialog_id, step_context.values)
            if len(produtos_encontrados) == 1: return await step_context.next(produtos_encontrados)
            if len(produtos_encontrados) > 1:
                step_context.values["produtos_encontrados_multi"] = produtos_encontrados
                response_message = "Encontrei mais de um produto com esse nome:\n\n"
                for p in produtos_encontrados:
                    response_message += (f"**ID:** {p.get('id', 'N/A')}\n\n" + f"**Nome:** {p.get('nome', 'N/A')}\n\n" + f"**Preço:** R$ {p.get('preco', 0.0):.2f}\n\n" + f"----------\n")
                response_message = response_message.rstrip("----------\n")
                await step_context.context.send_activity(MessageFactory.text(response_message))
                return await step_context.prompt(self.PROMPT_CHOOSE_PRODUCT_ID, PromptOptions(prompt=MessageFactory.text("Por favor, digite o ID do produto que você deseja escolher.")))
        elif order_type_choice == "Pagar pedido pendente":
            user_id = step_context.values.get("user_id")
            pedidos_pendentes = self.pedido_api.listar_pedidos_por_usuario_e_status(user_id, "pendente")
            if pedidos_pendentes:
                step_context.values["pedidos_pendentes_usuario"] = pedidos_pendentes
                response_message = f"Seus pedidos pendentes, {step_context.values['user_name']}:\n\n"
                for p in pedidos_pendentes:
                    response_message += (f"**ID do Pedido:** {p.get('id', 'N/A')}\n\n" + f"**Produtos:** {', '.join(p.get('produtos', []))}\n\n" + f"**Valor Total:** R$ {p.get('valorTotal', 0.0):.2f}\n\n" + f"**Data do Pedido:** {p.get('dataPedido', 'N/A')}\n\n" + f"----------\n")
                response_message = response_message.rstrip("----------\n")
                await step_context.context.send_activity(MessageFactory.text(response_message))
                return await step_context.prompt(self.PROMPT_PENDING_ORDER_ID, PromptOptions(prompt=MessageFactory.text("Por favor, digite o ID do pedido que deseja pagar.")))
            else:
                await step_context.context.send_activity("Você não possui pedidos pendentes no momento.")
                return await step_context.next(None)

    async def select_product_from_list_step(self, step_context: WaterfallStepContext):
        order_type_choice = step_context.values.get("order_type_choice")
        if order_type_choice != "Criar novo pedido": return await step_context.next(step_context.result)
        if step_context.result is None: return await step_context.next(False)

        produto_selecionado = None
        if isinstance(step_context.result, list):
            produto_selecionado = step_context.result[0]
        else:
            chosen_id = str(step_context.result)
            produtos_encontrados = step_context.values.get("produtos_encontrados_multi", [])
            produto_selecionado = next((p for p in produtos_encontrados if str(p.get('id')) == chosen_id), None)

        if not produto_selecionado: await step_context.context.send_activity("ID inválido."); return await step_context.replace_dialog(self.initial_dialog_id, step_context.values)

        if produto_selecionado.get('estoque', 0) > 0:
            self.produtos_para_novo_pedido_ids.append(produto_selecionado.get('id'))

            prompt_message = (
                f"'{produto_selecionado.get('nome')}' (R$ {produto_selecionado.get('preco', 0.0):.2f}) "
                f"adicionado. Deseja acrescentar mais algum produto?"
            )
            return await step_context.prompt(self.PROMPT_ADD_MORE_PRODUCTS, PromptOptions(prompt=MessageFactory.text(prompt_message)))
        else:
            await step_context.context.send_activity(f"'{produto_selecionado.get('nome')}' está fora de estoque.")
            return await step_context.prompt(self.PROMPT_ADD_MORE_PRODUCTS, PromptOptions(prompt=MessageFactory.text("Deseja tentar adicionar outro produto?")))

    async def ask_card_id_or_confirm_new_order_payment_step(self, step_context: WaterfallStepContext):
        order_type_choice = step_context.values.get("order_type_choice")

        if order_type_choice == "Pagar pedido pendente":
            pedido_id_to_pay = step_context.result
            if not pedido_id_to_pay: return await step_context.end_dialog()
            if isinstance(pedido_id_to_pay, str) and pedido_id_to_pay.upper() == "SAIR": await step_context.context.send_activity("Operação cancelada."); return await step_context.end_dialog()
            pedidos_pendentes_usuario = step_context.values.get("pedidos_pendentes_usuario", [])
            pedido_existe = next((p for p in pedidos_pendentes_usuario if str(p.get('id')) == str(pedido_id_to_pay)), None)

            if pedido_existe: step_context.values["pedido_a_pagar_id"] = pedido_id_to_pay; return await step_context.next(pedido_existe)
            else: await step_context.context.send_activity("Pedido não encontrado."); return await step_context.end_dialog()

        elif order_type_choice == "Criar novo pedido":
            if isinstance(step_context.result, bool) and step_context.result: return await step_context.replace_dialog(self.initial_dialog_id, step_context.values)
            else:
                if not self.produtos_para_novo_pedido_ids: await step_context.context.send_activity("Nenhum produto foi adicionado."); return await step_context.end_dialog()
                await step_context.context.send_activity("Finalizando a adição de produtos. Criando seu pedido...")
                user_id = step_context.values.get("user_id")
                pedido_criado = self.pedido_api.criar_pedido(user_id, self.produtos_para_novo_pedido_ids)
                if pedido_criado:
                    step_context.values["pedido_criado_id"] = pedido_criado.get('id')
                    await step_context.context.send_activity(f"Seu pedido '{pedido_criado.get('id')}' foi criado com status 'pendente'.")
                    return await step_context.prompt(self.PROMPT_CONFIRM_PAYMENT, PromptOptions(prompt=MessageFactory.text("Deseja realizar o pagamento agora?")))
                else:
                    await step_context.context.send_activity("Não foi possível criar o pedido.")
                    return await step_context.end_dialog()
        return await step_context.end_dialog()

    async def ask_for_card_id_step(self, step_context: WaterfallStepContext):
        order_type_choice = step_context.values.get("order_type_choice")
        if order_type_choice == "Pagar pedido pendente":
            step_context.values["pedido_a_pagar_details"] = step_context.result
            return await step_context.prompt(self.PROMPT_CARD_ID, PromptOptions(prompt=MessageFactory.text("Por favor, digite o ID do seu cartão de crédito para o pagamento.")))

        confirm_payment_now = step_context.result
        if isinstance(confirm_payment_now, bool):
            if confirm_payment_now:
                return await step_context.prompt(self.PROMPT_CARD_ID, PromptOptions(prompt=MessageFactory.text("Por favor, digite o ID do seu cartão de crédito para o pagamento.")))
            else:
                await step_context.context.send_activity("Seu pedido foi adicionado aos pendentes. Você pode pagá-lo mais tarde.")
                return await step_context.end_dialog()
        return await step_context.end_dialog()

    async def process_payment_step(self, step_context: WaterfallStepContext):
        order_type_choice = step_context.values.get("order_type_choice")
        card_id_raw = step_context.result
        try:
            cartao_id = int(card_id_raw)
            if cartao_id <= 0: raise ValueError("ID do cartão deve ser positivo.")
        except (ValueError, TypeError):
            await step_context.context.send_activity("ID do cartão inválido. Por favor, tente a operação novamente.")
            return await step_context.end_dialog()

        pedido_id_para_pagar = step_context.values.get("pedido_criado_id") if order_type_choice == "Criar novo pedido" else step_context.values.get("pedido_a_pagar_id")
        if not pedido_id_para_pagar:
            await step_context.context.send_activity("Não foi possível encontrar o pedido para pagamento. Por favor, tente novamente.")
            return await step_context.end_dialog()

        await step_context.context.send_activity("Processando o pagamento...")
        pedido_pago = self.pedido_api.processar_pagamento_pedido(pedido_id_para_pagar, cartao_id)

        if pedido_pago and pedido_pago.get('status') == 'pago':
            await step_context.context.send_activity(f"Pagamento do pedido '{pedido_id_para_pagar}' realizado com sucesso!")
        else:
            await step_context.context.send_activity(f"Desculpe, o pagamento do pedido '{pedido_id_para_pagar}' não pôde ser processado.")

        return await step_context.next(None)

    async def final_step(self, step_context: WaterfallStepContext):
        await step_context.context.send_activity("Operação finalizada. Espero ter ajudado!")
        return await step_context.end_dialog()