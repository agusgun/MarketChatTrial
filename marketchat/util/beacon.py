from collections import namedtuple
from urllib.parse import ParseResult, urlparse, urlunparse, urlencode, parse_qs


Beacon = namedtuple('Beacon', ['action', 'params'])


def make_beacon(action, **kwargs):
    params = [(k, val) for k, v in kwargs.items()
              for val in (v if isinstance(v, list) else [v])]

    return urlunparse(ParseResult(
        scheme='', netloc='', path=action, params='', query=urlencode(params), fragment=''))


def parse_beacon(url):
    parts = urlparse(url)
    action = parts.path
    params = {k: (v if len(v) > 1 else v[0]) for k, v in parse_qs(
        parts.query).items()}

    return Beacon(action, params)


__all__ = ['Beacon', 'make_beacon', 'parse_beacon']
