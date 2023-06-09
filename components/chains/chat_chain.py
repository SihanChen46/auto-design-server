# encoding:utf-8
import tiktoken
from langchain.memory.chat_memory import BaseChatMemory
from typing import List, Dict
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import ConversationChain, LLMChain
from langchain.chains.base import Chain
from components.chains.utils.stream_callback import ThreadedGenerator, StreamingGeneratorCallbackHandler
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from common.utils import get_openai_api_key
from common import log


class ChatChain(Chain):
    token_generator: ThreadedGenerator
    model_class = ChatOpenAI
    chain_class = LLMChain
    model_name = "gpt-3.5-turbo-16k"
    temperature = 0.75
    max_tokens = 16000
    prompt = PromptTemplate(
        input_variables=["new_msg", "history", "requirement",
                         "components", "workflow", "sequence_diagram"],
        template="""
System: As a tech lead, your objective is to communicate with users to understand their requests. The request could be ask you questions about the design, or ask you to improve the design based on their new requirements. 
If User is asking questions to better understand the current design, explain the design to the user. (Like why you choose this design, what are the pros and cons of this design, etc.)
If you are not sure about the requirements, you can ask for clarification from the user. 
If you are confident about users' need, you can make informed judgments to guide decision-making effectively. You don't need to output a new design, but just summarize the changes you want to make to the user.
If User's happy about the conversation, you can tell the user to click the [improve] button to improve the design.
*** Here's your knowledge about the current design, please read it carefully before you start the conversation ***
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

Now, let's start the conversation:
Conversation:
{history}
User: {new_msg}
Tech Lead:
""",
    )

    @property
    def input_keys(self) -> List[str]:
        return ["new_msg", "history", "requirement", "components", "workflow", "sequence_diagram"]

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
            streaming=True, callback_manager=CallbackManager([StreamingGeneratorCallbackHandler(self.token_generator), StreamingStdOutCallbackHandler()]),
            verbose=True
        )

        chain = self.chain_class(prompt=self.prompt, llm=llm,
                                 verbose=False)
        outputs = {"response": chain.run(inputs)}
        self.token_generator.close()
        return outputs
