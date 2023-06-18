from data_types import RequirementResp, Requirement
# import uuid
from components.chains import WorkflowChain, ComponentChain, SequenceDiagramChain, ClassDiagramChain


class RequirementHandler:
    def __init__(self):
        pass

    def handle(self, requirement: Requirement) -> RequirementResp:
        session_id = requirement.sessionId
        requirement_content = requirement.content
        components = ComponentChain().run(requirement_content)
        workflow = WorkflowChain().run(
            {'requirement': requirement_content, 'components': components})
        sequence_diagram_code = SequenceDiagramChain().run(workflow).split('```')[1]
        # class_diagram_code = ClassDiagramChain().run(
        #     {'requirement': requirement_content, 'components': components}).split('```')[1]

        resp = {
            "sessionId": session_id,
            "components": components,
            "workflow": workflow,
            "sequenceDiagramCode": sequence_diagram_code,
        }

        return resp
