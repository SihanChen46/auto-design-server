from data_types import ComponentReq
from components.chains import ComponentChain
from common import log
from fastapi.responses import StreamingResponse
from components.chains.utils.stream_callback import ThreadedGenerator
from concurrent.futures import ThreadPoolExecutor
from components.handlers.checkpoint_saver_thread import CheckpointContentSaverThread
from components.session import checkpoint_manager


class ComponentHandler:
    def __init__(self):
        self.executor = ThreadPoolExecutor(max_workers=2)

    def handle(self, req: ComponentReq) -> StreamingResponse:
        log.info(f"Received ComponentReq: {req}")
        checkpoint_manager.remove_checkpoint(req.checkpointId)
        checkpoint_id = req.checkpointId
        requirement = req.requirement
        checkpoint_manager.save_content(
            checkpoint_id,
            'requirement',
            requirement
        )
        token_generator = ThreadedGenerator()
        future = self.executor.submit(ComponentChain(
            token_generator=token_generator).run, input=requirement)
        saver = CheckpointContentSaverThread(checkpoint_id, 'components', future)
        saver.start()

        # threading.Thread(target=ComponentChain(
        #     token_generator=token_generator).run, kwargs={'input': requirement}).start()

        return StreamingResponse(token_generator, media_type='text/event-stream')
