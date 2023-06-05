# encoding:utf-8
from langchain.memory.chat_memory import BaseChatMemory
from typing import List, Dict
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import ConversationChain
from langchain.chains.base import Chain
from common.utils import get_openai_api_key


class ChatChain(Chain):
    conversation_memory: BaseChatMemory

    @property
    def input_keys(self) -> List[str]:
        return ['input']

    @property
    def output_keys(self) -> List[str]:
        return ['response']

    def _call(self, inputs: Dict[str, str]) -> Dict[str, str]:
        converstation_chain = self._build_conversation_chain()
        outputs = {'response': converstation_chain.run(inputs)}
        return outputs

    def _build_conversation_chain(self):
        llm = ChatOpenAI(
            temperature=0,
            openai_api_key=get_openai_api_key(),
            model_name='gpt-3.5-turbo',
            frequency_penalty=0.0,
            presence_penalty=1
        )
        prompt = PromptTemplate(
            input_variables=["input", "history"],
            template='''
***
System: As a tech lead, your objective is to assist users in designing software architectures that align with their requirements. You possess the following skills:
1. In software design, you excel at maintaining simplicity, modularity, and cohesion while reducing coupling. You promote abstraction and encapsulation, ensuring scalability and extensibility.
2. Whenever there is ambiguity in requirements, you proactively seek clarification from customers, ensuring clear understanding and alignment.
3. You confidently rely on your expertise to make informed judgments when necessary, leveraging your knowledge and experience to guide decision-making effectively."
***
{history}
User: {input}
Tech Lead:
'''
        )
        memory = self.conversation_memory
        conversation_chain = ConversationChain(
            prompt=prompt, llm=llm, verbose=True, memory=memory)
        return conversation_chain
