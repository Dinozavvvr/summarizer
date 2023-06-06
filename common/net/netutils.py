import re

import requests


def get_content(ref):
    ref = url_formatter(ref)

    return requests.get(ref, allow_redirects=True).content


def is_accesable(ref):
    response = requests.get(ref, allow_redirects=True)
    return response.ok


def url_formatter(ref):
    if not re.match('(?:http|https):', ref):
        return f'https:{ref}'

    return ref
