import threading
from components.session import session_manager


class SessionSaverThread(threading.Thread):
    def __init__(self, session_id, key, future):
        super().__init__()
        self.session_id = session_id
        self.future = future
        self.key = key

    def run(self):
        result = self.future.result()  # This will block until the future is done.
        session_manager.save_content(self.session_id, key=self.key, content=result)
