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

        #Prompt para escolha das opções
        self.add_dialog(ChoicePrompt(ChoicePrompt.__name__))
        self.add_dialog(ConfirmPrompt(ConfirmPrompt.__name__))

        #Area de atendimento de Verificar Pedidos  
        self.add_dialog(VerificarPedidoDialog())

        #Area de atendimento de Verificar Produtos
        self.add_dialog(VerificarProdutoDialog())
        
        #Area de atendimento de Lista da compra
        self.add_dialog(ListaCompra())
        
        self.add_dialog(ComprarProdutoDialog())

        # Prompt para escolha de opções
        # Tratamento das opções de escolha do usuário
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
        return await step_context.prompt(
            ChoicePrompt.__name__,
            PromptOptions(
                prompt=MessageFactory.text("Escolha a opção desejada:"),
                choices=[Choice("Verificar Pedidos"), Choice("Verificar Produtos"), Choice("Extrato da compra"), Choice("Comprar Produto")],
            ),
        )

    async def process_option_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        
        choice = step_context.result.value
        
        if choice == "Verificar Pedidos":
            return await step_context.begin_dialog("VerificarPedidoDialog")
        elif choice == "Verificar Produtos":
            return await step_context.begin_dialog("VerificarProdutoDialog")
        elif choice == "Extrato da compra":
            return await step_context.begin_dialog("ListaCompra")
        elif choice == "Comprar Produto":
            return await step_context.begin_dialog("ComprarProdutoDialog")
        
        return await step_context.next(None)
    
    
    async def loop_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        """
        Este passo é executado após um sub-diálogo terminar.
        Ele reinicia o diálogo principal para mostrar o menu de opções novamente.
        """
        return await step_context.replace_dialog(self.initial_dialog_id)
    

    async def show_card_produto(self ,turn_context):

        produto_api = ProductAPI()

        response = produto_api.consultar_api()
        print(response)

        #Chamada de API para obter os produtos
        card = CardFactory.hero_card(
            HeroCard(
                title=response["productName"],
                text=f"Preço: R$ {response['price']}",
                subtitle=response["productDescription"],
                images=[CardImage(url=response["imageUrl"][0])],
                buttons=[
                    CardAction(
                        type=ActionTypes.im_back,
                        title="Comprar Produto",
                        value=response["id"],
                    ),
                ],
            )
        )
        await turn_context.send_activity(MessageFactory.attachment(card))

        
        