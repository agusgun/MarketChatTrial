from urllib.parse import urlencode, parse_qs

# Action key constant.
ACTION_KEY = 'a'

def encode_beacon(action, **kwargs):
  return urlencode({
    ACTION_KEY: action,
    **kwargs
  })

class Beacon:
  def __init__(self, data):
    qs = parse_qs(data)

    self.action = qs[ACTION_KEY][0]; del qs[ACTION_KEY]
    self.params = {k: (v if len(v) > 1 else v[0]) for k, v in qs.items()}


__all__ = ['encode_beacon', 'Beacon']
