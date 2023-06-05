# encoding:utf-8
from langchain.memory.chat_memory import BaseChatMemory
from typing import List, Dict
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains.base import Chain
from common.utils import get_openai_api_key


class DesignChain(Chain):

    @property
    def input_keys(self) -> List[str]:
        return ['input']

    @property
    def output_keys(self) -> List[str]:
        return ['response']

    def _call(self, inputs: Dict[str, str]) -> Dict[str, str]:
        chain = self._build_conversation_chain()
        outputs = {'response': chain.run(inputs)}
        return outputs

    def _build_conversation_chain(self):
        llm = ChatOpenAI(
            temperature=0,
            openai_api_key=get_openai_api_key(),
            model_name='gpt-3.5-turbo',
            max_tokens=2000)
        prompt = PromptTemplate(
            input_variables=["input"],
            template='''
***
System:
As a tech lead, your expertise lies in ensuring simplicity, modularity, and cohesion, while minimizing coupling between components.
Now your goal is to support users in designing software components.
For each component that has a upstream/downstream component, there should be a data field defined indicating the data passed between them.
Keep in mind the following guidelines:
1. Use concise and informative naming, avoiding the use of special characters.
2. Ensure that the components encompass all the necessary features as per the requirements.
***
Example:
Input:
Overall mission of the app is understand the user's input using NLP algorithm
Here are some specific features:

1. the app will need to process different user's request independently
2. the app will have a UI for user to input text
3. the app will need to understand user's message using NLP techniques.
Output:
{{
    'Conversation Manager Component': {{
        'upstream': {{
            'User Interface Component': {{
                data: 'User input text'
            }},
        }},
        'downstream: {{
            'Natural Language Understanding Component': {{
                data: ['Processed user input text', 'context information']
            }},
        }}
    }},
}}

Now
Input: 
{input}
Output:
'''
        )
        chain = LLMChain(
            prompt=prompt, llm=llm, verbose=True)
        return chain
