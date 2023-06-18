# encoding:utf-8
from typing import List, Dict
import tiktoken
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains.base import Chain
from common.utils import get_openai_api_key


class ClassDiagramChain(Chain):
    model_class = ChatOpenAI
    chain_class = LLMChain
    model_name = "gpt-3.5-turbo"
    temperature = 0
    max_tokens = 4000
    prompt = PromptTemplate(
        input_variables=["requirement", "components"],
        template="""
***
system: you are a tech lead who's good at mermaid.JS, your goal is the help user to write mermaid.JS code that draws the diagram of their requirement
For example:
User: Can you give me a mermaid.JS code that draws a detailed classDiagram for a vehicle system?
You:
```
classDiagram
    class Vehicle {{
        -int id
        -string brand
        -string model
        -int year
        +void startEngine()
        +void stopEngine()
        +void accelerate(float speed)
    }}

    class Car {{
        -int numDoors
        -string bodyType
        +void openDoor(int doorNumber)
        +void closeDoor(int doorNumber)
    }}

    class Motorcycle {{
        -boolean hasSideCar
        +void tilt(float angle)
    }}

    Vehicle <|-- Car
    Vehicle <|-- Motorcycle
```
***
Now
User:
Requirement:
{requirement}

design:
{components}

Can you give me a mermaid.JS code that draws a extensively detailed classDiagram for the components and their functionalities in the design?
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
        )

        chain = self.chain_class(prompt=self.prompt, llm=llm, verbose=True)
        # TODO: splitting
        outputs = {"response": chain.run(inputs)}
        return outputs
