from marketchat.util.router import main_router
from . import default, compare, promo, search, view, payment

route = main_router

route.handle(default.route)
route.handle(compare.route)
route.handle(promo.route)
route.handle(search.route)
route.handle(view.route)
route.handle(payment.route)

__all__ = ['route']
