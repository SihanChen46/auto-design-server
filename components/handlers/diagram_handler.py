from data_types import Diagram, DiagramClick, MessageStatus
import uuid
from components.chains import SummaryChain, DesignChain, DiagramChain


class DiagramHandler:
    def __init__(self, session_manager):
        self.session_manager = session_manager

    def handle(self, diagram_click: DiagramClick) -> Diagram:
        conversation_id = diagram_click.conversationId
        conversation_memory = self.session_manager.get_conversation_memory(
            conversation_id
        )

        chat_history = str(conversation_memory.chat_memory.messages)

        chat_summary = SummaryChain().run(chat_history)
        design_content = DesignChain().run(chat_summary)
        diagram_code = DiagramChain().run(design_content)

        resp_diagram = {
            "diagramId": str(uuid.uuid4()),
            "conversationId": conversation_id,
            "diagramCode": diagram_code,
            "status": MessageStatus.DONE,
        }

        return resp_diagram
