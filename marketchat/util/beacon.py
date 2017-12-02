from collections import namedtuple
from urllib.parse import ParseResult, urlparse, urlunparse, urlencode, parse_qs


Beacon = namedtuple('Beacon', ['action', 'params'])

def make_beacon(action, **kwargs):
  return urlunparse(ParseResult(
    scheme='', netloc='', path=action, params='', query=urlencode(kwargs), fragment=''))

def parse_beacon(url):
  parts = urlparse(url)
  action = parts.path
  params = {k: (v if len(v) > 1 else v[0]) for k, v in parse_qs(parts.query)}

  return Beacon(action, params)


__all__ = ['Beacon', 'make_beacon', 'parse_beacon']
