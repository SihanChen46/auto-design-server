# encoding:utf-8
from typing import List, Dict
import tiktoken
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains.base import Chain
from common.utils import get_openai_api_key
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler


class WorkflowChain(Chain):
    model_class = ChatOpenAI
    chain_class = LLMChain
    model_name = "gpt-3.5-turbo-16k"
    temperature = 0.75
    max_tokens = 16000
    prompt = PromptTemplate(
        input_variables=["requirement", "components"],
        template="""
***
system: you are a tech lead who's good at designing softwares, your goal is the help user to define how data flows between all designed compnents.
***
requirement:
{requirement}

design:
{components}
User: Can you give me an detailed example of how data flows between in all components?
You:
""",
    )

    @property
    def input_keys(self) -> List[str]:
        return ["requirement", "components"]

    @property
    def output_keys(self) -> List[str]:
        return ["response"]

    def _call(self, inputs: Dict[str, str]) -> Dict[str, str]:
        encoding = tiktoken.encoding_for_model(self.model_name)
        prompted_input = self.prompt.format(**inputs)
        num_tokens = len(encoding.encode(prompted_input))

        llm = self.model_class(
            temperature=self.temperature,
            openai_api_key=get_openai_api_key(),
            model_name=self.model_name,
            max_tokens=self.max_tokens - num_tokens,
            streaming=True, callbacks=[StreamingStdOutCallbackHandler()]
        )

        chain = self.chain_class(prompt=self.prompt, llm=llm, verbose=True)
        # TODO: splitting
        outputs = {"response": chain.run(inputs)}
        return outputs
