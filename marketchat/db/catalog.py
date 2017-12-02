from collections import namedtuple

Item = namedtuple(
  'Item', ['name', 'image', 'category', 'store', 'price', 'promo'])


# Items.

items = [
  Item(
    name="Skinny Patched Up Jeans A|X",
    image="https://cdn.yoox.biz/46/46539875vo_14_f.jpg",
    category="Fashion",
    store="Yogya Kepatihan",
    price=1400000,
    promo=None),
  Item(
    name="Camo Jacquard Straight Fit Jeans A|X",
    image="https://cdn.yoox.biz/46/46532237xt_14_f.jpg",
    category="Fashion",
    store="Yogya Kepatihan",
    price=1320000,
    promo=0.5),
  Item(
    name="Arabian Egg",
    image="https://matriposterous.files.wordpress.com/2010/11/image_298.jpg",
    category="Grocery",
    store="Yogya Riau",
    price=25000,
    promo=None),
  Item(
    name="Australian Egg",
    image="https://22251-presscdn-pagely.netdna-ssl.com/wp-content/uploads/2015/09/1401323431993.jpg",
    category="Grocery",
    store="Yogya Riau",
    price=25000,
    promo=None)
]

popular_items = [
  items[0],
  items[1]
]

promo_items = [
  item for item in items if item.promo is not None
]


# Stores.

stores = list({
  item.store for item in items
})

categories = list({
  item.category for item in items
})


__all__ = [
  'Item', 'Store', 'Category',
  'items', 'popular_items', 'promo_items',
  'stores', 'categories'
]
