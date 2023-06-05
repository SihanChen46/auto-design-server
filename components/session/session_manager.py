from langchain.memory import ConversationBufferMemory
from common import log


class SessionManager(object):

    '''
    Manage the conversationmemory for each conversation window in cache

    {
        conversation_id: {
            conversation_memory: Langchain Memory Object,
        }
    }

    '''

    def __init__(self):
        log.debug("[SessionManager] initialied")
        self.dict = {}

    def get_conversation_memory(self, conversation_id):
        session = self.get_session(conversation_id)

        if not session['conversation_memory']:
            memory = ConversationBufferMemory(
                ai_prefix='Tech Lead', human_prefix='User')
            session['conversation_memory'] = memory

        return session['conversation_memory']

    def get_session(self, conversation_id):
        if conversation_id not in self.dict:
            session = {}
            session['conversation_memory'] = None
            self.dict[conversation_id] = session
        session = self.dict.get(conversation_id)
        return session

    def clear_session(self, conversation_id):
        self.dict.pop(conversation_id, None)
