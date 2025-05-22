from botbuilder.dialogs import ComponentDialog, WaterfallDialog, WaterfallStepContext
from botbuilder.core import MessageFactory
from botbuilder.dialogs.prompts import TextPrompt, PromptOptions


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

    async def product_name_step(self, step_context: WaterfallStepContext) :

        msgPrompt = MessageFactory.text("Informe o nome do produto que você deseja verificar.")

        opcoesPrompt = PromptOptions(
            prompt=msgPrompt,
            retry_prompt=MessageFactory.text("Não consegui entender. Informe o nome do produto novamente."),
        )

        return await step_context.prompt(TextPrompt.__name__, opcoesPrompt)

    async def prompt_process_product_name_step(self, step_context: WaterfallStepContext) :
        nomeProduto = step_context.result

        # Substituir pela API)
        produtos = [
            {"produto": "Camisa", "preco": "R$ 50,00", "estoque": 10},
            {"produto": "Calça", "preco": "R$ 80,00", "estoque": 5},
        ]
        resultado = next((p for p in produtos if p["produto"].lower() == nomeProduto.lower()), None)

        if resultado:
            resposta = (
                f"Produto: {resultado['produto']}\n"
                f"Preço: {resultado['preco']}\n"
                f"Estoque disponível: {resultado['estoque']}"
            )
        else:
            resposta = f"Não encontramos o produto '{nomeProduto}'."

        await step_context.context.send_activity(MessageFactory.text(resposta))
        return await step_context.end_dialog()


