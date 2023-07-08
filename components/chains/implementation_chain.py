# encoding:utf-8
from typing import List, Dict
import tiktoken
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains.base import Chain
from common.utils import get_openai_api_key
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from common import log


class ImplementationChain(Chain):
    model_class = ChatOpenAI
    chain_class = LLMChain
    model_name = "gpt-3.5-turbo-16k"
    temperature = 0.75
    max_tokens = 16000
    prompt = PromptTemplate(
        input_variables=[
            "designed_file_structure",
            "designed_data_types",
            "designed_interfaces",
            "programming_language"
        ],
        template="""
system: You are a tech lead who's good at building software, your goal is the help user to implement all the designed data types and interfaces in details so it can go to production.

You will output the content of each file in the file structure including ALL code.
Each file must strictly follow a markdown code block format, where the following tokens must be replaced such that
FILENAME is the lowercase file name including the file extension,
LANG is the markup code block language for the code's language, and CODE is the code:

FILENAME
```LANG
CODE
```

Please note that the code should be fully functional. No placeholders.

You will start with the "entrypoint" file, then go to the ones that are imported by that file, and so on. Before finishing, make sure that that all files in the designed_file_structure are implemented.
Follow a language and framework appropriate best practice file naming convention.
Make sure that files contain all imports, types etc. The code should be fully functional. Make sure that code in different files are compatible with each other.

This is an example
User:
Designed File Structure:
```
{{
  "twitter_search_engine": {{
    "app.py": {{}},
    "components": {{
      "search_algorithm.py": {{}},
    }}
    "models": {{
      "search_query.py": {{}},
      "tweet.py": {{}},
      "search_result.py": {{}},
    }}
  }}
}}
```
Designed Data Types:
```
SearchResult:
    tweets: list of Tweet
    query: SearchQuery
    total_matches: int
    search_time: float

SearchQuery:
    raw_query: string
    tokenized_query: list of string
    query_time: int
    boolean_operators: list of string

Tweet:
    id: string
    content: string
    user_id: string
    timestamp: int
    location: string
    retweets_count: int
    likes_count: int
    replies_count: int
```
Designed Interfaces:
```
SearchAlgorithm:
  process_search_query(query: SearchQuery) -> SearchQuery
  tokenize_search_query(query: SearchQuery) -> list[string]
  normalize_search_query(query: SearchQuery) -> SearchQuery
  execute_search(query: SearchQuery) -> SearchResult
  update_search_index(tweet_updates: list[Tweet]) -> string
```
Can you implement it in Python?
You:
# twitter_search_engine/app.py
```python
from fastapi import FastAPI
from components.search_algorithm import SearchAlgorithm

app = FastAPI()
search_algorithm = SearchAlgorithm()

@app.post("/search")
async def search(req: SearchReq) -> SearchResponse:
    query = req.query
    
    processed_query = search_algorithm.process_search_query(query)
    tokenized_query = search_algorithm.tokenize_search_query(processed_query)
    normalized_query = search_algorithm.normalize_search_query(tokenized_query)
    search_result = search_algorithm.execute_search(normalized_query)
    return search_result
```

# twitter_search_engine/components/search_algorithm.py
```python
from typing import List
from models.search_query import SearchQuery
from models.search_result import SearchResult
from models.tweet import Tweet

class SearchAlgorithm:
    def process_search_query(self, query: SearchQuery) -> SearchQuery:
        # Process the search query and return the processed query
        processed_query = None
        # Implement query processing logic and return processed query
        return processed_query

    def tokenize_search_query(self, query: SearchQuery) -> List[str]:
        # Tokenize the search query and return the list of tokens
        tokens = []
        # Implement tokenization logic and return tokens
        return tokens

    def normalize_search_query(self, query: SearchQuery) -> SearchQuery:
        # Normalize the search query and return the normalized query
        normalized_query = None
        # Implement normalization logic and return normalized query
        return normalized_query

    def execute_search(self, query: SearchQuery) -> SearchResult:
        # Execute the search query and return the search results
        search_result = None
        # Implement search execution logic and return search result
        return search_result
```

# twitter_search_engine/models/search_query.py
```python
from dataclasses import dataclass
from typing import List

@dataclass
class SearchQuery:
    raw_query: str
    tokenized_query: List[str]
    query_time: int
    boolean_operators: List[str]
```

# twitter_search_engine/models/tweet.py
```python
from dataclasses import dataclass

@dataclass
class Tweet:
    id: str
    content: str
    user_id: str
    timestamp: int
    location: str
    retweets_count: int
    likes_count: int
    replies_count: int
```

# twitter_search_engine/models/search_result.py
```python
from dataclasses import dataclass
from typing import List
from .tweet import Tweet
from .search_query import SearchQuery

@dataclass
class SearchResult:
    tweets: List[Tweet]
    query: SearchQuery
    total_matches: int
    search_time: float
```

Now
User:
Designed File Structure:
```
{designed_file_structure}
```
Designed Data Types:
```
{designed_data_types}
```
Designed Interfaces:
```
{designed_interfaces}
```
Can you implement it in {programming_language}?
You:
""",
    )

    @property
    def input_keys(self) -> List[str]:
        return ["designed_file_structure", "designed_data_types", "designed_interfaces", "programming_language"]

    @property
    def output_keys(self) -> List[str]:
        return ["implementation"]

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
            callback_manager=CallbackManager([StreamingStdOutCallbackHandler()])
        )

        chain = self.chain_class(prompt=self.prompt, llm=llm, verbose=False)
        outputs = {"implementation": chain.run(inputs)}
        return outputs
