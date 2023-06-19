from data_types import ComponentReq
from components.chains import ComponentChain
from common import log
from fastapi.responses import StreamingResponse
from components.chains.utils.stream_callback import ThreadedGenerator
import threading


class ComponentHandler:
    def __init__(self):
        pass

    def handle(self, req: ComponentReq) -> StreamingResponse:
        log.info(f"Received ComponentReq: {req}")
        session_id = req.sessionId
        requirement = req.requirement
        token_generator = ThreadedGenerator()
        threading.Thread(target=ComponentChain(
            token_generator=token_generator).run, kwargs={'input': requirement}).start()

        return StreamingResponse(token_generator, media_type='text/event-stream')
