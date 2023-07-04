from common import log
from typing import Dict, List


class SessionManager(object):

    """
    Manage the all middle results for each session. Store everything in string
    """

    def __init__(self):
        log.debug("[SessionManager] initialied")
        self.dict = {}

    def get_content(self, session_id, key) -> str:
        session = self.get_session(session_id)

        if key not in session:
            content = ''
        else:
            content = session[key]
        log.info(
            f'[SessionManager] get_content: session_id: {session_id}, key: {key}, content: {content}')
        return content

    def save_content(self, session_id, key, content) -> None:
        log.info(
            f'[SessionManager] save_content: session_id: {session_id}, key: {key}, content: {content}')
        session = self.get_session(session_id)
        session[key] = content

    def get_session(self, session_id) -> Dict:
        if session_id not in self.dict:
            session = {}
            self.dict[session_id] = session
        session = self.dict.get(session_id)
        return session

    def clear_session(self, session_id):
        self.dict.pop(session_id, None)
