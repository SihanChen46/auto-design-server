import argparse
import ast
import backoff
import openai
from openai.embeddings_utils import cosine_similarity
import os
import pandas as pd
import tiktoken
import time


openai.api_key = os.environ["OPENAI_API_KEY"]


def num_tokens_from_messages(messages, model="gpt-3.5-turbo-0301"):
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


def get_contextual_examples(df, embedding, n):
    """
    Return the rankings of the contextual examples based on their
    semantic relevance to the user content.
    """
    df["Cosine Similarity"] = df["Context and Source Embedding"].apply(lambda x: cosine_similarity(ast.literal_eval(x), embedding))
    res = df.sort_values("Cosine Similarity", ascending=False).head(n)
    return res


def get_counterfactual_masculine_examples(df, embedding, n):
    """
    Return the rankings of the counterfactual masculine examples based
    on their semantic relevance to the user content.
    """
    df["Cosine Similarity"] = df["Masculine Embedding"].apply(lambda x: cosine_similarity(ast.literal_eval(x), embedding))
    res = df.sort_values("Cosine Similarity", ascending=False).head(n)
    return res


def get_counterfactual_feminine_examples(df, embedding, n):
    """
    Return the rankings of the counterfactual feminine examples based
    on their semantic relevance to the user content.
    """
    df["Cosine Similarity"] = df["Feminine Embedding"].apply(lambda x: cosine_similarity(ast.literal_eval(x), embedding))
    res = df.sort_values("Cosine Similarity", ascending=False).head(n)
    return res


@backoff.on_exception(backoff.expo, openai.error.RateLimitError)
def get_response(target_lang, message, n, example_content, user_content, max_tokens=4000):
    """
    Return the completion from OpenAI's gpt-3.5-turbo engine given 
    the system and user prompts.
    """
    lang_codes = {
        "en": "English",
        "ar": "Arabic",
        "de": "German",
        "es": "Spanish",
        "fr": "French",
        "hi": "Hindi",
        "it": "Italian",
        "pt": "Portuguese",
        "ru": "Russian"
    }
    src_lang = "en"
    messages_codes = {
        "tsp": {
            1: [{"role": "user", "content": f"Here is one correct {lang_codes[target_lang]} translation: {example_content} Please provide the {lang_codes[target_lang]} translation for the following sentence: {user_content}"}],
            2: [{"role": "user", "content": f"Here are two correct {lang_codes[target_lang]} translations: {example_content} Please provide the {lang_codes[target_lang]} translation for the following sentence: {user_content}"}],
            3: [{"role": "user", "content": f"Here are three correct {lang_codes[target_lang]} translations: {example_content} Please provide the {lang_codes[target_lang]} translation for the following sentence: {user_content}"}]},
        "csp": {
            1: [{"role": "system", "content": f"You are a machine translation system that translates {lang_codes[src_lang]} to {lang_codes[target_lang]}."},
                {"role": "user", "content": f"Here is one correct {lang_codes[target_lang]} translation: {example_content} Please provide the {lang_codes[target_lang]} translation for the following sentence: {user_content}"}],
            2: [{"role": "system", "content": f"You are a machine translation system that translates {lang_codes[src_lang]} to {lang_codes[target_lang]}."},
                {"role": "user", "content": f"Here are two correct {lang_codes[target_lang]} translations: {example_content} Please provide the {lang_codes[target_lang]} translation for the following sentence: {user_content}"}],
            3: [{"role": "system", "content": f"You are a machine translation system that translates {lang_codes[src_lang]} to {lang_codes[target_lang]}."},
                {"role": "user", "content": f"Here are three correct {lang_codes[target_lang]} translations: {example_content} Please provide the {lang_codes[target_lang]} translation for the following sentence: {user_content}"}]},
        "dsp": {
            1: [{"role": "system", "content": f"You are a machine translation system that translates {lang_codes[src_lang]} to {lang_codes[target_lang]}."},
                {"role": "user", "content": f"Here is one correct {lang_codes[target_lang]} translation: {example_content} Please provide the {lang_codes[target_lang]} translation for the following sentence without gender bias: {user_content}"}],
            2: [{"role": "system", "content": f"You are a machine translation system that translates {lang_codes[src_lang]} to {lang_codes[target_lang]}."},
                {"role": "user", "content": f"Here are two correct {lang_codes[target_lang]} translations: {example_content} Please provide the {lang_codes[target_lang]} translation for the following sentence without gender bias: {user_content}"}],
            3: [{"role": "system", "content": f"You are a machine translation system that translates {lang_codes[src_lang]} to {lang_codes[target_lang]}."},
                {"role": "user", "content": f"Here are three correct {lang_codes[target_lang]} translations: {example_content} Please provide the {lang_codes[target_lang]} translation for the following sentence without gender bias: {user_content}"}]}
    }
    try:
        messages = messages_codes[message][n]
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            temperature=0,
            max_tokens=max_tokens - num_tokens_from_messages(messages),
            messages=messages)
        return completion["choices"][0]["message"]["content"]
    except openai.error.APIError as e:
        time.sleep(10)
        return get_response(target_lang, message, n, example_content, user_content)
    except openai.error.APIConnectionError as e:
        time.sleep(10)
        return get_response(target_lang, message, n, example_content, user_content)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--target_lang", type=str,
                        choices=["ar", "de", "es", "fr", "hi", "it", "pt", "ru"])
    parser.add_argument("--dataset", type=str,
                        choices=["contextual", "counterfactual"])
    parser.add_argument("--data_split", type=str,
                        choices=["dev", "test"])
    parser.add_argument("--translation_prompt", type=str,
                        choices=["tsp", "csp", "dsp"])
    parser.add_argument("--examples", type=int,
                        choices=[1, 2, 3])
    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    if args.data_split not in ["dev", "test"]:
        raise ValueError(f"Invalid argument for data_split {args.data_split}. Valid options are dev and test.")
    if args.translation_prompt not in ["tsp", "csp", "dsp"]:
        raise ValueError(f"Invalid argument for translation_prompt {args.translation_prompt}. Valid options are tsp, csp, and dsp.")
    if args.examples not in [1, 2, 3]:
        raise ValueError(f"Invalid argument for examples {args.examples}. Valid options are 1, 2, 3.")
    current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    count = 0
    if args.dataset == "contextual":
        test_path = f"{current_dir}/data/csv/context/geneval-context-test.en_{args.target_lang}.en.csv"
        test_df = pd.read_csv(test_path)
        dev_path = f"{current_dir}/data/csv/context/geneval-context-dev.en_{args.target_lang}.en.csv"
        dev_df = pd.read_csv(dev_path)
        res_path = f"{current_dir}/result/fs/context/geneval-context-wikiprofessions-2to1-test.en_{args.target_lang}.en.{args.translation_prompt}{args.examples}"
        for user_content, user_embedding, zs_output, accuracy in zip(test_df["Context and Source"], test_df["Context and Source Embedding"],
                                                                     test_df["Zero-Shot Reference"], test_df["Zero-Shot Accuracy"]):
            count += 1
            print(f"Line {count}: {user_content}")
            if accuracy == "Correct":
                with open(res_path, "a") as res_file:
                    print(f"Output: {zs_output}")
                    res_file.write(zs_output + "\n")
            elif accuracy == "Incorrect":
                user_embedding = ast.literal_eval(user_embedding)
                res_df = get_contextual_examples(dev_df, user_embedding, args.examples)
                example_content = ""
                for i in range(args.examples):
                    example_content += res_df.iloc[i]["Context and Source"] + "\n" + res_df.iloc[i]["Correct Reference"] + "\n"
                with open(res_path, "a") as res_file:
                    output = get_response(args.target_lang, args.translation_prompt, args.examples, example_content, user_content)
                    print(f"Output: {output}")
                    res_file.write(output + "\n")
    elif args.dataset == "counterfactual":
        test_path = f"{current_dir}/data/csv/sentences/geneval-sentences-test.en_{args.target_lang}.en.csv"
        test_df = pd.read_csv(test_path)
        dev_path = f"{current_dir}/data/csv/sentences/geneval-sentences-dev.en_{args.target_lang}.en.csv"
        dev_df = pd.read_csv(dev_path)
        res_path = [
            f"{current_dir}/result/fs/sentences/{args.data_split}/geneval-sentences-masculine-{args.data_split}.en_{args.target_lang}.en.{args.translation_prompt}{args.examples}",
            f"{current_dir}/result/fs/sentences/{args.data_split}/geneval-sentences-feminine-{args.data_split}.en_{args.target_lang}.en.{args.translation_prompt}{args.examples}"
        ]
        for user_content, user_embedding, zs_output, accuracy in zip(test_df["Masculine Source"], test_df["Masculine Embedding"],
                                                                     test_df["Masculine Zero-Shot Reference"], test_df["Masculine Zero-Shot Accuracy"]):
            count += 1
            print(f"Line {count}: {user_content}")
            if accuracy == "Correct":
                with open(res_path[0], "a") as res_file:
                    print(f"Output: {zs_output}")
                    res_file.write(zs_output + "\n")
            elif accuracy == "Incorrect":
                user_embedding = ast.literal_eval(user_embedding)
                res_df = get_counterfactual_masculine_examples(dev_df, user_embedding, args.examples)
                example_content = ""
                for i in range(args.examples):
                    example_content += res_df.iloc[i]["Masculine Source"] + "\n" + res_df.iloc[i]["Masculine Reference"] + "\n"
                with open(res_path[0], "a") as res_file:
                    output = get_response(args.target_lang, args.translation_prompt, args.examples, example_content, user_content)
                    print(f"Output: {output}")
                    res_file.write(output + "\n")
        for user_content, user_embedding, zs_output, accuracy in zip(test_df["Feminine Source"], test_df["Feminine Embedding"],
                                                                     test_df["Feminine Zero-Shot Reference"], test_df["Feminine Zero-Shot Accuracy"]):
            count += 1
            print(f"Line {count}: {user_content}")
            if accuracy == "Correct":
                with open(res_path[1], "a") as res_file:
                    print(f"Output: {zs_output}")
                    res_file.write(zs_output + "\n")
            elif accuracy == "Incorrect":
                user_embedding = ast.literal_eval(user_embedding)
                res_df = get_counterfactual_feminine_examples(dev_df, user_embedding, args.examples)
                example_content = ""
                for i in range(args.examples):
                    example_content += res_df.iloc[i]["Feminine Source"] + "\n" + res_df.iloc[i]["Feminine Reference"] + "\n"
                with open(res_path[1], "a") as res_file:
                    output = get_response(args.target_lang, args.translation_prompt, args.examples, example_content, user_content)
                    print(f"Output: {output}")
                    res_file.write(output + "\n")
    else:
        raise ValueError(
            f"Invalid argument for dataset {args.dataset}. Valid options are contextual, counterfactual.")


if __name__ == '__main__':
    main()
