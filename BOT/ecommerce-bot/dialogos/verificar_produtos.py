from botbuilder.dialogs import ComponentDialog, WaterfallDialog, WaterfallStepContext
from botbuilder.core import MessageFactory
from botbuilder.dialogs.prompts import TextPrompt, PromptOptions
from botbuilder.schema import TextFormatTypes, ActivityTypes

from api.rotas import ProdutosAPI

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
        self.product_api = ProdutosAPI()

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
            primeiro_produto = produtos_encontrados[0]

            resposta = (
                f"**Nome:** {primeiro_produto.get('nome', 'N/A')}\n"
                f"**Categoria:** {primeiro_produto.get('categoria', 'N/A')}\n"
                f"**Descrição:** {primeiro_produto.get('descricao', 'N/A')}\n"
                f"**Preço:** R$ {primeiro_produto.get('preco', 0.0):.2f}\n"
                f"**Estoque:** {primeiro_produto.get('estoque', 0)}"
            )
        else:
            resposta = f"Não encontramos o produto '{nomeProduto}'."

        # testando resposta no markdown
        activity = MessageFactory.text(resposta)
        activity.text_format = TextFormat.Markdown
        activity.value_type = ActivityTypes.Message

        await step_context.context.send_activity(activity)
        return await step_context.end_dialog()