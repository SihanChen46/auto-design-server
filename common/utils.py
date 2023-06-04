import random


from env import OPENAI_API_KEYS


def get_openai_api_key():
    openai_api_keys = OPENAI_API_KEYS
    if len(openai_api_keys) > 0:
        return random.choice(openai_api_keys)
    else:
        raise ValueError('no openai api key found')
