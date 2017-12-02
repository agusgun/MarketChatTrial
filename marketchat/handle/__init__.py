from marketchat.util.router import Router
from . import default, compare, search, view

route = Router()

route.handle(default.route)
route.handle(compare.route)
route.handle(search.route)
route.handle(view.route)

__all__ = ['route']
