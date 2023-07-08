from typing import List, Dict
from data_types import ImproveReq, ImproveResp, Message, CreatorRole
from components.chains import ImproveChain
from components.session import checkpoint_manager
from langchain.memory import ConversationBufferMemory
from common import log


class ImproveHandler:
    def __init__(self):
        pass

    def handle(self, req: ImproveReq) -> ImproveResp:
        checkpoint_id = req.checkpointId

        msg_list = checkpoint_manager.get_msg_list(
            checkpoint_id
        )
        history = self.build_conversation_memory(
            msg_list).load_memory_variables({})['history']
        requirement = checkpoint_manager.get_content(checkpoint_id, 'requirement')
        components = checkpoint_manager.get_content(checkpoint_id, 'components')
        workflow = checkpoint_manager.get_content(checkpoint_id, 'workflow')
        sequence_diagram = checkpoint_manager.get_content(
            checkpoint_id, 'sequence_diagram'
        )
        log.info(f'[ImproveHandler] history: {history}')

        improve_chain = ImproveChain()
        improved_design = improve_chain({
            'history': history,
            'requirement': requirement,
            'components': components,
            'workflow': workflow,
            'sequence_diagram': sequence_diagram,
        })['response']

        requirement, components, workflow, sequence_diagram = self.parse_design(
            improved_design)
        # checkpoint_manager.save_content(checkpoint_id, 'requirement', requirement)
        # checkpoint_manager.save_content(checkpoint_id, 'components', components)
        # checkpoint_manager.save_content(checkpoint_id, 'workflow', workflow)
        # checkpoint_manager.save_content(
        #     checkpoint_id, 'sequence_diagram', sequence_diagram)

        resp = {
            "checkpointId": checkpoint_id,
            'requirement': requirement,
            'components': components,
            'workflow': workflow,
            'sequenceDiagramCode': sequence_diagram,
        }
        return resp

    def build_conversation_memory(self, msg_list: List[Dict]):
        memory = ConversationBufferMemory(ai_prefix='Tech Lead', human_prefix='User')
        for msg in msg_list:
            if msg['creatorRole'] == CreatorRole.User:
                memory.chat_memory.add_user_message(msg['content'])
            elif msg['creatorRole'] == CreatorRole.Assistant:
                memory.chat_memory.add_ai_message(msg['content'])
        return memory

    def parse_design(self, design: str):
        requirement = design.split('```')[1]
        components = design.split('```')[3]
        workflow = design.split('```')[5]
        sequence_diagram = design.split('```')[7]
        return requirement, components, workflow, sequence_diagram
