from data_types import Message, CreatorRole
import uuid
from components.chains import ChatChain
from components.session import SessionManager


class MessageHandler:
    def __init__(self):
        self.session_manager = SessionManager()

    def handle(self, req_message: Message) -> Message:
        message_content = req_message.content
        conversation_id = req_message.conversationId
        conversation_memory = self.session_manager.get_conversation_memory(
            conversation_id
        )

        chat_chain = ChatChain(conversation_memory=conversation_memory)
        resp_content = chat_chain.run(message_content)

        resp_message = {
            "msgId": str(uuid.uuid4()),
            "conversationId": req_message.conversationId,
            "creatorRole": CreatorRole.Assistant,
            "content": resp_content,
            "status": "DONE",
        }

        return resp_message
