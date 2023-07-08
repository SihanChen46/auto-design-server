from data_types import ImplementReq, ImplementResp
from components.chains import WorkflowChain
from common import log
from components.session import checkpoint_manager


class ImplementationHandler:
    def __init__(self):
        pass

    def handle(self, req: ImplementReq) -> ImplementResp:
        log.info(f"Received ClassDiagramReq: {req}")
        session_id = req.sessionId

        components = checkpoint_manager.get_components(session_id)
        workflow = checkpoint_manager.get_workflow(session_id)
        sequence_diagram = checkpoint_manager.get_sequence_diagram(session_id)

        data_types, interfaces = DataTypesInterfaceChain().run(components, sequence_diagram)
        class_diagram = ClassDiagramChain().run(data_types, interfaces)

        resp = {
            "sessionId": session_id,
        }
        log.info(f"Returned ClassDiagramResp: {resp}")

        return resp
