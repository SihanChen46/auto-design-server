import argparse
import backoff
import openai
import os
import pandas as pd
import pickle
import tiktoken
import time


openai.api_key = os.environ["OPENAI_API_KEY"]


def num_tokens_from_messages(messages, model="gpt-4"):
    """
    Return the number of tokens in the messages.
    """
    encoding = tiktoken.encoding_for_model(model)
    num_tokens = 0
    for message in messages:
        num_tokens += 4
        for key, value in message.items():
            num_tokens += len(encoding.encode(value))
            if key == "name":
                num_tokens += -1
    num_tokens += 2
    return num_tokens


@backoff.on_exception(backoff.expo, openai.error.RateLimitError)
def get_response(target, user_content, max_tokens=8000):
    """
    Return the completion from OpenAI's GPT-4 given the user prompt.
    """
    messages = [
        {"role": "user", "content": f"Translate the following English text to {target}: {user_content}"}
    ]
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-4",
            temperature=0,
            max_tokens=max_tokens - num_tokens_from_messages(messages),
            messages=messages)
        return completion["choices"][0]["message"]["content"]
    except openai.error.Timeout as e:
        time.sleep(10)
        return get_response(target, user_content, max_tokens)
    except openai.error.APIError as e:
        time.sleep(10)
        return get_response(target, user_content, max_tokens)
    except openai.error.APIConnectionError as e:
        time.sleep(10)
        return get_response(target, user_content, max_tokens)
    except openai.error.RateLimitError as e:
        time.sleep(10)
        return get_response(target, user_content, max_tokens)
    

def ask_gpt_with_cache(target, user_content, cache, cache_path):
    """
    Return the completion using a cache to avoid recomputing.
    """
    print(f"Source: {user_content}\n")
    if user_content not in cache:
        cache[user_content] = get_response(target, user_content)
        with open(cache_path, "wb") as f:
            pickle.dump(cache, f)
    print(f"Reference: {cache[user_content]}\n")
    return cache[user_content]
    

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--target_lang", type=str, 
                        choices=["ar", "de", "es", "fr", "hi", "it", "pt", "ru"])
    parser.add_argument("--dataset", type=str, 
                        choices=["contextual", "counterfactual"])
    parser.add_argument("--data_split", type=str, 
                        choices=["dev", "test"])
    args = parser.parse_args()
    return args


def main():
    """
    Generate 0-Shot completions from OpenAI's GPT-4 for the counterfactual 
    and contextual datasets.
    """
    args = parse_args()
    lang_codes = {
        "en": "English",
        "ar": "Arabic",
        "de": "German",
        "es": "Spanish",
        "fr": "French",
        "hi": "Hindi",
        "it": "Italian",
        "pt": "Portuguese",
        "ru": "Russian",
    }
    current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = f"{current_dir}/data/{args.dataset}_en_{args.target_lang}_{args.data_split}.csv"
    cache_path = f"{current_dir}/data/{args.dataset}_en_{args.target_lang}_{args.data_split}_cache.pkl"
    df = pd.read_csv(data_path)
    try:
        cache = pd.read_pickle(cache_path)
    except FileNotFoundError: 
        cache = {}
    with open(cache_path, "wb") as f:
            pickle.dump(cache, f)
    if args.dataset == "contextual":
        df["Context"] = df["Context"].fillna("")
        df["GPT-4 (0-Shot)"] = df.apply(lambda row: ask_gpt_with_cache(lang_codes[args.target_lang], 
                                                                       row["Context"] + " " + row["Source"],
                                                                       cache, cache_path), axis=1)
    elif args.dataset == "counterfactual":
        df["Masculine GPT-4 (0-Shot)"] = df.apply(lambda row: ask_gpt_with_cache(lang_codes[args.target_lang], 
                                                                           row["Masculine Source"],
                                                                           cache, cache_path), axis=1)
        df["Feminine GPT-4 (0-Shot)"] = df.apply(lambda row: ask_gpt_with_cache(lang_codes[args.target_lang], 
                                                                          row["Feminine Source"],
                                                                          cache, cache_path), axis=1)
    df.to_csv(data_path, index=False)


if __name__ == '__main__':
    main()
