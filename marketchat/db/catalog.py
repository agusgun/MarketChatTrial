from collections import namedtuple


Item = namedtuple('Item', ['name', 'image', 'price', 'promo'])
Store = namedtuple('Store', ['name', 'items'])
Category = namedtuple('Category', ['name', 'items'])

# Items.

items = [
  Item(
    name="Skinny Patched Up Jeans A|X",
    image="https://cdn.yoox.biz/46/46539875vo_14_f.jpg",
    price=1400000,
    promo=None),
  Item(
    name="Camo Jacquard Straight Fit Jeans A|X",
    image="https://cdn.yoox.biz/46/46532237xt_14_f.jpg",
    price=1320000,
    promo=0.5),
  Item(
    name="Arabian Egg",
    image="https://matriposterous.files.wordpress.com/2010/11/image_298.jpg",
    price=25000,
    promo=None),
  Item(
    name="Australian Egg",
    image="https://22251-presscdn-pagely.netdna-ssl.com/wp-content/uploads/2015/09/1401323431993.jpg",
    price=25000,
    promo=None)
]

popular_items = [
  items[0],
  items[1]
]

promo_items = [
  for item in items if item.promo is not None
]

# Stores.

stores = [
  Store(
    name="Yogya Kepatihan",
    items=[
      items[0],
      items[2]
    ]
  ),
  Store(
    name="Yogya Riau",
    items=[
      items[1],
      items[3]
    ]
  ),
]

# Categories.

categories = [
  Category(
    name="Grocery",
    items=[
      items[2],
      items[3]
    ]
  ),
  Category(
    name="Fashion",
    items=[
      items[0],
      items[1]
    ]
  )
]


__all__ = [
  'Item', 'Store', 'Category',
  'items', 'popular_items', 'promo_items',
  'stores', 'categories'
]
