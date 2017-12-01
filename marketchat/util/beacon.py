from urllib.parse import ParseResult, urlparse, urlunparse, urlencode, parse_qs


class Beacon:
  def __init__(self):
    self.action = ''
    self.params = {}

  @staticmethod
  def build(action, **kwargs):
    beacon = Beacon()

    beacon.action = action
    beacon.params = kwargs
    return beacon

  @staticmethod
  def decode(url):
    beacon = Beacon()

    parts = urlparse(url)
    beacon.action = parts.path
    beacon.params = parse_qs(parts.query)
    return beacon

  def encode(self):
    return urlunparse(ParseResult(
      scheme='', netloc='', path=self.action, params='', query=urlencode(
        self.params), fragment=''))


# Shortcut to build beacons.
make_beacon = Beacon.build


__all__ = ['Beacon', 'make_beacon']
