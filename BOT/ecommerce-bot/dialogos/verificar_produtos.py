from botbuilder.dialogs import ComponentDialog, WaterfallDialog, WaterfallStepContext
from botbuilder.core import MessageFactory
from botbuilder.dialogs.prompts import TextPrompt, PromptOptions

from api.rotas import ProductAPI

class VerificarProdutoDialog(ComponentDialog):
    def __init__(self):
        super(VerificarProdutoDialog, self).__init__("VerificarProdutoDialog")

        self.add_dialog(TextPrompt(TextPrompt.__name__))

        self.add_dialog(
            WaterfallDialog(
                "verificarProdutoWaterfallDialog",
                [
                    self.product_name_step,
                    self.prompt_process_product_name_step,
                ],
            )
        )

        self.initial_dialog_id = "verificarProdutoWaterfallDialog"
        self.product_api = ProductAPI()

    async def product_name_step(self, step_context: WaterfallStepContext):
        msgPrompt = MessageFactory.text("Informe o nome do produto que você deseja consultar")

        opcoesPrompt = PromptOptions(
            prompt=msgPrompt,
            retry_prompt=MessageFactory.text("Não consegui entender. Informe o nome do produto novamente."),
        )

        return await step_context.prompt(TextPrompt.__name__, opcoesPrompt)

    async def prompt_process_product_name_step(self, step_context: WaterfallStepContext):
        nomeProduto = step_context.result

        produtos_encontrados = self.product_api.verificar_produtos(nomeProduto)

        if produtos_encontrados:
            resposta_detalhada = f"Encontrei os seguintes produtos que contêm '{nomeProduto}':\n\n"

            for produto in produtos_encontrados:
                resposta_detalhada += (
                    f"**Nome:** {produto.get('nome', 'N/A')}\n\n"
                    f"**Categoria:** {produto.get('categoria', 'N/A')}\n\n"
                    f"**Descrição:** {produto.get('descricao', 'N/A')}\n\n"
                    f"**Preço:** R$ {produto.get('preco', 0.0):.2f}\n\n"
                    f"**Estoque:** {produto.get('estoque', 0)}\n\n"
                    f"----------\n"
                )

            resposta = resposta_detalhada.rstrip("----------\n")
        else:
            resposta = f"Não encontramos nenhum produto que contenha '{nomeProduto}'."

        await step_context.context.send_activity(MessageFactory.text(resposta))
        return await step_context.end_dialog()