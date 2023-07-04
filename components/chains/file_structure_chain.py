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


class FileStructureChain(Chain):
    model_class = ChatOpenAI
    chain_class = LLMChain
    model_name = "gpt-3.5-turbo-16k"
    temperature = 0.75
    max_tokens = 16000
    prompt = PromptTemplate(
        input_variables=["designed_data_types",
                         "designed_interfaces", "programming_language"],
        template="""
System: you are a tech lead who's good at building software, your goal is to help the user design their project file stucture so it's organized and can deploy easily.
You will start with creating an "entrypoint" file, then structure the necessary files that will be imported by that file, and so on. Follow a language and framework appropriate best practice for file naming convention.
Ensure that the files are designed to contain all necessary imports, types etc. Make sure that the structured files are compatible with each other in terms of code organization. Before you finish, double check that all parts of the architecture are represented within the file structure.
Demonstrate the file structure using json.
Wrap the file structure in ``` ``` block like the example.

This is an example
User:
Data Types:
```
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

SearchResult:
    tweets: list of Tweet
    query: SearchQuery
    total_matches: int
    search_time: float

User:
    id: string
    username: string
    name: string
    profile_image_url: string
    verified: boolean
    following: list of string
    followers: list of string
    liked_tweets: list of string
    retweeted_tweets: list of string
    replied_tweets: list of string

FilterOptions:
    date_range: tuple of int
    location: string
    language: string
    user_type: string
    user_id: string
    includes_media: boolean
    hashtags: list of string

UserPreferences:
    preferred_languages: list of string
    preferred_topics: list of string

AnalyticsData:
    search_queries: list of SearchQuery
    successful_search_queries: list of SearchQuery
    failed_search_queries: list of SearchQuery
    user_logins: list of User
    user_activity: dict (key: string, value: list of Tweet)
```
Interfaces:
```
SearchAlgorithm:
  process_search_query(query: SearchQuery) -> SearchQuery
  tokenize_search_query(query: SearchQuery) -> list[string]
  normalize_search_query(query: SearchQuery) -> SearchQuery
  execute_search(query: SearchQuery) -> SearchResult
  update_search_index(tweet_updates: list[Tweet]) -> string

TweetIndexer:
  fetch_matching_tweets(query: SearchQuery) -> list[Tweet]
  index_tweet(tweet: Tweet) -> string
  update_tweet_index(tweet_updates: list[Tweet]) -> string

TweetRanker:
  sort_tweets_by_rank(tweets: list[Tweet]) -> list[Tweet]
  modify_ranking_parameters(parameters: dict) -> string

UserInterface:
  show_search_results(search_result: SearchResult) -> None
  show_tweet(tweet: Tweet) -> None
  show_user_profile(user: User) -> None
  navigate_tweets() -> list[Tweet]
  implement_filters(filter_options: FilterOptions, tweets: list[Tweet]) -> list[Tweet]
  display_error_message(error_message: string) -> None
  initiate_login() -> User

TweetUpdateMonitor:
  initiate_tweet_monitoring() -> string
  terminate_tweet_monitoring() -> string
  fetch_new_tweets() -> list[Tweet]
  distribute_notifications(new_tweets: list[Tweet]) -> None

AdvancedSearcher:
  execute_advanced_search(query: SearchQuery) -> SearchResult
  search_tweets_by_date(query: SearchQuery, date: tuple[int, int]) -> list[Tweet], string
  search_tweets_by_location(query: SearchQuery, location: string) -> list[Tweet], string
  search_tweets_by_user(query: SearchQuery, user: User) -> list[Tweet], string

UserPreferenceManager:
  implement_user_preferences(user_preferences: UserPreferences) -> None
  modify_user_preferences(updated_preferences: UserPreferences) -> string
  fetch_user_preferences() -> UserPreferences

AnalyticsMonitor:
  monitor_search_usage(usage_data: AnalyticsData) -> None
  monitor_search_query(search_query: SearchQuery) -> None
  monitor_successful_search_query(successful_query: SearchQuery) -> None
  monitor_failed_search_query(failed_query: SearchQuery) -> None
  monitor_login_attempts(user: User) -> None
  monitor_user_activity(user_activity: dict[string, list[Tweet]]) -> None
```
Can you design the file structure for this project in this programming language: python

You:
```
{{
  "twitter_search_engine": {{
    "app.py": {{}},
    "components": {{
      "__init__.py": {{}},
      "user_interface.py": {{}},
      "search_algorithm.py": {{}},
      "tweet_indexer.py": {{}},
      "tweet_ranker.py": {{}},
      "tweet_update_monitor.py": {{}},
      "advanced_searcher.py": {{}},
      "user_preference_manager.py": {{}},
      "analytics_monitor.py": {{}}
    }}
    "models": {{
      "__init__.py": {{}},
      "search_query.py": {{}},
      "tweet.py": {{}},
      "search_result.py": {{}},
      "user.py": {{}},
      "filter_options.py": {{}},
      "user_preferences.py": {{}},
      "analytics_data.py": {{}}
    }},
    "utils": {{
      "__init__.py": {{}},
      "common_functions.py": {{}},
      "constants.py": {{}}
    }},
    "tests": {{
      "__init__.py": {{}},
      "test_search_algorithm.py": {{}},
      "test_tweet_indexer.py": {{}},
      "test_tweet_ranker.py": {{}},
      "test_user_interface.py": {{}},
      "test_tweet_update_monitor.py": {{}},
      "test_advanced_searcher.py": {{}},
      "test_user_preference_manager.py": {{}},
      "test_analytics_monitor.py": {{}}
    }},
    "config": {{
      "__init__.py": {{}},
      "settings.py": {{}},
      "logging.py": {{}}
    }},
    "static": {{}},
    "templates": {{}},
    "README.md": {{}},
    ".gitignore": {{}}
  }}
}}
```

Now
User:
Data Types:
```
{designed_data_types}
```
Interfaces:
```
{designed_interfaces}
```
Can you design the file structure for this project in this programming language: {programming_language}

You:
""",
    )

    @property
    def input_keys(self) -> List[str]:
        return ["designed_data_types",
                "designed_interfaces", "programming_language"]

    @property
    def output_keys(self) -> List[str]:
        return ["file_structure"]

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
        outputs = chain.run(inputs)
        file_structure = outputs.split('```')[1]
        outputs = {"file_structure": file_structure}
        return outputs
