from marketchat.util.router import Router
from . import default

route = Router()

route.handle(default.route)

__all__ = ['route']
