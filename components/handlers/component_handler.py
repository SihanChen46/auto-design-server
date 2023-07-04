from data_types import ComponentReq
from components.chains import ComponentChain
from common import log
from fastapi.responses import StreamingResponse
from components.chains.utils.stream_callback import ThreadedGenerator
from concurrent.futures import ThreadPoolExecutor
from components.handlers.session_saver_thread import SessionSaverThread
from components.session import session_manager


class ComponentHandler:
    def __init__(self):
        self.executor = ThreadPoolExecutor(max_workers=2)

    def handle(self, req: ComponentReq) -> StreamingResponse:
        log.info(f"Received ComponentReq: {req}")
        session_id = req.sessionId
        requirement = req.requirement
        session_manager.save_content(
            session_id,
            'requirement',
            requirement
        )
        token_generator = ThreadedGenerator()
        future = self.executor.submit(ComponentChain(
            token_generator=token_generator).run, input=requirement)
        saver = SessionSaverThread(session_id, 'components', future)
        saver.start()

        # threading.Thread(target=ComponentChain(
        #     token_generator=token_generator).run, kwargs={'input': requirement}).start()

        return StreamingResponse(token_generator, media_type='text/event-stream')
