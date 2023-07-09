from data_types import SequenceDiagramReq, SequenceDiagramResp
from components.chains import SequenceDiagramChain
from common import log
from components.session import checkpoint_manager


class SequenceDiagramHandler:
    def __init__(self):
        pass

    def handle(self, req: SequenceDiagramReq) -> SequenceDiagramResp:
        log.info(f"Received SequenceDiagramReq: {req}")
        checkpoint_id = req.checkpointId
        workflow = checkpoint_manager.get_content(checkpoint_id, 'workflow')
        log.info(f"Workflow: {workflow}")
        sequence_diagram_code = SequenceDiagramChain().run(workflow).split('```')[1]
        checkpoint_manager.save_content(
            checkpoint_id, key='sequence_diagram', content=sequence_diagram_code)

        resp = {
            "checkpointId": checkpoint_id,
            "sequenceDiagramCode": sequence_diagram_code,
        }
        log.info(f"Built SequenceDiagramResp: {resp}")

        return resp
