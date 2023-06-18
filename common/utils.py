import random
import os
import ast


def get_openai_api_key():
    openai_api_keys = ast.literal_eval(os.getenv('OPENAI_API_KEYS'))
    if len(openai_api_keys) > 0:
        return random.choice(openai_api_keys)
    else:
        raise ValueError("no openai api key found")
