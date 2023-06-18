# encoding:utf-8
from typing import List, Dict
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains.base import Chain
from common.utils import get_openai_api_key


class DiagramChain(Chain):
    @property
    def input_keys(self) -> List[str]:
        return ["input"]

    @property
    def output_keys(self) -> List[str]:
        return ["response"]

    def _call(self, inputs: Dict[str, str]) -> Dict[str, str]:
        chain = self._build_chain()
        outputs = {"response": chain.run(inputs)}
        return outputs

    def _build_chain(self):
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
System: Given this design, generate a Mermaid.JS code that draws a flowchat TD representing the relationship of each component, use node to represent component and edge to represent connections between components, put name of data on links as well

Remember: 
1. Don't put spaces in the node labels but assign them unique identifiers
2. Don't put special characters in naming
3. Make sure there is no missing connections between some components.
***

Example:
Input:
{{
    'Conversation Manager Component': {{
        'upstream': {{
            'User Interface Component': {{
                data: 'User input (text)'
            }},
        }},
        'downstream: {{
            'Natural Language Understanding (NLU) Component': {{
                data: ['Processed user input (text)', 'context information']
            }},
        }}
    }},
}}
Output:
flowchart TD
    A[User Interface Component] -->|User input| B[User Management Component]
    B -->|Processed user input| C[Natural Language Understanding Component]
    B -->|context information| C

Now
Input:
{input}
Output:
""",
        )
        chain = LLMChain(prompt=prompt, llm=llm, verbose=True)
        return chain
