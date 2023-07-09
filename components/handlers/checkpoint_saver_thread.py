import threading
from data_types import MessageReq, MessageResp, Message, CreatorRole
from components.session import checkpoint_manager
import uuid
from datetime import datetime


class CheckpointContentSaverThread(threading.Thread):
    def __init__(self, checkpoint_id, key, future):
        super().__init__()
        self.checkpoint_id = checkpoint_id
        self.future = future
        self.key = key

    def run(self):
        result = self.future.result()  # This will block until the future is done.
        checkpoint_manager.save_content(
            self.checkpoint_id, key=self.key, content=result)


class CheckpointMsgSaverThread(threading.Thread):
    def __init__(self, checkpoint_id, req_content, resp_content_future):
        super().__init__()
        self.checkpoint_id = checkpoint_id
        self.req_content = req_content
        self.resp_content_future = resp_content_future

    def run(self):
        # This will block until the future is done.
        resp_content = self.resp_content_future.result()
        req_msg = {
            'msgId': str(uuid.uuid4()),
            'creatorRole': CreatorRole.User,
            'content': self.req_content,
            'createTimestamp': int(datetime.utcnow().timestamp()),
        }
        resp_msg = {
            'msgId': str(uuid.uuid4()),
            'creatorRole': CreatorRole.Assistant,
            'content': resp_content,
            'createTimestamp': int(datetime.utcnow().timestamp()),
        }
        checkpoint_manager.add_msg(self.checkpoint_id, req_msg)
        checkpoint_manager.add_msg(self.checkpoint_id, resp_msg)
