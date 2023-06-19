from data_types import SequenceDiagramReq, SequenceDiagramResp
from components.chains import WorkflowChain, SequenceDiagramChain
from common import log


class SequenceDiagramHandler:
    def __init__(self):
        pass

    def handle(self, req: SequenceDiagramReq) -> SequenceDiagramResp:
        log.info(f"Received SequenceDiagramReq: {req}")
        session_id = req.sessionId
        workflow = req.workflow
        sequence_diagram_code = SequenceDiagramChain().run(workflow).split('```')[1]

        resp = {
            "sessionId": session_id,
            "sequenceDiagramCode": sequence_diagram_code,
        }
        log.info(f"Built SequenceDiagramResp: {resp}")

        return resp
