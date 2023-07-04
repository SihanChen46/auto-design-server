import os
import re
from data_types import ImplementReq, ImplementResp
from components.chains import ImplementationChain, DataTypeInterfaceChain, FileStructureChain
from common import log
from components.session import session_manager


class ImplementHandler:
    def __init__(self):
        pass

    def handle(self, req: ImplementReq) -> ImplementResp:
        log.info(f"Received ImplementReq: {req}")
        programming_language = req.programmingLanguage
        session_id = req.sessionId

        components = session_manager.get_content(session_id, 'components')
        sequence_diagram = session_manager.get_content(session_id, 'sequence_diagram')

        outputs = DataTypeInterfaceChain()({
            'components': components,
            'sequence_diagram': sequence_diagram
        })

        designed_data_types, designed_interfaces = outputs['data_types'], outputs['interfaces']

        outputs = FileStructureChain()({
            'designed_data_types': designed_data_types,
            'designed_interfaces': designed_interfaces,
            'programming_language': programming_language
        })
        designed_file_structure = outputs['file_structure']
        outputs = ImplementationChain()({
            'designed_data_types': designed_data_types,
            'designed_interfaces': designed_interfaces,
            'designed_file_structure': designed_file_structure,
            'programming_language': programming_language
        })
        implementation = outputs['implementation']

        implementation_file_dict = self.parse_implementation(implementation)
        log.info(f"implementation_file_dict: {implementation_file_dict}")
        self.implementation_to_files(
            session_id, implementation_file_dict)  # save to cloud?

        resp = {
            "sessionId": session_id,
            "status": "success",
        }
        log.info(f"Returned ImplementResp: {resp}")

        return resp

    @staticmethod
    def parse_implementation(implementation):
        # Get all ``` blocks and preceding filenames
        regex = r"(\S+)\n\s*```[^\n]*\n(.+?)```"
        matches = re.finditer(regex, implementation, re.DOTALL)

        file_dict = {}
        for match in matches:
            # Strip the filename of any non-allowed characters and convert / to \
            path = re.sub(r'[<>"|?*]', "", match.group(1))

            # Remove leading and trailing brackets
            path = re.sub(r"^\[(.*)\]$", r"\1", path)

            # Remove leading and trailing backticks
            path = re.sub(r"^`(.*)`$", r"\1", path)

            # Remove trailing ]
            path = re.sub(r"\]$", "", path)

            # Get the code
            code = match.group(2)

            # Add the file to the list
            file_dict[path] = code

        # Return the files
        return file_dict

    @staticmethod
    def implementation_to_files(session_id, file_dict):
        for file_path, file_code in file_dict.items():
            file_path = os.path.join('generated_projects', session_id, file_path)

            # Get the directory path
            directory = os.path.dirname(file_path)

            # Create the directory if it doesn't exist
            if not os.path.exists(directory):
                os.makedirs(directory)

            # Write the file
            with open(file_path, 'w') as file:
                file.write(file_code)
