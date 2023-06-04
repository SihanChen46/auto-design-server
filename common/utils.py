import random


def get_openai_api_key():
    openai_api_keys = ['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']
    if len(openai_api_keys) > 0:
        return random.choice(openai_api_keys)
    else:
        raise ValueError('no openai api key found')
