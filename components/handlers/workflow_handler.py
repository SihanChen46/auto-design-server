from data_types import WorkflowReq
from components.chains import WorkflowChain
from common import log
from fastapi.responses import StreamingResponse
from components.chains.utils.stream_callback import ThreadedGenerator
from concurrent.futures import ThreadPoolExecutor
from components.handlers.checkpoint_saver_thread import CheckpointContentSaverThread
from components.session import checkpoint_manager


class WorkflowHandler:
    def __init__(self):
        self.executor = ThreadPoolExecutor(max_workers=2)

    def handle(self, req: WorkflowReq) -> StreamingResponse:
        log.info(f"Received WorkflowReq: {req}")
        checkpoint_id = req.checkpointId
        requirement = checkpoint_manager.get_content(checkpoint_id, 'requirement')
        components = checkpoint_manager.get_content(checkpoint_id, 'components')
        token_generator = ThreadedGenerator()
        future = self.executor.submit(WorkflowChain(
            token_generator=token_generator).run, requirement=requirement, components=components)
        saver = CheckpointContentSaverThread(checkpoint_id, 'workflow', future)
        saver.start()

        # threading.Thread(target=WorkflowChain(
        #     token_generator=token_generator).run, kwargs={'requirement': requirement, 'components': components}).start()

        return StreamingResponse(token_generator, media_type='text/event-stream')
