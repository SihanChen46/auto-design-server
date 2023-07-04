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


class DataTypeInterfaceChain(Chain):
    model_class = ChatOpenAI
    chain_class = LLMChain
    model_name = "gpt-3.5-turbo-16k"
    temperature = 0.75
    max_tokens = 16000
    prompt = PromptTemplate(
        input_variables=["components", "sequence_diagram"],
        template="""
system: you are a tech lead who's good at designing interfaces for software, your goal is the help user to define the interfaces and data types based on their list of components and sequenccec diagram workflow.
Only for each component in the list, design a detailed abstract interface that follows a good engineer practice considering clarity, simplicity and Low Coupling. Make sure the methods are at the granular level it should be.
Think it step by step, you can start with interfaces, then data types, then update the interfaces based on data types.
Return the result in ``` ``` block like the example.
This is an example

User:
List of Components:
```
Search Bar: Allows users to enter keywords or hashtags they want to search for on Twitter.
Search Algorithm: Processes the user's search query and retrieves relevant tweets based on various factors such as relevance, popularity, and recency.
Indexing System: Organizes the tweets and user data in a searchable index to optimize search performance.
Ranking System: Ranks the search results based on their relevance to the user's query, taking into account factors such as engagement, author credibility, and recency.
User Interface: Presents the search results in a visually appealing and user-friendly format, allowing users to easily browse and interact with the tweets.
Filtering Options: Provides various options for users to filter the search results based on criteria such as date, location, language, and user type (e.g., verified accounts).
Real-time Updates: Continuously updates the search results as new tweets matching the user's query are posted, ensuring users have access to the most recent information.
Advanced Search Features: Offers advanced search functionality, including boolean operators, exact phrase matching, and filtering by media type (e.g., photos, videos).
Personalization: Takes into account the user's preferences, past search history, and social connections to deliver personalized search results tailored to their interests.
Analytics and Metrics: Tracks and analyzes search usage data to improve the search engine's performance, identify trends, and optimize search algorithms.v
```
Sequence Diagram:
```
sequenceDiagram
    participant User
    participant SearchBar
    participant SearchAlgorithm
    participant IndexingSystem
    participant RankingSystem
    participant UserInterface
    participant RealTimeUpdates
    participant AdvancedSearchFeatures
    participant Personalization
    participant AnalyticsMetrics

    User->>SearchBar: Enter keywords or hashtags
    SearchBar->>SearchAlgorithm: Send search query
    SearchAlgorithm->>IndexingSystem: Retrieve relevant tweets
    IndexingSystem->>SearchAlgorithm: Return relevant tweets
    SearchAlgorithm->>RankingSystem: Rank search results
    RankingSystem->>SearchAlgorithm: Return ranked search results
    SearchAlgorithm->>UserInterface: Send ranked search results
    UserInterface->>User: Display search results
    User->>UserInterface: Browse and interact with tweets
    UserInterface->>UserInterface: Apply filtering options
    RealTimeUpdates->>SearchAlgorithm: Monitor new tweets
    SearchAlgorithm->>RealTimeUpdates: Send matching tweets
    User->>SearchBar: Enter new keywords or hashtags
    SearchBar->>SearchAlgorithm: Send new search query
    SearchAlgorithm->>IndexingSystem: Retrieve new relevant tweets
    IndexingSystem->>SearchAlgorithm: Return new relevant tweets
    SearchAlgorithm->>RankingSystem: Rank new search results
    RankingSystem->>SearchAlgorithm: Return new ranked search results
    SearchAlgorithm->>UserInterface: Send new ranked search results
    UserInterface->>User: Display updated search results
    AdvancedSearchFeatures->>SearchAlgorithm: Perform additional search functionality
    Personalization->>SearchAlgorithm: Take user preferences into account
    AnalyticsMetrics->>SearchAlgorithm: Track and analyze search usage data
```
You:
Initial Interfaces:
```
SearchAlgorithm:
  process_search_query(query) -> processed_query
  tokenize_search_query(query) -> query_tokens
  normalize_search_query(query) -> normalized_query
  execute_search(query) -> search_results
  update_search_index(tweet_updates) -> update_status

TweetIndexer:
  fetch_matching_tweets(query) -> matching_tweets
  index_tweet(tweet) -> indexed_tweet
  update_tweet_index(tweet_updates) -> update_status

TweetRanker:
  sort_tweets_by_rank(tweets) -> ranked_tweets
  modify_ranking_parameters(parameters) -> update_status

UserInterface:
  show_search_results(tweets)
  show_tweet(tweet)
  show_user_profile(user_profile)
  navigate_tweets() -> browsed_tweets
  implement_filters(filter_options) -> filtered_tweets
  display_error_message(error_message)
  initiate_login()

TweetUpdateMonitor:
  initiate_tweet_monitoring() -> monitoring_status
  terminate_tweet_monitoring() -> monitoring_status
  fetch_new_tweets() -> new_tweets_batch
  distribute_notifications(new_tweets)

AdvancedSearcher:
  execute_advanced_search(query) -> advanced_search_results
  search_tweets_by_date(query, date) -> dated_results, search_status
  search_tweets_by_location(query, location) -> location_specific_results, search_status
  search_tweets_by_user(query, user) -> user_specific_results, search_status

UserPreferenceManager:
  implement_user_preferences(user_preferences) -> personalized_interface
  modify_user_preferences(updated_preferences) -> update_status
  fetch_user_preferences() -> current_preferences

AnalyticsMonitor:
  monitor_search_usage(usage_data)
  monitor_search_query(search_query)
  monitor_successful_search_query(successful_query)
  monitor_failed_search_query(failed_query)
  monitor_login_attempts(user)
  monitor_user_activity(user_activity)
```
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
Updated Interfaces:
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

Now:
User:
List of Components:
```
{components}
```
Sequence Diagram:
```
{sequence_diagram}
```
You:
""",
    )

    @property
    def input_keys(self) -> List[str]:
        return ["components", "sequence_diagram"]

    @property
    def output_keys(self) -> List[str]:
        return ["data_types", "interfaces"]

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
        data_types = outputs.split('```')[3]
        interfaces = outputs.split('```')[5]
        outputs = {"data_types": data_types, "interfaces": interfaces}
        return outputs
