# encoding:utf-8
from typing import List, Dict
from langchain.llms import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains.base import Chain
from common.utils import get_openai_api_key


class SummaryChain(Chain):
    @property
    def input_keys(self) -> List[str]:
        return ["input"]

    @property
    def output_keys(self) -> List[str]:
        return ["response"]

    def _call(self, inputs: Dict[str, str]) -> Dict[str, str]:
        chain = self._build_conversation_chain()
        outputs = {"response": chain.run(inputs)}
        return outputs

    def _build_conversation_chain(self):
        llm = ChatOpenAI(
            temperature=0,
            openai_api_key=get_openai_api_key(),
            model_name="gpt-3.5-turbo",
            max_tokens=2000,
        )
        prompt = PromptTemplate(
            input_variables=["input"],
            template="""
***
System: As a tech lead, your objective is to assist users in designing software architectures that align with their requirements. You excel at maintaining simplicity, modularity, and cohesion while reducing coupling. You promote abstraction and encapsulation, ensuring scalability and extensibility.
***
Now, analyze the following chat history, Come up with a the final design:

----------
{input}
----------

design:
""",
        )
        chain = LLMChain(prompt=prompt, llm=llm, verbose=True)
        return chain
