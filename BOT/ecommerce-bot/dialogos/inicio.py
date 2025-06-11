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

        self.add_dialog(ChoicePrompt(ChoicePrompt.__name__))
        self.add_dialog(ConfirmPrompt(ConfirmPrompt.__name__))

        self.add_dialog(VerificarPedidoDialog())
        self.add_dialog(VerificarProdutoDialog())
        self.add_dialog(ListaCompra())
        self.add_dialog(ComprarProdutoDialog())

        self.add_dialog(
            WaterfallDialog(
                "inicio",
                [
                    self.prompt_option_step,
                    self.process_option_step,
                    self.loop_step,
                ],
            )
        )

        self.initial_dialog_id = "inicio"

    async def prompt_option_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        if step_context.context.activity.text is None:
             await step_context.context.send_activity("Olá! Sou seu assistente de compras. O que você gostaria de fazer hoje?")

        return await step_context.prompt(
            ChoicePrompt.__name__,
            PromptOptions(
                prompt=MessageFactory.text("Escolha a opção desejada:"),
                choices=[
                    Choice("Consultar Pedidos"),
                    Choice("Consultar Produtos"),
                    Choice("Extrato de compras"),
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
        else:
            await step_context.context.send_activity("Não entendi a opção. Por favor, escolha uma das opções válidas.")
            return await step_context.replace_dialog(self.initial_dialog_id)

    async def loop_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

        await step_context.context.send_activity("Voltando ao menu principal...")
        return await step_context.replace_dialog(self.initial_dialog_id)