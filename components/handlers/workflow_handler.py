from data_types import WorkflowReq
from components.chains import WorkflowChain
from common import log
from fastapi.responses import StreamingResponse
from components.chains.utils.stream_callback import ThreadedGenerator
import threading


class WorkflowHandler:
    def __init__(self):
        pass

    def handle(self, req: WorkflowReq) -> StreamingResponse:
        log.info(f"Received WorkflowReq: {req}")
        session_id = req.sessionId
        requirement = req.requirement
        components = req.components
        token_generator = ThreadedGenerator()
        threading.Thread(target=WorkflowChain(
            token_generator=token_generator).run, kwargs={'requirement': requirement, 'components': components}).start()

        return StreamingResponse(token_generator, media_type='text/event-stream')
