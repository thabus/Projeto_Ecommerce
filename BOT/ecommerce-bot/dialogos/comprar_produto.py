from botbuilder.dialogs import ComponentDialog, WaterfallDialog, WaterfallStepContext
from botbuilder.core import MessageFactory
from botbuilder.dialogs.prompts import TextPrompt, PromptOptions, NumberPrompt, ChoicePrompt, ConfirmPrompt
from botbuilder.schema import ActivityTypes, TextFormat
from botbuilder.dialogs.choices import Choice

from api.rotas import ProductAPI, PedidoAPI, UsuarioAPI

class ComprarProdutoDialog(ComponentDialog):
    def __init__(self):
        super(ComprarProdutoDialog, self).__init__("ComprarProdutoDialog")

        self.PROMPT_USER_ID = "userIdPrompt"
        self.PROMPT_CHOICE_ORDER_TYPE = "choiceOrderTypePrompt"
        self.PROMPT_PENDING_ORDER_ID = "pendingOrderIdPrompt"
        self.PROMPT_PRODUCT_NAME = "productNamePrompt"
        self.PROMPT_ADD_MORE_PRODUCTS = "addMoreProductsPrompt"
        self.PROMPT_CARD_ID = "cardIdPrompt"
        self.PROMPT_CONFIRM_PAYMENT = "confirmPaymentPrompt"

        self.add_dialog(TextPrompt(self.PROMPT_USER_ID))
        self.add_dialog(ChoicePrompt(self.PROMPT_CHOICE_ORDER_TYPE))
        self.add_dialog(TextPrompt(self.PROMPT_PENDING_ORDER_ID))
        self.add_dialog(TextPrompt(self.PROMPT_PRODUCT_NAME))
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
                    self.ask_card_id_or_confirm_new_order_payment_step,
                    self.create_and_process_payment_step,
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
        # Pede o id do usuario
        return await step_context.prompt(
            self.PROMPT_USER_ID,
            PromptOptions(prompt=MessageFactory.text("Por favor, informe seu identificador de usuário (ID):"))
        )

    async def verify_user_and_ask_order_type_step(self, step_context: WaterfallStepContext):
        # Verifica o usuário e pergunta se deseja criar novo pedido ou pagar um pendente
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
        #Direciona o fluxo baseado na escolha do usuário (Criar novo ou Pagar pendente)
        choice = step_context.result.value
        step_context.values["order_type_choice"] = choice

        if choice == "Pagar pedido pendente":
            return await step_context.next(None) # Pula para o próximo passo para listar pedidos pendentes
        elif choice == "Criar novo pedido":
            # Limpa a lista de produtos temporária para um novo pedido
            self.produtos_para_novo_pedido_ids = []
            return await step_context.prompt(
                self.PROMPT_PRODUCT_NAME,
                PromptOptions(prompt=MessageFactory.text("Qual o nome do primeiro produto que você deseja adicionar ao novo pedido?"))
            )
        else:
            await step_context.context.send_activity("Não entendi sua escolha. Por favor, tente novamente.")
            return await step_context.replace_dialog(self.initial_dialog_id)

    async def process_new_or_pending_order_flow_step(self, step_context: WaterfallStepContext):
        # Gerencia o fluxo de criação de novo pedido ou listagem de pendente.
        user_id = step_context.values.get("user_id")
        order_type_choice = step_context.values.get("order_type_choice")

        if order_type_choice == "Pagar pedido pendente":
            pedidos_pendentes = await self.pedido_api.listar_pedidos_por_usuario_e_status(user_id, "pendente")
            step_context.values["pedidos_pendentes_usuario"] = pedidos_pendentes

            if pedidos_pendentes:
                response_message = f"Seus pedidos pendentes, {step_context.values['user_name']}:\n\n"
                for pedido in pedidos_pendentes:
                    # 'produtos' agora é a lista de nomes no seu modelo de Pedido
                    produtos_nomes = pedido.get('produtos', [])
                    response_message += (
                        f"**ID do Pedido:** {pedido.get('id', 'N/A')}\n"
                        f"**Produtos:** {', '.join(produtos_nomes) if produtos_nomes else 'N/A'}\n"
                        f"**Valor Total:** R$ {pedido.get('valorTotal', 0.0):.2f}\n"
                        f"**Data:** {pedido.get('dataPedido', 'N/A')}\n"
                        f"----------\n"
                    )
                response_message = response_message.rstrip("----------\n")

                activity = MessageFactory.text(response_message)
                activity.text_format = TextFormat.Markdown
                await step_context.context.send_activity(activity)

                return await step_context.prompt(
                    self.PROMPT_PENDING_ORDER_ID,
                    PromptOptions(prompt=MessageFactory.text("Por favor, digite o ID do pedido que você deseja pagar."))
                )
            else:
                await step_context.context.send_activity("Você não possui pedidos pendentes no momento.")
                return await step_context.end_dialog()

        elif order_type_choice == "Criar novo pedido":
            # resultado do PROMPT_PRODUCT_NAME OU loop de adicionar mais produtos
            product_name = step_context.result

            # Se o usuário digitou "SAIR"
            if isinstance(product_name, str) and product_name.upper() == "SAIR":
                await step_context.context.send_activity("Operação cancelada. Voltando ao menu principal.")
                return await step_context.end_dialog()

            produtos_encontrados = self.product_api.verificar_produtos(product_name)

            if produtos_encontrados:
                produto = produtos_encontrados[0]
                if produto.get('estoque', 0) > 0:
                    self.produtos_para_novo_pedido_ids.append(produto.get('id'))

                    # Pergunta se quer acrescentar mais produtos
                    return await step_context.prompt(
                        self.PROMPT_ADD_MORE_PRODUCTS,
                        PromptOptions(
                            prompt=MessageFactory.text(f"'{produto.get('nome')}' (R$ {produto.get('preco', 0.0):.2f}) adicionado. Deseja acrescentar mais algum produto?"),
                            retry_prompt=MessageFactory.text("Por favor, responda 'Sim' ou 'Não'.")
                        )
                    )
                else:
                    await step_context.context.send_activity(f"Desculpe, o produto '{product_name}' está fora de estoque no momento.")
                    return await step_context.end_dialog()
            else:
                await step_context.context.send_activity(f"Produto '{product_name}' não encontrado. Por favor, digite o nome novamente ou 'SAIR'.")
                # Loop para tentar novamente ou sair
                return await step_context.replace_dialog(self.initial_dialog_id, step_context.values) # Volta ao início do diálogo de compra

        return await step_context.end_dialog() # Em caso de fluxo inesperado


    async def ask_card_id_or_confirm_new_order_payment_step(self, step_context: WaterfallStepContext):
        """
        Passo 5: Para pedido pendente: valida ID e pede cartão. Para novo pedido: lida com loop de "adicionar mais" ou pergunta se quer pagar.
        """
        user_id = step_context.values.get("user_id")
        order_type_choice = step_context.values.get("order_type_choice")

        if order_type_choice == "Pagar pedido pendente":
            # Resultado do PROMPT_PENDING_ORDER_ID
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
            add_more_products = step_context.result # Resultado do PROMPT_ADD_MORE_PRODUCTS (bool)

            if add_more_products:
                # Loop para adicionar mais produtos
                return await step_context.prompt(
                    self.PROMPT_PRODUCT_NAME,
                    PromptOptions(prompt=MessageFactory.text("Ok! Qual o nome do próximo produto que você quer adicionar? (Digite 'SAIR' para finalizar a adição)"))
                )
            else: # Usuário não quer mais produtos, então criamos o pedido
                produtos_ids_compra = self.produtos_para_novo_pedido_ids # Pega a lista acumulada

                if not produtos_ids_compra:
                    await step_context.context.send_activity("Nenhum produto foi adicionado ao seu pedido. Compra cancelada.")
                    return await step_context.end_dialog()

                await step_context.context.send_activity("Finalizando a adição de produtos. Criando seu pedido...")
                pedido_criado = self.pedido_api.criar_pedido(user_id, produtos_ids_compra)

                if pedido_criado:
                    step_context.values["pedido_criado_id"] = pedido_criado.get('id')
                    await step_context.context.send_activity(
                        f"Seu pedido '{pedido_criado.get('id')}' foi criado com status 'pendente'."
                    )
                    # Pergunta se o usuário quer pagar agora
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

        cartao_id = None
        pedido_id_para_pagar = None

        if order_type_choice == "Pagar pedido pendente":
            cartao_id = int(step_context.result) # Resultado do PROMPT_CARD_ID
            pedido_id_para_pagar = step_context.values.get("pedido_a_pagar_id")
        elif order_type_choice == "Criar novo pedido":
            confirm_payment_now = step_context.result # Resultado do PROMPT_CONFIRM_PAYMENT (bool)

            if not confirm_payment_now:
                await step_context.context.send_activity("Seu pedido foi adicionado aos pendentes. Você pode pagá-lo mais tarde.")
                return await step_context.end_dialog() # Termina o diálogo

            # Se o usuário confirmou pagamento, precisamos pedir o ID do cartão AGORA
            # Este é um loop: Se o usuário confirmou pagamento, mas o ID do cartão ainda não foi pedido,
            # voltamos ao prompt do cartão e o próximo passo será este mesmo passo com o ID do cartão.
            if step_context.result is True and not step_context.values.get("card_id_asked"):
                step_context.values["card_id_asked"] = True # Marca que já pedimos
                return await step_context.prompt(
                    self.PROMPT_CARD_ID,
                    PromptOptions(prompt=MessageFactory.text("Por favor, digite o ID do seu cartão de crédito para o pagamento."))
                )

            # Se chegamos aqui, é porque o usuário já forneceu o ID do cartão
            cartao_id = int(step_context.result) # Resultado do PROMPT_CARD_ID da segunda vez
            pedido_id_para_pagar = step_context.values.get("pedido_criado_id")

        # Se por algum motivo o cartao_id não foi obtido (ex: usuário digitou algo não numérico)
        if cartao_id is None or cartao_id <= 0:
            await step_context.context.send_activity("ID do cartão inválido. Tente novamente ou digite 'SAIR'.")
            return await step_context.end_dialog()

        # Validação de existência do cartão (opcional, pode ser feito pela API de usuário/cartão)
        # Por enquanto, confiamos que a API de pagamento lidará com cartões inexistentes.

        await step_context.context.send_activity("Processando o pagamento...")

        pedido_pago = self.pedido_api.processar_pagamento_pedido(pedido_id_para_pagar, cartao_id)

        if pedido_pago and pedido_pago.get('status') == 'pago':
            # Detalhes para a mensagem de sucesso
            if order_type_choice == "Pagar pedido pendente":
                pedido_details = step_context.values.get("pedido_a_pagar_details", {})
                produtos_comprados_nomes = pedido_details.get("produtos", []) # Pega nomes do pedido existente
            else: # Novo pedido
                # Pega a lista de IDs de produtos do novo pedido e pode precisar buscar nomes
                # Uma forma simples de mostrar os nomes se não foram armazenados:
                produtos_comprados_nomes = []
                for prod_id in self.produtos_para_novo_pedido_ids:
                    produto_info = self.product_api.verificar_produtos_por_id(prod_id) # API ProductAPI precisa de um método por ID
                    if produto_info:
                        produtos_comprados_nomes.append(produto_info[0].get("nome", "Produto Desconhecido"))

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

        return await step_context.next(None)

    async def final_step(self, step_context: WaterfallStepContext):
        """
        Passo final: Termina o diálogo de compra e limpa variáveis temporárias.
        """
        # Limpa a lista de produtos temporária para o próximo novo pedido
        self.produtos_para_novo_pedido_ids = []
        return await step_context.end_dialog()