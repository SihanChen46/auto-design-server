from typing import List, Dict
from data_types import MessageReq, MessageResp, Message, CreatorRole
import uuid
from components.chains import ChatChain
from components.session import checkpoint_manager
from datetime import datetime
from fastapi.responses import StreamingResponse
from langchain.memory import ConversationBufferMemory
from components.chains.utils.stream_callback import ThreadedGenerator
from components.handlers.checkpoint_saver_thread import CheckpointMsgSaverThread
from concurrent.futures import ThreadPoolExecutor
from common import log


class MessageHandler:
    def __init__(self):
        self.executor = ThreadPoolExecutor(max_workers=2)

    def handle(self, req: MessageReq) -> MessageResp:
        checkpoint_id = req.checkpointId
        req_content = req.content

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

        token_generator = ThreadedGenerator()
        resp_content_future = self.executor.submit(
            ChatChain(token_generator=token_generator).run,
            history=history,
            new_msg=req_content,
            requirement=requirement,
            components=components,
            workflow=workflow,
            sequence_diagram=sequence_diagram
        )
        saver = CheckpointMsgSaverThread(
            checkpoint_id, req_content, resp_content_future)
        saver.start()

        return StreamingResponse(token_generator, media_type='text/event-stream')

    def build_conversation_memory(self, msg_list: List[Dict]):
        memory = ConversationBufferMemory(ai_prefix='Tech Lead', human_prefix='User')
        for msg in msg_list:
            if msg['creatorRole'] == CreatorRole.User:
                memory.chat_memory.add_user_message(msg['content'])
            elif msg['creatorRole'] == CreatorRole.Assistant:
                memory.chat_memory.add_ai_message(msg['content'])
        return memory
