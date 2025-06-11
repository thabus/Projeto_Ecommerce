from botbuilder.core import CardFactory
from botbuilder.dialogs import (
    ComponentDialog,
    WaterfallDialog,
    WaterfallStepContext,
    DialogTurnResult,
)
from botbuilder.dialogs.prompts import (
    TextPrompt,
    NumberPrompt,
    ChoicePrompt,
    ConfirmPrompt,
    AttachmentPrompt,
    PromptOptions,
    PromptValidatorContext,
)
from botbuilder.schema import (
    ActionTypes,
    HeroCard,
    CardAction,
    CardImage,
)
from botbuilder.dialogs.choices import Choice
from botbuilder.core import MessageFactory, UserState
from api.rotas import ProductAPI
from dialogos.verificar_pedidos import VerificarPedidoDialog
from dialogos.verificar_produtos import VerificarProdutoDialog
from dialogos.lista_compra import ListaCompra
from dialogos.comprar_produto import ComprarProdutoDialog


class Inicio(ComponentDialog):
    def __init__(self, user_state: UserState):
        super(Inicio, self).__init__("inicio")

        self.user_state = user_state

        # Escolha das opções
        self.add_dialog(ChoicePrompt(ChoicePrompt.__name__))
        self.add_dialog(ConfirmPrompt(ConfirmPrompt.__name__))

        # Adiciona os sub-diálogos
        self.add_dialog(VerificarPedidoDialog())
        self.add_dialog(VerificarProdutoDialog())
        self.add_dialog(ListaCompra())
        self.add_dialog(ComprarProdutoDialog())

        # Tratamento das opções - Waterfall principal
        self.add_dialog(
            WaterfallDialog(
                "inicio",
                [
                    self.prompt_option_step,
                    self.process_option_step,
                    self.loop_step, # Este passo é crucial para o ciclo do menu
                ],
            )
        )

        self.initial_dialog_id = "inicio"

    async def prompt_option_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        # Mensagem inicial do bot ou de retorno ao menu
        # Podemos adicionar uma mensagem de boas-vindas na primeira vez
        if step_context.context.activity.text is None: # Se é o início da conversa ou recém-começou o diálogo
             await step_context.context.send_activity("Olá! Sou seu assistente de compras. O que você gostaria de fazer hoje?")

        return await step_context.prompt(
            ChoicePrompt.__name__,
            PromptOptions(
                prompt=MessageFactory.text("Escolha a opção desejada:"),
                choices=[
                    Choice("Consultar Pedidos"),
                    Choice("Consultar Produtos"),
                    Choice("Extrato de compras"), # Nome da opção para o usuário
                    Choice("Comprar Produto")
                ],
            ),
        )

    async def process_option_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:

        choice = step_context.result.value

        if choice == "Consultar Pedidos":
            return await step_context.begin_dialog("VerificarPedidoDialog")
        elif choice == "Consultar Produtos":
            return await step_context.begin_dialog("VerificarProdutoDialog")
        elif choice == "Extrato de compras":
            return await step_context.begin_dialog("ListaCompra")
        elif choice == "Comprar Produto":
            return await step_context.begin_dialog("ComprarProdutoDialog")
        else: # Caso a opção não seja reconhecida (embora ChoicePrompt ajude a evitar isso)
            await step_context.context.send_activity("Não entendi a opção. Por favor, escolha uma das opções válidas.")
            return await step_context.replace_dialog(self.initial_dialog_id) # Reinicia o fluxo do menu

    async def loop_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        """
        Este passo é executado após um sub-diálogo (como ListaCompra, VerificarPedidoDialog, etc.) terminar.
        Ele garante que o fluxo volte para o início do diálogo 'Inicio' para exibir o menu novamente.
        """
        # Adicione uma pequena mensagem para indicar que o bot está pronto para a próxima interação
        await step_context.context.send_activity("Espero ter ajudado!")

        # Volta ao primeiro passo do diálogo 'Inicio' para exibir as opções novamente.
        # 'replace_dialog' reinicia o diálogo atual e o empilha novamente.
        return await step_context.replace_dialog(self.initial_dialog_id)