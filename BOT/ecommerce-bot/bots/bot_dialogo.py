from botbuilder.core import ActivityHandler, ConversationState, TurnContext, UserState, MessageFactory
from botbuilder.dialogs import Dialog
from helpers.dialog_helper import DialogHelper

class BotDialogo(ActivityHandler):
    def __init__(
        self,
        conversation_state: ConversationState,
        user_state: UserState,
        dialog: Dialog,
    ):
        if conversation_state is None:
            raise TypeError(
                "[BotDialogo]: Missing parameter. conversation_state is required but None was given"
            )
        if dialog is None:
            raise Exception("[BotDialogo]: Missing parameter. dialog is required")

        self.conversation_state = conversation_state
        self.user_state = user_state
        self.dialog = dialog
        
    async def on_turn(self, turn_context: TurnContext):
        await super().on_turn(turn_context)

        # Save any state changes that might have ocurred during the turn.
        await self.conversation_state.save_changes(turn_context)
        await self.user_state.save_changes(turn_context)
        
    async def on_message_activity(self, turn_context: TurnContext):
        
        if turn_context.activity.text and turn_context.activity.text.strip().lower() == "sair":
            await turn_context.send_activity(
                MessageFactory.text("Até logo! Obrigado por usar nosso assistente.")
            )
            # O 'return' impede que a lógica do diálogo continue para este turno
            return
        
        await DialogHelper.run_dialog(
            self.dialog,
            turn_context,
            self.conversation_state.create_property("DialogState"),
        )
        
    async def on_members_added_activity(self, members_added, turn_context: TurnContext):
        for member in members_added:
            if member.id == turn_context.activity.recipient.id:
                await turn_context.send_activity(
                    MessageFactory.text(
                    f"Seja bem-vindo(a) ao bot de atendimento do IBMEC MALL! " 
                    f"Digite uma mensagem para iniciar o atendimento."
                    )
                )