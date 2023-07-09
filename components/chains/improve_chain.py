# encoding:utf-8
import tiktoken
from typing import List, Dict
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains.base import Chain
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from common.utils import get_openai_api_key
from common import log


class ImproveChain(Chain):
    model_class = ChatOpenAI
    chain_class = LLMChain
    model_name = "gpt-3.5-turbo-16k"
    temperature = 0.75
    max_tokens = 16000
    prompt = PromptTemplate(
        input_variables=["history", "requirement",
                         "components", "workflow", "sequence_diagram"],
        template="""
System: As a tech lead, your objective is to improve the current design based on the conversation with user.
Return the new design in the same format as the current design.
*** Here's your knowledge about the current design, please read it carefully before you starts improving it ***
Requirement:
```
{requirement}
```
Components:
```
{components}
```
Workflow:
```
{workflow}
```
Sequence Diagram:
```
{sequence_diagram}
```
*** END ***

*** Here's the conversation history, please read it carefully before you starts improving the design
{history}
***

Now, please improve the deisgn and replace the PLACEHOLDER in the following template:
Requirement:
```
PLACEHOLDER
```
Components:
```
PLACEHOLDER
```
Workflow:
```
PLACEHOLDER
```
Sequence Diagram:
```
PLACEHOLDER
```
You:
""",
    )

    @property
    def input_keys(self) -> List[str]:
        return ["history", "requirement", "components", "workflow", "sequence_diagram"]

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
            streaming=True,
            callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]),
            verbose=True
        )

        chain = self.chain_class(prompt=self.prompt, llm=llm,
                                 verbose=False)
        outputs = {"response": chain.run(inputs)}
        return outputs
