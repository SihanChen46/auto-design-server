# encoding:utf-8
from typing import List, Dict
import tiktoken
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains.base import Chain
from common.utils import get_openai_api_key
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler


class SequenceDiagramChain(Chain):
    model_class = ChatOpenAI
    chain_class = LLMChain
    model_name = "gpt-3.5-turbo-16k"
    temperature = 0.75
    max_tokens = 16000
    prompt = PromptTemplate(
        input_variables=["input"],
        template="""
system: you are a tech lead who's good at demonstated workflow between components usinig mermaid.JS, your goal is the help user to write mermaid.JS code that draws the sequenceDiagram that covers every single details. Only return the mermaid.JS code. Make sure no syntax error in the mermaid code.

This is an example
User: Write a mermaid.JS code that draws a detailed sequenceDiagram for a NLU component for chatbot?
You:
```
sequenceDiagram
    participant User
    participant Chatbot
    participant NLU

    User->>Chatbot: Send message
    Chatbot->>NLU: Process message
    Note over NLU: Extract intent and entities

    alt Intent recognized
        NLU-->>Chatbot: Intent: <intent>
        Note over NLU: Extracted entities: <entities>
    else No intent recognized
        NLU-->>Chatbot: No intent recognized
    end

    Chatbot->>User: Reply with intent and entities
```
This is another example
User: Write a mermaid.JS code that draws a detailed sequenceDiagram for a payment component for amazon?
You:
```
sequenceDiagram
    participant C as Customer
    participant F as Frontend
    participant P as PaymentService
    participant A as AmazonAPI

    C->>F: Choose product
    F->>C: Display product details
    C->>F: Add to cart
    F->>C: Display cart details
    C->>F: Proceed to checkout
    F->>C: Display checkout form
    C->>F: Enter payment information
    F->>P: Send payment information
    P->>A: Request to process payment
    alt Payment Successful
        A->>P: Confirm payment
        P->>F: Confirm payment
        F->>C: Confirm order and payment
    else Payment Unsuccessful
        A->>P: Reject payment
        P->>F: Reject payment
        F->>C: Payment unsuccessful, request to re-enter information
    end
```
Now
User:
{input}
Write a mermaid.JS code that draws a extensively detailed sequenceDiagram for the described workflow?
You:
""",
    )

    @property
    def input_keys(self) -> List[str]:
        return ["input"]

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
            callbacks=[StreamingStdOutCallbackHandler()]
        )

        chain = self.chain_class(prompt=self.prompt, llm=llm, verbose=True)
        # TODO: splitting
        outputs = {"response": chain.run(inputs)}
        return outputs
