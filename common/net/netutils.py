import re

import requests


def get_content(ref):
    ref = url_formatter(ref)

    return requests.get(ref, allow_redirects=True).content


def url_formatter(ref):
    if not re.match('(?:http|https):', ref):
        return f'https:{ref}'

    return ref
