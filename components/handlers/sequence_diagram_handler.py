from data_types import SequenceDiagramReq, SequenceDiagramResp
from components.chains import WorkflowChain, SequenceDiagramChain
from common import log
from components.session import session_manager


class SequenceDiagramHandler:
    def __init__(self):
        pass

    def handle(self, req: SequenceDiagramReq) -> SequenceDiagramResp:
        log.info(f"Received SequenceDiagramReq: {req}")
        session_id = req.sessionId
        workflow = session_manager.get_content(session_id, 'workflow')
        log.info(f"Workflow: {workflow}")
        sequence_diagram_code = SequenceDiagramChain().run(workflow).split('```')[1]
        session_manager.save_content(
            session_id, key='sequence_diagram', content=sequence_diagram_code)

        resp = {
            "sessionId": session_id,
            "sequenceDiagramCode": sequence_diagram_code,
        }
        log.info(f"Built SequenceDiagramResp: {resp}")

        return resp
