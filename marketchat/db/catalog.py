from collections import namedtuple
from enum import Flag, auto


class ItemFlag(Flag):
    POPULAR = auto()

Item = namedtuple(
    'Item', ['name', 'image', 'category', 'store', 'price', 'stock', 'deliv', 'promo', 'flags'])
Status = namedtuple('Status', ['item', 'status'])


# Items.

items = [
    Item(
        name="Skinny Patched Up Jeans A|X",
        image="https://cdn.yoox.biz/46/46539875vo_14_f.jpg",
        category="Fashion",
        store="Yogya Kepatihan",
        price=1400000,
        stock=30,
        deliv="cost free delivery",
        promo=None,
        flags=ItemFlag.POPULAR),
    Item(
        name="Camo Jacquard Straight Fit Jeans A|X",
        image="https://cdn.yoox.biz/46/46532237xt_14_f.jpg",
        category="Fashion",
        store="Yogya Kepatihan",
        price=1320000,
        stock=20,
        deliv="cost free delivery",
        promo=0.5,
        flags=ItemFlag(0)),
    Item(
        name="Arabian Egg",
        image="https://matriposterous.files.wordpress.com/2010/11/image_298.jpg",
        category="Grocery",
        store="Yogya Riau",
        price=25000,
        stock=100,
        deliv="cost free delivery",
        promo=None,
        flags=ItemFlag(0)),
    Item(
        name="Australian Egg",
        image="https://22251-presscdn-pagely.netdna-ssl.com/wp-content/uploads/2015/09/1401323431993.jpg",
        category="Grocery",
        store="Yogya Riau",
        price=25000,
        stock=70,
        deliv="cost free delivery",
        promo=None,
        flags=ItemFlag(0)),
    Item(
        name="AGV Corsa Misrano Ltd. 2015",
        image="https://www.fc-moto.de/WebRoot/FCMotoDB/Shops/10207048/576B/26BB/C2F2/BBC0/CDF8/4DEB/AEAD/5F3E/AGV_Corsa_Misano_Ltd._Integralhelm_2015.jpg",
        category="Automotive",
        store="Juragan Helm",
        price=10039555,
        stock=15,
        deliv="cost free delivery",
        promo=None,
        flags=ItemFlag.POPULAR),
    Item(
        name="AGV Pista GP R Carbon Anniversario",
        image="https://www.revzilla.com/product_images/0298/6934/agv_pista_gpr_carbon_anniversario_helmet.jpg",
        category="Automotive",
        store="Juragan Helm",
        price=21624876,
        stock=10,
        deliv="cost free delivery",
        promo=0.8,
        flags=ItemFlag(0)),
    Item(
        name="iPhone X 256GB",
        image="https://macpoin.com/wp-content/uploads/2017/11/iphonexfrontback-800x573.jpg",
        category="Electronics",
        store="BEC Electronics",
        price=18493139,
        stock=15,
        deliv="cost free delivery",
        promo=0.9,
        flags=ItemFlag(0)),
    Item(
        name="New Surface Pro Intel Core i5",
        image="https://d2rormqr1qwzpz.cloudfront.net/photos/2017/05/24/95255-791b0235bc0a24f7a1269cc42a180b4f.jpg",
        category="Electronics",
        store="BEC Electronics",
        price=148513514,
        stock=25,
        deliv="cost free delivery",
        promo=0.8,
        flags=ItemFlag.POPULAR)
]


# Stores.

stores = list({
    item.store for item in items
})

categories = list({
    item.category for item in items
})


# Statuses.

statuses = [
    Status(
        item=items[0],
        status="Delivering"),
    Status(
        item=items[1],
        status="Packing"),
]


__all__ = [
    'Item', 'ItemFlag',
    'items', 'stores', 'categories'
]
