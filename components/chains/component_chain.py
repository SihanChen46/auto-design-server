# encoding:utf-8
from typing import List, Dict
import tiktoken
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains.base import Chain
from common.utils import get_openai_api_key
from components.chains.utils.stream_callback import ThreadedGenerator, StreamingGeneratorCallbackHandler
from langchain.callbacks.manager import CallbackManager


class ComponentChain(Chain):
    token_generator: ThreadedGenerator
    model_class = ChatOpenAI
    chain_class = LLMChain
    model_name = "gpt-3.5-turbo-0613"
    temperature = 0.75
    max_tokens = 4000
    prompt = PromptTemplate(
        input_variables=["input"],
        template="""
system: you are a tech lead who's good at designing softwares, your goal is the help user to define the components in their software. Only return the components
This is an example
User: Give me a list of components for the design of a e-commerce platform and their core functionality.
You:
User Interface: Provides an easy-to-navigate and visually pleasing interface where users can interact with the different functionalities of the e-commerce platform. 
Product Catalog: Manages and displays product information and inventory for users to browse and purchase.
Shopping Cart: Enables users to add, remove, and manage products before proceeding to checkout.
Order Management: Handles the processing, tracking, and management of user orders from placement to fulfillment.
Reviews and Ratings: Enables users to provide feedback and ratings on products to assist others in making informed decisions.
Recommendation Engine: Analyzes user behavior and preferences to provide personalized product suggestions and improve user engagement.
Order Fulfillment and Shipping: Manages the fulfillment process, including generating shipping labels, tracking shipments, and updating delivery status.
Search and Filtering: Enables users to search for specific products and apply filters to refine search results.
Inventory Management: Tracks and manages product inventory levels to ensure accurate availability and restocking.

Now
User: {input}. Give me a list of components for the design that covers the requirement, and their core functionality
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
            streaming=True, callback_manager=CallbackManager([StreamingGeneratorCallbackHandler(self.token_generator)])
        )

        chain = self.chain_class(prompt=self.prompt, llm=llm, verbose=True)
        outputs = {"response": chain.run(inputs)}
        self.token_generator.close()
        return outputs
