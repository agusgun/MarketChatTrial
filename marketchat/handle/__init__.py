from marketchat.util.router import Router
from . import default, search

route = Router()

route.handle(default.route)
route.handle(search.route)

__all__ = ['route']
